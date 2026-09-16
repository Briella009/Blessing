# AAIO release and provenance policy

AAIO treats dataset releases as research artifacts, not rolling spreadsheets. The goal is to make every published version inspectable, reproducible and citable.

## Versioning

AAIO uses semantic-style dataset versions:

- **MAJOR** — a breaking change to the incident model, inclusion threshold or interpretation of core fields.
- **MINOR** — new core incidents, new evidence layers, substantial interoperability or dashboard capabilities, or material methodology extensions.
- **PATCH** — corrections, source refreshes, wording calibration, metadata fixes and non-breaking tooling changes.

The repository-root `VERSION` file is the canonical human-readable version marker. `CITATION.cff`, the changelog and dashboard must agree with it before a release is considered ready.

## Release gates

A release is ready only when all of the following are true:

1. `python scripts/validate.py` passes for the core dataset.
2. Multilingual and operational staging validators pass.
3. The full pytest suite passes.
4. The deterministic interoperability export can be regenerated.
5. Core records retain traceable public evidence and calibrated uncertainty.
6. Material record changes are entered in `data/record_history.csv`.
7. Version metadata is synchronized across `VERSION`, `CITATION.cff`, `CHANGELOG.md` and the dashboard.

## Promotion from evidence layers

Candidate records may live outside `data/incidents.csv` while evidence is still being evaluated. Promotion into the core dataset requires:

- credible AI linkage;
- a realised incident or material adverse effect;
- a material African nexus;
- traceable public evidence;
- calibrated language that does not exceed what the sources establish; and
- evidence confidence A or B unless an explicit release note explains an exception.

When a staged operational record is promoted, the staging record keeps its original `AAIO-OP-*` identifier and receives a `promoted_core_id` plus `promoted_in_release`. This preserves review history rather than erasing the pre-release evidence trail.

## Corrections and record history

AAIO does not silently rewrite material facts. Material changes should be appended to `data/record_history.csv`, including the affected incident ID, release, change type, fields affected, a concise reason and a supporting evidence URL where available.

Typographical changes that do not alter meaning do not require a history entry.

## Persistent citation and archiving

`CITATION.cff` provides repository-level citation metadata. AAIO should also archive stable releases in a DOI-minting research repository such as Zenodo. A DOI must not be added to AAIO metadata until it has actually been minted and verified.

For DOI-backed releases, preserve both:

- the concept-level DOI for the evolving project, when available; and
- the version-specific DOI for the cited dataset release.

## Generated exports

Generated interoperability files are derived artifacts and are intentionally not treated as the source of truth. They must be reproducible from committed source data and mapping files. Release notes should publish or attach generated exports only after validation against the release commit.

## Claim discipline

Release metadata must not imply that AAIO is comprehensive, representative of incident prevalence, endorsed by AIID/OECD/NIST/African Union, or evidence that countries missing from the dataset experience no AI harms.
