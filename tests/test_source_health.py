import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_source_health.py"

spec = importlib.util.spec_from_file_location("aaio_source_health", SCRIPT)
health = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(health)


def test_http_status_classification_preserves_access_block_boundary():
    assert health.classify_http_status(200) == "reachable"
    assert health.classify_http_status(301) == "reachable"
    assert health.classify_http_status(403) == "access_blocked"
    assert health.classify_http_status(429) == "access_blocked"
    assert health.classify_http_status(404) == "not_found"
    assert health.classify_http_status(410) == "not_found"
    assert health.classify_http_status(503) == "server_error"


def test_inventory_collects_deduplicated_public_evidence_urls():
    inventory = health.collect_inventory()
    urls = [entry["url"] for entry in inventory]
    assert len(urls) == len(set(urls))
    assert len(urls) >= 20
    assert all(url.startswith(("http://", "https://")) for url in urls)
    assert any("incidentdatabase.ai" in url for url in urls)
    assert any("nature.com" in url for url in urls)
    assert any("saflii.org" in url for url in urls)


def test_inventory_preserves_record_and_layer_provenance():
    inventory = health.collect_inventory()
    nature = next(entry for entry in inventory if "s44360-026-00082-5" in entry["url"])
    assert "core" in nature["source_layers"]
    assert "operational" in nature["source_layers"]
    assert "AAIO-0018" in nature["record_ids"]
    assert "AAIO-OP-0001" in nature["record_ids"]


def test_inventory_only_cli_makes_reproducible_non_network_report(tmp_path):
    output = tmp_path / "source-health.json"
    markdown = tmp_path / "source-health.md"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--inventory-only",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["inventory_only"] is True
    assert payload["url_count"] >= 20
    assert payload["status_counts"] == {"inventory_only": payload["url_count"]}
    assert "Reachability is not evidence validity" in markdown.read_text(encoding="utf-8")
