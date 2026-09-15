# Interactive dashboard

AAIO includes a Streamlit research dashboard in `app.py`.

## What the dashboard is for

The dashboard is designed for **evidence exploration, provenance and research reuse**, not prevalence ranking. It provides:

- country, sector, year, severity and evidence-confidence filters;
- an Africa map showing where current core records are documented;
- timelines and sector distributions;
- record-level source inspection;
- conditional AIID links so original AAIO records are not given fictitious upstream identifiers;
- a separate evidence-quality view;
- a **Pipeline & provenance** view showing operational staging, multilingual evidence candidates and material record history;
- a conservative watchlist for cases excluded because AI attribution is not sufficiently established;
- CSV export of filtered core records;
- a direct link to the structured community incident-submission form;
- links to methodology, release policy and source evidence;
- a working filter reset that clears Streamlit widget state rather than only rerunning the page.

The displayed dataset version is read from the repository-root `VERSION` file, preventing the dashboard banner from drifting away from citation and release metadata.

A country with fewer records should never be interpreted as having fewer AI harms. The dataset reflects public visibility, language, source availability, sector transparency and curator coverage.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/validate_release.py
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Connect a Streamlit Community Cloud account to GitHub.
2. Select the repository `Briella009/Africa-AI-Incident-Observatory`.
3. Use branch `main`.
4. Set the entrypoint to `app.py`.
5. Deploy publicly if the dashboard is intended for research/community use.

No secrets or external API keys are required.

## Visual design

The interface intentionally uses a restrained editorial palette and avoids decorative AI imagery. The goal is to resemble a research/public-interest data product rather than a generic AI demo.
