# Operational AI incident coverage

## Purpose

AAIO's original seed was visibly concentrated in synthetic media, information integrity and public-facing generative-AI failures. The operational workstream tests whether the same evidence discipline can identify realised AI harms in settings where failures are less visible.

This workstream does **not** lower the core inclusion threshold. It preserves a reviewable operational register even after qualifying records are promoted into `data/incidents.csv`.

## Promotion standard

An operational record may be marked `eligible_for_core` only when all five conditions are met:

1. a credible source establishes AI involvement rather than merely automation, digitisation or biometrics;
2. the source documents a realised adverse output, event or material effect rather than a hypothetical risk;
3. the event has a material African nexus;
4. at least one traceable public source supports the record, with primary or peer-reviewed evidence preferred;
5. AAIO wording does not upgrade evidence beyond what the source establishes.

When an eligible record is promoted, its operational ID is retained and `core_promotion_status` becomes `promoted_to_core`. The staging record then records both the stable `promoted_core_id` and `promoted_in_release`. This prevents the evidence-review history from disappearing once a case enters the core dataset.

## v0.2.0 promotions

### AAIO-OP-0001 → AAIO-0018 — Kenya — clinical decision support

A peer-reviewed 2026 Nature Health evaluation reviewed 1,469 records from an EHR-embedded LLM clinical decision-support system deployed in 16 Kenyan primary-care clinics between July and September 2024. Physician reviewers identified actively harmful LLM recommendations in 115 encounters (7.8%); 67 harmful recommendations appeared in final documentation. The paper separately reports 50 hallucination encounters.

AAIO deliberately does **not** translate those unsafe outputs into a claim that 115 patients were injured. The study measures recommendation safety and documentation adoption, not 115 proven patient injuries. A later pragmatic trial of the intervention reported no serious adverse events judged related to the intervention and no statistically significant difference in its primary treatment-failure outcome. Both findings can be true and are retained as context.

Sources:
- Nature Health: https://www.nature.com/articles/s44360-026-00082-5
- PubMed: https://pubmed.ncbi.nlm.nih.gov/42272940/
- Later Nature Medicine trial: https://www.nature.com/articles/s41591-026-04503-6

### AAIO-OP-0002 → AAIO-0019 — South Africa — professional legal research

In *Parker v Forsyth NNO and Others*, South African lawyers relied on legal authorities sourced through ChatGPT that could not be verified. Later South African High Court authority in *Mavundla* recounts that the attorneys admitted they had neither accessed nor read the cases and that the references had been sourced from ChatGPT. The failure therefore has a direct AI linkage and a realised professional/court-process effect.

AAIO does not claim that ChatGPT caused every adverse result in the underlying litigation. The incident is narrowly defined as professional reliance on fictitious AI-generated authorities without verification.

Sources:
- LawLibrary judicial record: https://lawlibrary.org.za/akn/za-gp/judgment/zagprd/2023/1/eng@2023-06-29
- SAFLII, *Mavundla*: https://www.saflii.org/za/cases/ZAKZPHC/2025/2.html

## Sectors researched but not promoted in this pass

The research pass also searched for African cases in credit/financial decisioning, employment/recruitment, education and public-service delivery. Public reporting frequently described **risk**, adoption, automation, biometrics, or algorithmic decision-making without enough evidence to establish both AI involvement and a realised adverse effect attributable to the system.

Those leads are not converted into core incidents merely to satisfy sector quotas. In particular:

- an automated decision or biometric verification system is not assumed to be AI;
- evidence of model bias in a benchmark is not automatically a deployed incident;
- a complaint about possible discrimination is not converted into a confirmed AI-caused harm without supporting evidence;
- a beneficial or neutral deployment is not re-labelled as an incident;
- lack of public evidence is recorded as a visibility gap, not as evidence that the sector has no AI incidents.

This negative-result discipline is part of AAIO's methodology. Operational coverage should become broader as stronger public evidence emerges, but not less defensible.

## Relationship to other AAIO workstreams

This file is intentionally distinct from:

- `data/multilingual_incidents.csv`, which addresses language discovery and translation provenance;
- `mapping/interoperability-map-v1.json` and `scripts/export_interoperability.py`, which address semantic interoperability with external incident frameworks;
- `data/watchlist.csv`, which holds relevant cases that do not currently establish the AI linkage required for core inclusion;
- `data/record_history.csv`, which records material changes once a case becomes part of the versioned core dataset.

Operational staging, core promotion and record history together create an auditable path from **candidate evidence → reviewed case → versioned incident**.
