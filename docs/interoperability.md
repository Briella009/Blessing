# Interoperability

AAIO provides a **semantic interoperability layer** for two widely used AI-incident ecosystems:

- the [AI Incident Database (AIID)](https://incidentdatabase.ai/), including its editor-defined incident concepts and external incident identifiers; and
- the [OECD common reporting framework for AI incidents](https://www.oecd.org/en/publications/towards-a-common-reporting-framework-for-ai-incidents_f326d4ac-en.html), which defines 29 reporting criteria for interoperable incident reporting.

The export is intentionally conservative. It does **not** claim to be an official AIID submission schema, an OECD AIM ingestion format, a conformity assessment, or an endorsement by either organisation.

## Why semantic alignment instead of schema mimicry

AIID and OECD serve related but different purposes. AAIO maps only what its source data actually supports. When two fields are related but not semantically equivalent, the export preserves the AAIO value as `raw_aaio_value` and marks the target field `approximate` or `unmapped` rather than inventing a normalized value.

The machine-readable mapping is maintained in [`mapping/interoperability-map-v1.json`](../mapping/interoperability-map-v1.json).

## Alignment-status vocabulary

| Status | Meaning |
|---|---|
| `direct` | AAIO captures substantially the same concept and can transfer it without semantic inference. |
| `partial` | AAIO captures only part of the target concept or lacks target subfields. |
| `approximate` | AAIO has related information, but target semantics or controlled vocabulary differ. |
| `unmapped` | AAIO does not currently capture the target concept in a defensible structured field. |
| `cross_reference_only` | AAIO stores an external identifier/URL but does not reproduce the external record schema. |

## AIID alignment and original AAIO incidents

AAIO preserves an AIID identifier only when a core incident has already been matched to an existing AIID incident. It does **not** fabricate an AIID number for original AAIO records.

In v0.2.0, `AAIO-0018` and `AAIO-0019` have no AIID identifier in the core dataset. Their interoperability export therefore sets `existing_incident` to `null` while still exporting their AAIO title, description, date, affected-party candidates, supporting reports and evidence provenance. This makes the absence of an upstream identifier explicit and machine-readable.

| AIID concept | AAIO field(s) | Status | Export behaviour |
|---|---|---|---|
| Existing incident number | `aiid_id`, `aiid_url` | `cross_reference_only` when present | Preserved only for already matched AIID incidents; otherwise `null`. |
| Incident title | `title` | `direct` | Preserved without claiming AIID editor approval. |
| Description | `summary` | `direct` | Preserved as AAIO's source-calibrated synopsis. |
| Incident date | `incident_date`, `date_precision` | `partial` | Date and explicit precision are preserved. |
| Developer entities | none | `unmapped` | No entity is inferred from narrative text. |
| Deployer entities | none | `unmapped` | No entity is inferred from narrative text. |
| Harmed/nearly harmed parties | `affected_parties` | `approximate` | Exported as candidate labels, not normalized AIID entity tags. |
| Supporting reports | source fields | `partial` | Source name, URL and type are preserved, but AAIO does not construct full AIID report objects. |
| AIID taxonomy annotations | none | `unmapped` | AAIO does not fabricate AIID taxonomy labels. |

## OECD common reporting framework alignment

OECD's common reporting framework contains **29 criteria**. The mapping covers all 29. Seven are identified as mandatory in the framework: **1, 2, 3, 4, 7, 10 and 11**.

`strict_mandatory_mapping` is an **AAIO internal quality signal only**. It reports whether those seven criteria are available as direct, non-null mappings. It must not be interpreted as an OECD submission-readiness or compliance determination.

Key non-equivalences are deliberately preserved:

- AAIO severity fields are **not** converted into OECD criterion 10 severity values.
- AAIO `harm_types` remain raw descriptors rather than silently becoming OECD controlled values.
- AAIO `affected_parties` remain candidate labels rather than normalized stakeholder categories.
- AAIO `sector` is not treated as an ISIC classification.
- AAIO `system_type` is descriptive and is not converted into an OECD task taxonomy.
- Free-text response information is preserved without inferring prevention, mitigation, remediation or cessation categories.

## Deterministic export contract

Generate the interoperability artifact with:

```bash
python scripts/export_interoperability.py
```

By default this writes:

- `exports/aaio-interoperability-v1.json`
- `exports/aaio-interoperability-v1.sha256`

The export is deterministic for the same input bytes, project version and mapping version:

1. records are sorted by `incident_id`;
2. JSON object keys are sorted;
3. UTF-8 and a fixed pretty-print representation are used;
4. no runtime timestamp is embedded;
5. SHA-256 hashes of `data/incidents.csv` and the mapping file are embedded; and
6. a SHA-256 manifest is written alongside the export.

The export reads the current dataset version from the repository-root `VERSION` file. This prevents the interoperability artifact from silently reporting an old dataset version after a release changes.

Generated export artifacts are intentionally **not committed as the source of truth**. `data/incidents.csv`, `VERSION`, and the mapping file remain authoritative inputs. Release artifacts may be generated from a validated release commit.

## Preserved AAIO provenance

Every exported record keeps the AAIO evidence layer even when an external field cannot be normalized:

- `evidence_confidence`
- `qualification_basis`
- `source_calibration_notes`
- `last_verified`
- `curator`
- primary and secondary source name, URL and source type
- AAIO severity dimensions, score and band, explicitly labelled as an AAIO project rubric

This makes the export auditable: a consumer can distinguish **what AAIO observed** from **what the interoperability layer could safely map**.

## Validation and tests

Run:

```bash
python scripts/validate.py
python scripts/validate_operational.py
python scripts/validate_release.py
pytest -q
```

The interoperability tests verify that:

- all 29 OECD criteria and the seven mandatory criteria are represented;
- key AIID concepts are mapped or explicitly marked unmapped;
- the export is byte-deterministic;
- the SHA-256 manifest matches the generated file;
- all **19 v0.2.0 core records** are exported;
- the export version matches the canonical `VERSION` file;
- evidence-confidence and source-calibration fields survive unchanged;
- existing AIID IDs are preserved while original AAIO records retain `null` upstream references;
- AIID developer/deployer/taxonomy fields are not fabricated;
- non-equivalent OECD fields remain `null` with explicit mapping status; and
- source/mapping SHA-256 values are embedded in the export.

## What this does not claim

AAIO interoperability output is **not**:

- an official AIID bulk-import or submission format;
- an OECD AIM ingestion schema;
- proof that an incident satisfies every OECD reporting criterion;
- an automatic AIID taxonomy classifier;
- an ISIC classifier;
- an OECD or AIID severity conversion; or
- evidence of endorsement, affiliation or certification.

## External references

- OECD (2025), *Towards a common reporting framework for AI incidents*: https://www.oecd.org/en/publications/towards-a-common-reporting-framework-for-ai-incidents_f326d4ac-en.html
- OECD AIM methodology: https://oecd.ai/en/incidents-methodology
- AI Incident Database Editor's Guide: https://incidentdatabase.ai/editors-guide/
- AI Incident Database taxonomies: https://incidentdatabase.ai/taxonomies/
