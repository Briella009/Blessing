# Methodology

## 1. Purpose

AAIO is a public-interest evidence layer for AI incidents with an African nexus. It is designed to make cases comparable without overstating what the sources prove.

The project follows a conservative rule: **when AI involvement is unclear, exclude the case from the core dataset and document it in the watchlist instead.**

## 2. Conceptual basis

The methodology is informed by:

- OECD AI Incidents and Hazards Monitor definitions and common-reporting work;
- AI Incident Database incident records and research on collective incident memory; and
- NIST AI Risk Management Framework incident-response, monitoring and documentation practices.

AAIO does not reproduce or claim ownership of those taxonomies. It keeps its core schema small enough for journalists, researchers, civil-society organisations and practitioners to inspect without specialist tooling, while maintaining a separate semantic interoperability layer.

## 3. Core incident definition

For AAIO, a core incident is a publicly documented event in which the development, deployment, use, misuse or malfunction of an AI system is credibly linked to realised harm or a material adverse effect affecting an African person, community, institution, market, public service, information environment or country.

A case is included only when all five criteria below are satisfied.

### 3.1 AI linkage
A source must establish a credible connection to an AI system or AI-generated output. Marketing language, automation alone or speculation is insufficient.

### 3.2 Realised event
There must be an event or material adverse output that actually occurred. Purely hypothetical hazards belong in future hazard research, not the core incident table.

### 3.3 African nexus
At least one African country, population, institution or information environment must be materially affected.

### 3.4 Traceable evidence
At least one source must be publicly reviewable and credible. Primary, judicial, regulatory, peer-reviewed or independently corroborated evidence is preferred. A single social-media allegation without corroboration is insufficient.

### 3.5 Calibrated wording
The record may not state as fact what the source states only as allegation. Terms such as `reported`, `purported`, `believed`, `alleged`, `probable` and `uncertain` are preserved when required.

## 4. Evidence confidence is separate from severity

AAIO assigns an evidence-confidence grade and a separate project severity score. These answer different questions:

- **evidence confidence** asks how strongly the public evidence supports the incident record;
- **severity** is a transparent research aid describing magnitude, scale, criticality and difficulty of reversal.

A serious allegation with weak evidence must not become a high-confidence fact merely because the alleged harm would be severe.

## 5. Exclusions and staging

AAIO excludes from the core table:

- ordinary software or automated decision failures where AI involvement is not established;
- hypothetical risks with no realised event;
- unattributed social-media claims that lack credible verification;
- duplicated reports of the same underlying event;
- claims whose only support is an AI-content detector score with no corroborating evidence; and
- private or non-public information that cannot be safely reviewed.

Important excluded cases may be placed in `data/watchlist.csv` with an explicit reason.

Evidence may also be reviewed in dedicated staging layers before promotion. `data/multilingual_incidents.csv` preserves original-language discovery and translation uncertainty. `data/operational_incidents.csv` preserves the review path for operational failures and, after promotion, records the stable core ID and release in which promotion occurred.

## 6. Source hierarchy

Preferred evidence order:

1. court judgments, regulator findings, official incident notices and direct developer/company admissions;
2. peer-reviewed or methodologically transparent deployment research;
3. independent investigative journalism and specialist fact-checking;
4. reputable incident databases that preserve source provenance; and
5. other credible public reporting.

A source is never treated as infallible. Conflicts are recorded and wording is narrowed to the strongest supportable claim.

## 7. Deduplication

Records are deduplicated by the underlying event, not by article URL. Multiple reports about the same event remain sources on one record unless materially distinct harms or deployments justify separate incidents.

Upstream identifiers are cross-references rather than ownership claims. If an original AAIO incident later appears in AIID or another external database, AAIO records the verified identifier rather than retroactively implying that the external database originated the AAIO record.

## 8. Dates and verification

`incident_date` represents the earliest reasonably supported date of occurrence, circulation or deployment-related event, not necessarily the publication date of a fact-check or study. `date_precision` indicates whether the date is exact, month-level or approximate.

`last_verified` records when AAIO most recently checked the evidence supporting that record. It should change when a material evidence review occurs, not merely because the repository was edited.

## 9. Updates, corrections and version history

AAIO does not silently rewrite material facts. A substantive correction or reclassification should:

1. update the source-backed record;
2. update `last_verified` when the supporting evidence has been re-reviewed;
3. append a material-change entry to `data/record_history.csv`;
4. update release-level notes in `CHANGELOG.md` when appropriate; and
5. preserve uncertainty rather than resolving disputed facts without stronger evidence.

Typographical edits that do not alter meaning do not require a material-history entry.

Release metadata is governed by `docs/release-policy.md`. The root `VERSION`, `CITATION.cff`, README and changelog must remain synchronized for a versioned release.

## 10. What absence means

Country-, language- or sector-level absence is **not evidence of safety**. It can reflect monitoring gaps, language coverage, media access, reporting incentives, litigation visibility, sector secrecy, database coverage or curator capacity.

AAIO therefore treats documentation bias as part of the research problem. Record counts should not be interpreted as national prevalence rankings.
