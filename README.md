# Africa AI Incident Observatory

**A source-traceable, open dataset for documenting AI incidents affecting African people, institutions and information environments.**

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://aaio-africa.streamlit.app/)
[![Validate data](https://github.com/Briella009/Africa-AI-Incident-Observatory/actions/workflows/validate-data.yml/badge.svg)](https://github.com/Briella009/Africa-AI-Incident-Observatory/actions/workflows/validate-data.yml)
![Records](https://img.shields.io/badge/verified%20core%20records-19-0f766e)
![Version](https://img.shields.io/badge/dataset-v0.2.0-516b78)
![License](https://img.shields.io/badge/code-MIT-blue)
![Data](https://img.shields.io/badge/data-CC%20BY%204.0-green)

**Live dashboard:** https://aaio-africa.streamlit.app/

**Dataset version:** v0.2.0 · 19 curated core records · 9 primary African countries · multilingual evidence layer · operational evidence provenance

## Why this exists

AI failures become useful public evidence only when they are documented consistently enough to compare, audit and learn from.

In August 2026, the AI Incident Database reported that, from February 2020 through July 2026, African incidents represented roughly **1.3% of records in the OECD AI Incidents and Hazards Monitor and 4.2% of records in AIID**. AIID argued that this reflects a structural visibility and reporting problem rather than evidence that Africa experiences unusually few AI harms.

The **Africa AI Incident Observatory (AAIO)** is an independent, open-data response to that gap. It turns scattered public reports into structured incident records while preserving uncertainty, provenance and links back to the evidence.

> **This is not an official AIID, OECD, NIST, African Union or government project.** AAIO is an independent research and public-interest technology project. It links to those resources where relevant and does not claim their endorsement.

## What changed in v0.2.0

AAIO now moves beyond a synthetic-media-heavy seed dataset. Two independently sourced operational failures were promoted into the core dataset:

- **Kenya / clinical decision support:** a peer-reviewed evaluation of an EHR-embedded LLM across 16 primary-care clinics documented actively harmful recommendations while preserving the distinction between unsafe output and proven patient injury.
- **South Africa / legal services:** judicial material documented professional reliance on fictitious legal authorities sourced through ChatGPT without adequate verification.

The release also adds an append-only material-change ledger, explicit operational-to-core promotion provenance, synchronized version metadata, release-integrity validation, and a dashboard view for evidence still moving through the research pipeline.

## Research foundation

- [AI Incident Database: Strengthening AI Incident Monitoring and Reporting in Africa for Global AI Safety](https://incidentdatabase.ai/blog/strengthening-ai-incident-monitoring-and-reporting-in-africa-for-global-ai-safety/)
- [OECD: Towards a common reporting framework for AI incidents](https://www.oecd.org/en/publications/towards-a-common-reporting-framework-for-ai-incidents_f326d4ac-en.html)
- [OECD AI Incidents and Hazards Monitor methodology](https://oecd.ai/en/incidents-methodology)
- [NIST AI Risk Management Framework / AIRC](https://airc.nist.gov/airmf-resources/airmf/)
- [African Union Continental Artificial Intelligence Strategy](https://au.int/en/documents/20240809/continental-artificial-intelligence-strategy)

## Explore the live dashboard

The Streamlit explorer lets readers filter the core dataset by country, year, sector, severity and evidence confidence; inspect individual records; compare evidence quality; review the conservative watchlist; inspect multilingual and operational evidence pipelines; review material record history; and download filtered data.

[Open the live Africa AI Incident Observatory dashboard](https://aaio-africa.streamlit.app/)

## What is in the repository

- `data/incidents.csv` — versioned core records that meet the inclusion threshold
- `data/multilingual_incidents.csv` — source-led French-, Arabic- and Portuguese-language evidence candidates with translation uncertainty preserved
- `data/operational_incidents.csv` — operational incident review layer with promotion status and core-ID traceability
- `data/watchlist.csv` — important automated/algorithmic cases excluded because AI causation is not sufficiently established
- `data/record_history.csv` — append-only ledger for material record changes and promotions
- `schema/incident.schema.json` — machine-readable core record schema
- `mapping/interoperability-map-v1.json` — versioned semantic mapping to AIID/OECD concepts
- `scripts/export_interoperability.py` — deterministic interoperability export with provenance hashes
- `scripts/validate.py` — deterministic core dataset validator
- `scripts/validate_multilingual.py` — multilingual evidence validator
- `scripts/validate_operational.py` — operational evidence and promotion validator
- `scripts/validate_release.py` — version, citation, promotion and history consistency checks
- `docs/methodology.md` — inclusion, exclusion and verification methodology
- `docs/severity-and-confidence.md` — transparent severity and evidence-confidence rubric
- `docs/interoperability.md` — field-level AIID/OECD interoperability notes and non-equivalence safeguards
- `docs/multilingual-evidence.md` — multilingual discovery and translation-calibration protocol
- `docs/operational-coverage.md` — operational coverage expansion and negative-result discipline
- `docs/release-policy.md` — versioning, provenance, corrections and DOI discipline
- `docs/impact.md` — independently verifiable adoption, reuse and citation ledger
- `docs/aiid-submission-packet.md` — prepared upstream submission notes for original AAIO operational cases
- `app.py` — interactive Streamlit explorer
- `.github/ISSUE_TEMPLATE/incident_submission.yml` — structured community incident submission template

## Core dataset

v0.2.0 contains **19 source-traceable core records** spanning misinformation, influence operations, health misinformation, financial scams, conflict information, model behaviour, government-policy integrity, clinical decision support and professional legal research.

It is intentionally **not comprehensive or prevalence-weighted**. The absence of a record for a country does **not** mean that no incident occurred. It means only that no qualifying record has yet been included in the current core dataset.

### Primary countries represented

Nigeria, Zambia, Kenya, Ghana, Tanzania, Rwanda, Burkina Faso, South Africa and Sudan. Some incidents have cross-border effects.

## Inclusion rule

A core record must satisfy all of the following:

1. **AI linkage** — a credible source connects the event to an AI system, model, AI-generated content or AI-enabled deployment.
2. **Realised event** — the record documents an incident, not only a hypothetical risk.
3. **African nexus** — the event materially affects an African country, population, institution or information environment.
4. **Traceable evidence** — at least one credible, publicly reviewable source is available.
5. **Calibrated language** — uncertain claims remain labelled as alleged, purported, reported, believed or unverified where appropriate.

Cases relevant to automated decision-making but failing the AI-linkage threshold remain in the **watchlist**, not silently promoted to AI incidents.

## Evidence confidence

| Grade | Meaning |
|---|---|
| A | Strong evidence: primary/official evidence, direct admission, court record, peer-reviewed deployment evidence, or strong independent corroboration |
| B | Good evidence: credible independent reporting/fact-checking with direct technical or documentary support |
| C | Limited but credible: one strong source or material attribution uncertainty; wording must preserve uncertainty |
| D | Unverified/disputed: excluded from the core dataset |

Confidence measures **evidence quality**, not incident severity.

## Severity

AAIO uses a transparent project rubric based on four dimensions scored 0-4:

- magnitude of harm — 35%
- scale of exposure/affected population — 25%
- criticality (health, safety, rights, democracy, critical services) — 25%
- difficulty of reversal/remediation — 15%

The score is a **research aid, not an official legal or regulatory rating**. See `docs/severity-and-confidence.md`.

## Reproducibility and release integrity

AAIO treats releases as research artifacts rather than a continuously overwritten spreadsheet. v0.2.0 introduces a canonical `VERSION` file, material-change history and release consistency checks.

Run the full local validation path:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/validate.py
python scripts/validate_multilingual.py
python scripts/validate_operational.py
python scripts/validate_release.py
pytest -q
python scripts/export_interoperability.py --output /tmp/aaio-interoperability-v1.json --sha-output /tmp/aaio-interoperability-v1.sha256
streamlit run app.py
```

## Contribute an incident

Use the [structured Incident submission form](https://github.com/Briella009/Africa-AI-Incident-Observatory/issues/new?template=incident_submission.yml) and provide the source links and evidence requested by the template. Submissions are reviewed against the same inclusion criteria as existing records.

Please do **not** submit private personal data, leaked credentials, graphic abuse material, operational instructions that enable wrongdoing, or allegations without evidence.

## Relationship to existing incident work

AAIO is designed to complement, not duplicate, global incident infrastructure. The project now includes explicit semantic interoperability work for all 29 criteria in the OECD common reporting framework while preserving AAIO-specific evidence-confidence and source-calibration data.

Where a core record is already indexed by AIID, its AIID identifier is preserved for traceability. Original AAIO cases can be prepared for upstream submission without fabricating an AIID identifier before one exists.

## Citation

Please cite the repository using `CITATION.cff`. AAIO does not claim a DOI until one has actually been minted and verified for a stable release.

## Author

**Blessing Ezeobioha**  
Cybersecurity practitioner and AI researcher working on threat intelligence, AI governance and responsible technology in African contexts.

- GitHub: [@Briella009](https://github.com/Briella009)
- ORCID: [0009-0005-9972-9380](https://orcid.org/0009-0005-9972-9380)
- LinkedIn: [Blessing Ezeobioha](https://www.linkedin.com/in/blessing-ezeobioha-)

## Status

**v0.2.0 research release.** The dataset will evolve as sources are corrected, incidents are added, multilingual evidence is promoted, or classifications are re-evaluated. Material changes are recorded in `data/record_history.csv`; release-level changes are recorded in `CHANGELOG.md`.
