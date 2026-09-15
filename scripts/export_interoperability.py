#!/usr/bin/env python3
"""Build a deterministic AAIO semantic interoperability export.

The export preserves AAIO provenance while aligning fields to AIID core concepts
and the OECD common reporting framework. It is not an official ingest schema or
an endorsement by either external project.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data" / "incidents.csv"
DEFAULT_MAPPING = ROOT / "mapping" / "interoperability-map-v1.json"
DEFAULT_OUTPUT = ROOT / "exports" / "aaio-interoperability-v1.json"
DEFAULT_SHA_OUTPUT = ROOT / "exports" / "aaio-interoperability-v1.sha256"
VERSION_FILE = ROOT / "VERSION"
EXPORT_SCHEMA_VERSION = "1.0.0"

NUMERIC_FIELDS = {
    "magnitude",
    "scale",
    "criticality",
    "irreversibility",
    "severity_score",
}

REQUIRED_SOURCE_FIELDS = {
    "incident_id",
    "title",
    "incident_date",
    "date_precision",
    "country",
    "countries_affected",
    "region",
    "sector",
    "system_type",
    "ai_system_or_tool",
    "incident_or_hazard",
    "harm_types",
    "affected_parties",
    "summary",
    "reported_intent",
    "response",
    "regulatory_or_legal_outcome",
    "magnitude",
    "scale",
    "criticality",
    "irreversibility",
    "evidence_confidence",
    "qualification_basis",
    "source_1_name",
    "source_1_url",
    "source_1_type",
    "source_2_name",
    "source_2_url",
    "source_2_type",
    "aiid_id",
    "aiid_url",
    "last_verified",
    "notes",
    "curator",
    "severity_score",
    "severity_band",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dataset_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def split_pipe(value: str) -> list[str]:
    return [part.strip() for part in value.split("|") if part.strip()]


def typed_row(row: dict[str, str]) -> dict[str, Any]:
    out: dict[str, Any] = dict(row)
    for field in NUMERIC_FIELDS:
        out[field] = int(out[field])
    return out


def read_rows(source: Path) -> list[dict[str, Any]]:
    with source.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED_SOURCE_FIELDS - set(reader.fieldnames or []))
        if missing:
            raise ValueError(
                "Source dataset is missing required fields: " + ", ".join(missing)
            )
        rows = [typed_row(row) for row in reader]

    ids = [row["incident_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Source dataset contains duplicate incident_id values")
    return sorted(rows, key=lambda row: row["incident_id"])


def read_mapping(path: Path) -> dict[str, Any]:
    mapping = json.loads(path.read_text(encoding="utf-8"))
    ids = [item.get("id") for item in mapping.get("oecd_common_reporting_framework", [])]
    if ids != list(range(1, 30)):
        raise ValueError("OECD mapping must contain criteria 1 through 29 in order")
    return mapping


def sources(row: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "name": row[f"source_{index}_name"],
            "url": row[f"source_{index}_url"],
            "source_type": row[f"source_{index}_type"],
        }
        for index in (1, 2)
    ]


def criterion(
    value: Any,
    status: str,
    source_fields: list[str],
    note: str | None = None,
    raw_aaio_value: Any = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "value": value,
        "status": status,
        "source_fields": source_fields,
    }
    if note:
        item["note"] = note
    if raw_aaio_value is not None:
        item["raw_aaio_value"] = raw_aaio_value
    return item


def oecd_alignment(row: dict[str, Any]) -> dict[str, Any]:
    srcs = sources(row)
    harm = split_pipe(row["harm_types"])
    affected = split_pipe(row["affected_parties"])

    criteria: dict[str, dict[str, Any]] = {
        str(index): criterion(None, "unmapped", []) for index in range(1, 30)
    }
    criteria.update(
        {
            "1": criterion(row["title"], "direct", ["title"]),
            "2": criterion(row["summary"], "direct", ["summary"]),
            "4": criterion(
                {
                    "name": row["curator"],
                    "role": None,
                    "affiliation": None,
                    "email": None,
                    "relation_to_incident": None,
                },
                "partial",
                ["curator"],
                "AAIO records the curator name, not the full OECD submitter-information fields.",
            ),
            "5": criterion(
                {"date": row["incident_date"], "precision": row["date_precision"]},
                "partial",
                ["incident_date", "date_precision"],
                "AAIO stores the earliest reasonably supported date and makes imprecision explicit.",
            ),
            "6": criterion(
                [row["country"]],
                "partial",
                ["country"],
                "AAIO primary country is exported separately from broader affected geography.",
            ),
            "7": criterion(srcs, "direct", ["source_1_*", "source_2_*"]),
            "8": criterion(
                {"name_or_tool": row["ai_system_or_tool"], "version": None},
                "partial",
                ["ai_system_or_tool"],
                "AAIO does not currently capture system version as a separate field.",
            ),
            "10": criterion(
                None,
                "unmapped",
                [
                    "severity_score",
                    "severity_band",
                    "magnitude",
                    "scale",
                    "criticality",
                    "irreversibility",
                ],
                "AAIO severity is a project rubric and is not converted into OECD CRF severity categories.",
                {
                    "score": row["severity_score"],
                    "band": row["severity_band"],
                    "dimensions": {
                        "magnitude": row["magnitude"],
                        "scale": row["scale"],
                        "criticality": row["criticality"],
                        "irreversibility": row["irreversibility"],
                    },
                },
            ),
            "11": criterion(
                None,
                "approximate",
                ["harm_types"],
                "AAIO free-form harm descriptors are preserved but not silently converted to OECD controlled values.",
                harm,
            ),
            "13": criterion(
                None,
                "unmapped",
                ["reported_intent"],
                "AAIO reported_intent is not equivalent to the OECD wrongful/unintended-use criterion.",
                row["reported_intent"],
            ),
            "14": criterion(
                None,
                "approximate",
                ["affected_parties"],
                "AAIO affected-party labels are preserved but not converted to OECD stakeholder categories without review.",
                affected,
            ),
            "17": criterion(
                None,
                "approximate",
                ["sector"],
                "AAIO sector labels are not ISIC-coded.",
                row["sector"],
            ),
            "20": criterion(
                None,
                "unmapped",
                ["scale"],
                "AAIO scale measures impact exposure; it is not deployment breadth.",
                row["scale"],
            ),
            "25": criterion(
                None,
                "unmapped",
                ["system_type"],
                "AAIO system_type is descriptive and is not converted to OECD task categories without manual classification.",
                row["system_type"],
            ),
            "27": criterion(
                row["response"],
                "partial",
                ["response"],
                "AAIO response is free text; response categories are not inferred.",
            ),
            "29": criterion(
                {
                    "reported_intent": row["reported_intent"],
                    "regulatory_or_legal_outcome": row["regulatory_or_legal_outcome"],
                    "qualification_basis": row["qualification_basis"],
                    "source_calibration_notes": row["notes"],
                },
                "partial",
                [
                    "reported_intent",
                    "regulatory_or_legal_outcome",
                    "qualification_basis",
                    "notes",
                ],
            ),
        }
    )

    mandatory = ["1", "2", "3", "4", "7", "10", "11"]
    non_direct = [
        item
        for item in mandatory
        if criteria[item]["status"] != "direct" or criteria[item]["value"] is None
    ]
    return {
        "criteria": criteria,
        "strict_mandatory_mapping": {
            "criterion_ids": [int(item) for item in mandatory],
            "complete": not non_direct,
            "missing_or_non_direct": [int(item) for item in non_direct],
            "note": "AAIO strict mapping is an internal quality signal, not an OECD submission-readiness determination.",
        },
    }


def aiid_alignment(row: dict[str, Any]) -> dict[str, Any]:
    aiid_id = str(row["aiid_id"]).strip()
    aiid_url = str(row["aiid_url"]).strip()
    existing_incident = None
    if aiid_id:
        existing_incident = {
            "incident_id": int(aiid_id),
            "url": aiid_url,
            "status": "cross_reference_only",
        }

    return {
        "existing_incident": existing_incident,
        "incident_title": {"value": row["title"], "status": "direct"},
        "description": {"value": row["summary"], "status": "direct"},
        "incident_date": {
            "value": row["incident_date"],
            "precision": row["date_precision"],
            "status": "partial",
        },
        "entities": {
            "developer": {"value": None, "status": "unmapped"},
            "deployer": {"value": None, "status": "unmapped"},
            "harmed_or_nearly_harmed_party_candidates": {
                "value": split_pipe(row["affected_parties"]),
                "status": "approximate",
                "note": "Candidate labels only; AAIO affected_parties is broader than AIID entity-role semantics.",
            },
        },
        "supporting_reports": {
            "value": sources(row),
            "status": "partial",
            "note": "AAIO source metadata is not a complete AIID report object.",
        },
        "taxonomy_annotations": {
            "value": None,
            "status": "unmapped",
            "note": "AAIO does not invent AIID taxonomy annotations.",
        },
    }


def build_record(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "aaio": {
            "incident_id": row["incident_id"],
            "title": row["title"],
            "incident_date": row["incident_date"],
            "date_precision": row["date_precision"],
            "primary_country": row["country"],
            "countries_affected": split_pipe(row["countries_affected"]),
            "region": row["region"],
            "sector": row["sector"],
            "system_type": row["system_type"],
            "ai_system_or_tool": row["ai_system_or_tool"],
            "incident_or_hazard": row["incident_or_hazard"],
            "harm_types": split_pipe(row["harm_types"]),
            "affected_parties": split_pipe(row["affected_parties"]),
            "summary": row["summary"],
            "reported_intent": row["reported_intent"],
            "response": row["response"],
            "regulatory_or_legal_outcome": row["regulatory_or_legal_outcome"],
            "severity": {
                "magnitude": row["magnitude"],
                "scale": row["scale"],
                "criticality": row["criticality"],
                "irreversibility": row["irreversibility"],
                "score": row["severity_score"],
                "band": row["severity_band"],
                "framework": "AAIO project rubric; not an OECD or AIID severity classification",
            },
            "provenance": {
                "evidence_confidence": row["evidence_confidence"],
                "qualification_basis": row["qualification_basis"],
                "source_calibration_notes": row["notes"],
                "last_verified": row["last_verified"],
                "curator": row["curator"],
                "sources": sources(row),
            },
        },
        "alignments": {
            "aiid_core": aiid_alignment(row),
            "oecd_common_reporting_framework": oecd_alignment(row),
        },
        "mapping_gaps": {
            "aiid_core": [
                "developer_entities",
                "deployer_entities",
                "taxonomy_annotations",
            ],
            "oecd_criteria_unmapped_or_non_direct": [
                3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            ],
            "aaio_fields_preserved_without_external_normalisation": [
                "evidence_confidence",
                "qualification_basis",
                "source_calibration_notes",
                "reported_intent",
                "regulatory_or_legal_outcome",
                "severity_score",
                "severity_band",
                "magnitude",
                "scale",
                "criticality",
                "irreversibility",
            ],
        },
    }


def build_export(source: Path, mapping_path: Path) -> dict[str, Any]:
    rows = read_rows(source)
    mapping = read_mapping(mapping_path)
    return {
        "export_format": "AAIO Interoperability Export",
        "export_schema_version": EXPORT_SCHEMA_VERSION,
        "mapping_version": mapping["mapping_version"],
        "disclaimer": "Semantic alignment only. This file is not an official AIID submission schema, OECD AIM ingest schema, or endorsement by AIID/OECD.",
        "source_dataset": {
            "name": "Africa AI Incident Observatory",
            "version": dataset_version(),
            "path": "data/incidents.csv",
            "sha256": sha256_bytes(source.read_bytes()),
            "record_count": len(rows),
            "last_verified_values": sorted({row["last_verified"] for row in rows}),
        },
        "mapping": {
            "path": "mapping/interoperability-map-v1.json",
            "sha256": sha256_bytes(mapping_path.read_bytes()),
            "references": mapping["references"],
            "status_definitions": mapping["status_definitions"],
        },
        "records": [build_record(row) for row in rows],
    }


def canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def write_export(
    payload: dict[str, Any], output: Path, sha_output: Path
) -> tuple[bytes, str]:
    data = canonical_json_bytes(payload)
    digest = sha256_bytes(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    sha_output.write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return data, digest


def check_export(payload: dict[str, Any], output: Path, sha_output: Path) -> bool:
    expected = canonical_json_bytes(payload)
    expected_digest = sha256_bytes(expected)
    if not output.exists() or not sha_output.exists():
        return False
    return (
        output.read_bytes() == expected
        and sha_output.read_text(encoding="utf-8").strip()
        == f"{expected_digest}  {output.name}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sha-output", type=Path, default=DEFAULT_SHA_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if committed export/hash are missing or stale",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_export(args.source, args.mapping)
    if args.check:
        if check_export(payload, args.output, args.sha_output):
            print(
                f"OK: interoperability export is current ({payload['source_dataset']['record_count']} records)."
            )
            return 0
        print(
            "ERROR: interoperability export or SHA-256 manifest is missing/stale. "
            "Run scripts/export_interoperability.py"
        )
        return 1

    data, digest = write_export(payload, args.output, args.sha_output)
    print(f"Wrote {payload['source_dataset']['record_count']} records to {args.output}")
    print(f"SHA256 {digest}")
    print(f"Bytes {len(data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
