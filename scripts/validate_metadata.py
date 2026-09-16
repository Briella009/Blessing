#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
PACKAGE = ROOT / "datapackage.json"
JSONLD = ROOT / "metadata" / "aaio-dataset.jsonld"
CITATION = ROOT / "CITATION.cff"


def main() -> int:
    errors: list[str] = []

    try:
        package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: could not parse datapackage.json: {exc}")
        return 1

    try:
        jsonld = json.loads(JSONLD.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: could not parse metadata/aaio-dataset.jsonld: {exc}")
        return 1

    if package.get("name") != "africa-ai-incident-observatory":
        errors.append("datapackage name must be africa-ai-incident-observatory")
    if package.get("version") != VERSION:
        errors.append(f"datapackage version {package.get('version')} != VERSION {VERSION}")
    if package.get("profile") != "data-package":
        errors.append("datapackage profile must be data-package")

    licenses = package.get("licenses", [])
    if not any(item.get("name") == "CC-BY-4.0" for item in licenses if isinstance(item, dict)):
        errors.append("datapackage must declare CC-BY-4.0 data license")

    resources = package.get("resources", [])
    if not resources:
        errors.append("datapackage must contain resources")
    resource_names: set[str] = set()
    for resource in resources:
        if not isinstance(resource, dict):
            errors.append("datapackage resource must be an object")
            continue
        name = str(resource.get("name", "")).strip()
        path = str(resource.get("path", "")).strip()
        if not name:
            errors.append("datapackage resource missing name")
        if name in resource_names:
            errors.append(f"duplicate datapackage resource name: {name}")
        resource_names.add(name)
        if resource.get("profile") != "tabular-data-resource":
            errors.append(f"resource {name or '<unnamed>'} must use tabular-data-resource profile")
        if not path:
            errors.append(f"resource {name or '<unnamed>'} missing path")
        elif not (ROOT / path).exists():
            errors.append(f"resource path does not exist: {path}")
        schema = resource.get("schema")
        if schema:
            schema_path = ROOT / str(schema)
            if not schema_path.exists():
                errors.append(f"resource schema path does not exist: {schema}")
            else:
                try:
                    json.loads(schema_path.read_text(encoding="utf-8"))
                except Exception as exc:
                    errors.append(f"resource schema is not valid JSON: {schema}: {exc}")

    expected_resources = {
        "core-incidents",
        "multilingual-evidence",
        "operational-evidence",
        "watchlist",
        "record-history",
    }
    if not expected_resources <= resource_names:
        errors.append(
            "datapackage missing expected resources: "
            + ", ".join(sorted(expected_resources - resource_names))
        )

    core = next((r for r in resources if isinstance(r, dict) and r.get("name") == "core-incidents"), None)
    if not core or core.get("schema") != "schema/core-table-schema.json":
        errors.append("core-incidents must reference schema/core-table-schema.json")

    if jsonld.get("@context") != "https://schema.org":
        errors.append("JSON-LD @context must be https://schema.org")
    if jsonld.get("@type") != "Dataset":
        errors.append("JSON-LD @type must be Dataset")
    if jsonld.get("version") != VERSION:
        errors.append(f"JSON-LD version {jsonld.get('version')} != VERSION {VERSION}")
    if jsonld.get("license") != "https://creativecommons.org/licenses/by/4.0/":
        errors.append("JSON-LD must declare the CC BY 4.0 license URL")
    if not jsonld.get("description"):
        errors.append("JSON-LD description is required")
    if not jsonld.get("creator", {}).get("name"):
        errors.append("JSON-LD creator name is required")
    if not jsonld.get("distribution"):
        errors.append("JSON-LD must describe at least one distribution")

    citation_text = CITATION.read_text(encoding="utf-8")
    if f'version: "{VERSION}"' not in citation_text:
        errors.append("CITATION.cff version does not match VERSION")

    if errors:
        print("\n".join("ERROR: " + error for error in errors))
        return 1

    print(
        f"OK: machine-readable metadata validated for AAIO v{VERSION}; "
        f"{len(resources)} packaged resources are present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
