# AIID submission packet for original AAIO operational cases

This document prepares two AAIO cases for manual upstream submission to the **AI Incident Database (AIID)**. It follows AIID editorial principles: concise titles, neutral descriptions, explicit location and harm, traceable reports, and cautious wording where causation is limited.

**Status:** prepared only. AAIO must not claim either case has been submitted to or accepted by AIID until that occurs and an external AIID identifier or queue record is verified.

## AAIO-0018 — Kenya clinical decision-support case

### Suggested incident title

**LLM Clinical Decision Support Produced Harmful Recommendations in Kenyan Primary-Care Clinics**

### Incident date

July 2024, with the evaluated deployment window running July–September 2024.

### Location

Kenya.

### AI system / deployment

EHR-embedded large-language-model clinical decision support used across 16 Penda Health primary-care clinics. The peer-reviewed study describes the system as AI Consult and evaluates LLM-generated clinical recommendations.

### Nature of harm

Clinical safety risk from actively harmful recommendations, including recommendations that were subsequently present in final clinical documentation.

### Neutral incident description

A retrospective physician review of 1,469 encounters involving an EHR-embedded LLM clinical decision-support system deployed across 16 Kenyan primary-care clinics identified 115 encounters (7.8%) containing actively harmful LLM recommendations. Sixty-seven harmful recommendations appeared in final clinical documentation. The same evaluation identified 50 hallucination encounters. The study documented unsafe recommendations and their adoption into documentation; it did **not** establish that 115 patients were injured.

### Primary reports

1. Nature Health — *Safety of a large language model-based clinical decision support system in African primary healthcare*  
   https://www.nature.com/articles/s44360-026-00082-5
2. PubMed — PMID 42272940  
   https://pubmed.ncbi.nlm.nih.gov/42272940/

### Follow-up context

A later pragmatic cluster-randomised trial should be treated as follow-up context rather than as a reason to erase the earlier incident evidence. It reported no serious adverse events judged related to the intervention and no statistically significant difference in the primary 14-day treatment-failure outcome.

### Claim boundary

Do not restate "115 harmful-recommendation encounters" as "115 injured patients." The source establishes unsafe outputs and some incorporation into documentation, not a patient-injury count.

---

## AAIO-0019 — South Africa legal-research case

### Suggested incident title

**South African Lawyers Relied on ChatGPT-Generated Fictitious Legal Authorities**

### Incident date

29 June 2023, using the judgment date for `Parker v Forsyth NNO and Others`.

### Location

South Africa.

### AI system / deployment

ChatGPT used for professional legal research.

### Nature of harm

Fabricated legal citations, professional-verification failure and burden on the administration of justice.

### Neutral incident description

In `Parker v Forsyth NNO and Others`, the plaintiff's legal team relied on legal research sourced through ChatGPT. The cited authorities could not be located, and the attorneys ultimately admitted they had not accessed or read them. The court criticised the lawyers' reliance on AI-generated legal research without adequate verification. Later South African High Court material in `Mavundla` discussed the Parker episode when addressing fictitious legal authorities and professional use of AI.

### Primary reports

1. LawLibrary — `Parker v Forsyth NNO and Others (1585/20) [2023] ZAGPRD 1`  
   https://lawlibrary.org.za/akn/za-gp/judgment/zagprd/2023/1/eng@2023-06-29
2. SAFLII — `Mavundla v MEC [2025] ZAKZPHC 2`  
   https://www.saflii.org/za/cases/ZAKZPHC/2025/2.html

### Claim boundary

Do not attribute every adverse litigation outcome to ChatGPT. The incident AAIO can directly support is the production and professional reliance on fictitious AI-generated authorities and the resulting verification/court-process burden.

---

## Upstream workflow

1. Search AIID immediately before submission to avoid creating a duplicate incident.
2. If no equivalent incident exists, submit the strongest primary report first and add corroborating reports separately where the AIID interface permits.
3. Preserve the claim boundaries above in any free-text description.
4. Record the submission date and public queue/incident identifier in `docs/impact.md` only after verification.
5. If AIID editors merge the report into an existing incident, record that existing AIID identifier rather than representing AAIO as the origin of a new AIID incident.
