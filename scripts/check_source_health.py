#!/usr/bin/env python3
"""Audit the reachability of public evidence URLs used by AAIO.

This is a monitoring tool, not an evidence validator. A temporary HTTP error,
403, 429, bot challenge or network timeout does not make an incident invalid.
The script therefore exits successfully after completing an audit unless its
own inputs are malformed. Consumers should inspect status categories rather
than treating every non-2xx response as a dead source.
"""
from __future__ import annotations

import argparse
import csv
import json
import socket
import ssl
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
DEFAULT_OUTPUT = ROOT / "artifacts" / "source-health.json"
DEFAULT_MARKDOWN = ROOT / "artifacts" / "source-health.md"
USER_AGENT = "AAIO-Source-Health/1.0 (+https://github.com/Briella009/Africa-AI-Incident-Observatory)"

SOURCE_SPECS = [
    ("core", ROOT / "data" / "incidents.csv", "incident_id", ("source_1_url", "source_2_url", "aiid_url")),
    ("multilingual", ROOT / "data" / "multilingual_incidents.csv", "record_id", ("source_url",)),
    ("operational", ROOT / "data" / "operational_incidents.csv", "incident_id", ("source_1_url", "source_2_url", "aiid_url")),
    ("watchlist", ROOT / "data" / "watchlist.csv", "watch_id", ("source_url",)),
]


def is_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def collect_inventory() -> list[dict]:
    grouped: dict[str, dict[str, set[str]]] = defaultdict(lambda: {"layers": set(), "records": set()})

    for layer, path, id_field, url_fields in SOURCE_SPECS:
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                record_id = (row.get(id_field) or "").strip()
                for field in url_fields:
                    value = (row.get(field) or "").strip()
                    if not value:
                        continue
                    if not is_http_url(value):
                        raise ValueError(f"Invalid public source URL in {path.name} {record_id} {field}: {value}")
                    grouped[value]["layers"].add(layer)
                    if record_id:
                        grouped[value]["records"].add(record_id)

    inventory = []
    for url in sorted(grouped):
        inventory.append(
            {
                "url": url,
                "source_layers": sorted(grouped[url]["layers"]),
                "record_ids": sorted(grouped[url]["records"]),
            }
        )
    return inventory


def classify_http_status(status: int) -> str:
    if 200 <= status < 400:
        return "reachable"
    if status in {401, 403, 407, 429, 451}:
        return "access_blocked"
    if status in {404, 410}:
        return "not_found"
    if 400 <= status < 500:
        return "client_error"
    if 500 <= status < 600:
        return "server_error"
    return "unexpected_status"


def request_once(url: str, method: str, timeout: float) -> tuple[int | None, str, str | None]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/json,text/plain;q=0.8,*/*;q=0.5",
    }
    if method == "GET":
        headers["Range"] = "bytes=0-4095"
    request = Request(url, headers=headers, method=method)
    try:
        with urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
            status = response.getcode()
            return status, response.geturl(), None
    except HTTPError as exc:
        return exc.code, exc.geturl() or url, str(exc)
    except (URLError, socket.timeout, TimeoutError, ssl.SSLError, OSError) as exc:
        return None, url, f"{type(exc).__name__}: {exc}"


def audit_url(url: str, timeout: float) -> dict:
    status, final_url, error = request_once(url, "HEAD", timeout)
    method = "HEAD"

    # Some public sites reject HEAD or automated clients even though ordinary GET works.
    if status in {400, 401, 403, 405, 406, 429, 501} or status is None:
        get_status, get_final, get_error = request_once(url, "GET", timeout)
        if get_status is not None or status is None:
            status, final_url, error = get_status, get_final, get_error
            method = "GET"

    if status is None:
        category = "network_error"
    else:
        category = classify_http_status(status)

    return {
        "status": category,
        "http_status": status,
        "checked_method": method,
        "final_url": final_url,
        "error": error,
    }


def build_report(inventory: Iterable[dict], *, timeout: float, limit: int | None, inventory_only: bool) -> dict:
    items = list(inventory)
    if limit is not None:
        items = items[:limit]

    entries = []
    for item in items:
        result = {
            **item,
            "status": "inventory_only",
            "http_status": None,
            "checked_method": None,
            "final_url": item["url"],
            "error": None,
        }
        if not inventory_only:
            result.update(audit_url(item["url"], timeout))
        entries.append(result)

    counts = Counter(entry["status"] for entry in entries)
    return {
        "report_type": "AAIO public source health audit",
        "dataset_version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inventory_only": inventory_only,
        "url_count": len(entries),
        "status_counts": dict(sorted(counts.items())),
        "interpretation": (
            "HTTP reachability is operational metadata, not evidence validity. "
            "Access-blocked and network-error statuses can reflect bot protection, rate limiting, "
            "temporary outages or runner geography and must not automatically downgrade an incident."
        ),
        "entries": entries,
    }


def markdown_report(report: dict) -> str:
    lines = [
        "# AAIO source health audit",
        "",
        f"- Dataset version: `{report['dataset_version']}`",
        f"- Generated: `{report['generated_at']}`",
        f"- Unique URLs checked: **{report['url_count']}**",
        f"- Inventory-only mode: **{report['inventory_only']}**",
        "",
        "## Status summary",
        "",
        "| Status | URLs |",
        "|---|---:|",
    ]
    for status, count in report["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(
        [
            "",
            "> Reachability is not evidence validity. A 403/429, bot challenge, timeout or temporary server error must not automatically downgrade an AAIO incident.",
            "",
            "## URLs needing review",
            "",
        ]
    )
    review = [entry for entry in report["entries"] if entry["status"] not in {"reachable", "inventory_only"}]
    if not review:
        lines.append("No URLs were flagged in this audit.")
    else:
        for entry in review:
            code = entry["http_status"] if entry["http_status"] is not None else "n/a"
            records = ", ".join(entry["record_ids"]) or "unassigned"
            lines.append(f"- `{entry['status']}` HTTP `{code}` — {entry['url']} — records: {records}")

    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--inventory-only",
        action="store_true",
        help="Build the deduplicated source inventory without making network requests.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        inventory = collect_inventory()
        report = build_report(
            inventory,
            timeout=args.timeout,
            limit=args.limit,
            inventory_only=args.inventory_only,
        )
    except Exception as exc:
        print(f"ERROR: source-health audit could not be built: {exc}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(markdown_report(report), encoding="utf-8")

    print(
        f"OK: source-health audit built for {report['url_count']} unique public URLs; "
        + ", ".join(f"{key}={value}" for key, value in report["status_counts"].items())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
