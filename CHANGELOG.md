# Changelog

## 0.2.0 - 2026-09-15

### Added
- Two operational AI incidents promoted into the versioned core dataset, expanding coverage into Kenyan clinical decision support and South African professional legal research.
- Append-only `data/record_history.csv` for material record changes and promotion provenance.
- Explicit repository `VERSION` marker and release-consistency validation.
- Promotion traceability from `AAIO-OP-*` staging records to stable core incident IDs.
- Release and provenance policy covering semantic-style versioning, correction history, release gates and DOI archiving discipline.
- Public impact/adoption ledger and an AIID submission packet for original AAIO cases.
- Dashboard pipeline/provenance views and a direct incident-submission path.

### Changed
- Core dataset increased from 17 to 19 records while retaining 9 primary African countries.
- Operational evidence validation now checks promoted core IDs and release metadata.
- Dashboard version is read from the canonical `VERSION` file rather than hard-coded.
- CI now validates release metadata and material record history in addition to data, multilingual evidence, operational evidence, pytest and deterministic interoperability export generation.

### Research significance
- v0.2.0 moves AAIO beyond a synthetic-media-heavy seed by incorporating a peer-reviewed deployed-healthcare safety case and a direct judicial record of professional generative-AI failure.
- The release deliberately preserves the distinction between evidence strength, severity, candidate evidence and confirmed core incidents.

## 0.1.2 - 2026-09-09

### Added
- A source-led multilingual incident register with initial francophone, arabophone and lusophone African cases.
- Preservation of original-language source URLs and headlines alongside conservative English curator summaries.
- Explicit translation method, translation-uncertainty and AI-attribution-strength fields.
- A documented multilingual evidence and core-promotion protocol.
- Automated validation and tests requiring all three issue #2 language families, source provenance and translation calibration.

### Changed
- CI now validates multilingual evidence separately from the core incident dataset and interoperability export.

## 0.1.1 - 2026-09-09

### Added
- Versioned AIID/OECD semantic interoperability mapping covering all 29 OECD common-reporting criteria.
- Deterministic interoperability JSON export with embedded source/mapping SHA-256 hashes and a companion manifest.
- JSON Schema and tests for the interoperability export across all 17 v0.1.0 seed records.
- Explicit mapping-gap handling that preserves AAIO evidence confidence and source-calibration notes without fabricating external taxonomy values.

### Changed
- Expanded interoperability documentation with field-level mapping, limitations, provenance rules and non-equivalence safeguards.
- CI now smoke-tests interoperability export generation in addition to dataset validation and pytest.

## 0.1.0 - 2026-09-08

### Added
- 17 source-traceable seed incident records.
- Conservative watchlist for automated/algorithmic cases without sufficient AI attribution.
- Evidence-confidence and transparent severity rubrics.
- JSON Schema, deterministic validation and tests.
- Streamlit explorer and reproducible analysis script.
- Contributor, correction, ethics, security and interoperability documentation.
