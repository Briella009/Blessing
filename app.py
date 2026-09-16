from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "incidents.csv"
WATCHLIST = ROOT / "data" / "watchlist.csv"
MULTILINGUAL = ROOT / "data" / "multilingual_incidents.csv"
OPERATIONAL = ROOT / "data" / "operational_incidents.csv"
HISTORY = ROOT / "data" / "record_history.csv"
VERSION_FILE = ROOT / "VERSION"
REPO = "https://github.com/Briella009/Africa-AI-Incident-Observatory"
SUBMIT = f"{REPO}/issues/new?template=incident_submission.yml"

st.set_page_config(
    page_title="Africa AI Incident Observatory",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      :root {
        --ink: #14242c;
        --muted: #5f6b70;
        --paper: #f7f5ef;
        --line: #dedbd2;
        --teal: #1d625d;
        --gold: #b88234;
      }
      .stApp { background: var(--paper); color: var(--ink); }
      .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1450px; }
      h1, h2, h3 { color: var(--ink); letter-spacing: -0.02em; }
      h1 { font-size: 3rem !important; line-height: 1.02 !important; }
      [data-testid="stMetric"] {
        background: white;
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 14px 16px;
      }
      [data-testid="stMetricLabel"] { color: var(--muted); }
      [data-testid="stSidebar"] { background: #efede7; border-right: 1px solid var(--line); }
      .aaio-kicker { font-size: 0.78rem; letter-spacing: .14em; text-transform: uppercase; color: var(--teal); font-weight: 700; }
      .aaio-deck { max-width: 950px; font-size: 1.12rem; color: var(--muted); line-height: 1.65; margin: .4rem 0 1.3rem 0; }
      .aaio-note { background: white; border-left: 4px solid var(--gold); padding: 14px 18px; border-radius: 6px; margin: 1rem 0; }
      .aaio-small { color: var(--muted); font-size: .88rem; }
      div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    incidents = pd.read_csv(DATA)
    watch = pd.read_csv(WATCHLIST)
    multilingual = pd.read_csv(MULTILINGUAL)
    operational = pd.read_csv(OPERATIONAL)
    history = pd.read_csv(HISTORY)
    incidents["incident_date"] = pd.to_datetime(incidents["incident_date"], errors="coerce")
    incidents["year"] = incidents["incident_date"].dt.year.astype("Int64")
    return incidents, watch, multilingual, operational, history


def clear_filters():
    for key in (
        "filter_countries",
        "filter_sectors",
        "filter_years",
        "filter_confidence",
        "filter_severity",
        "filter_query",
    ):
        st.session_state.pop(key, None)


df, watch, multilingual, operational, history = load_data()
version = VERSION_FILE.read_text(encoding="utf-8").strip()

st.markdown(f'<div class="aaio-kicker">AAIO · Dataset v{version}</div>', unsafe_allow_html=True)
st.title("Africa AI Incident Observatory")
st.markdown(
    '<div class="aaio-deck">A source-traceable research dashboard for documented AI incidents affecting African people, institutions and information environments. The aim is not to count every failure. It is to make the evidence that does exist easier to inspect, challenge and reuse.</div>',
    unsafe_allow_html=True,
)

b1, b2, b3, _ = st.columns([1.2, 1.2, 1.2, 4.4])
with b1:
    st.link_button("View repository", REPO, use_container_width=True)
with b2:
    st.link_button("Read methodology", f"{REPO}/blob/main/docs/methodology.md", use_container_width=True)
with b3:
    st.link_button("Submit an incident", SUBMIT, use_container_width=True)

st.markdown(
    """
    <div class="aaio-note"><strong>Why this matters:</strong> AIID reported that African incidents represented roughly <strong>1.3%</strong> of incidents in the OECD AIM and <strong>4.2%</strong> of AIID records between February 2020 and July 2026. AAIO treats that as a visibility problem to investigate, not evidence that Africa has fewer AI harms.</div>
    """,
    unsafe_allow_html=True,
)

# Sidebar filters
st.sidebar.markdown("## Explore the evidence")
st.sidebar.caption("Filters change the core-dataset charts and explorer.")

countries = st.sidebar.multiselect(
    "Primary country", sorted(df["country"].dropna().unique()), key="filter_countries"
)
sectors = st.sidebar.multiselect(
    "Sector", sorted(df["sector"].dropna().unique()), key="filter_sectors"
)
years = st.sidebar.multiselect(
    "Year", sorted(df["year"].dropna().astype(int).unique()), key="filter_years"
)
confidence = st.sidebar.multiselect(
    "Evidence confidence", ["A", "B", "C"], key="filter_confidence"
)
severity = st.sidebar.multiselect(
    "Severity band",
    ["Low", "Limited", "Moderate", "High", "Critical"],
    key="filter_severity",
)
query = st.sidebar.text_input("Search title or summary", key="filter_query")
st.sidebar.button("Reset filters", use_container_width=True, on_click=clear_filters)

f = df.copy()
if countries:
    f = f[f["country"].isin(countries)]
if sectors:
    f = f[f["sector"].isin(sectors)]
if years:
    f = f[f["year"].isin(years)]
if confidence:
    f = f[f["evidence_confidence"].isin(confidence)]
if severity:
    f = f[f["severity_band"].isin(severity)]
if query:
    q = query.strip()
    mask = (
        f["title"].fillna("").str.contains(q, case=False, regex=False)
        | f["summary"].fillna("").str.contains(q, case=False, regex=False)
        | f["harm_types"].fillna("").str.contains(q, case=False, regex=False)
    )
    f = f[mask]

high_critical = int(f["severity_band"].isin(["High", "Critical"]).sum())
ab_evidence = int(f["evidence_confidence"].isin(["A", "B"]).sum())

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Core records", len(f), help="Core records matching the current filters")
m2.metric("Primary countries", f["country"].nunique())
m3.metric("Sectors", f["sector"].nunique())
m4.metric("High / critical", high_critical)
m5.metric("A/B evidence", ab_evidence)

st.caption(
    f"Showing {len(f)} of {len(df)} v{version} core records. "
    f"The watchlist contains {len(watch)} technology-governance cases excluded because AI attribution is not sufficiently established."
)

tab_overview, tab_explorer, tab_evidence, tab_pipeline, tab_watchlist, tab_method = st.tabs(
    [
        "Snapshot",
        "Incident explorer",
        "Evidence quality",
        "Pipeline & provenance",
        "Watchlist",
        "Methodology",
    ]
)

with tab_overview:
    st.subheader("What is visible in the current core dataset")
    st.caption("Record counts show documentation visibility in this dataset, not national prevalence of AI harm.")

    left, right = st.columns([1.15, 1])
    with left:
        by_country = (
            f.groupby("country", as_index=False)
            .size()
            .rename(columns={"size": "records"})
        )
        if not by_country.empty:
            fig_map = px.choropleth(
                by_country,
                locations="country",
                locationmode="country names",
                color="records",
                scope="africa",
                hover_name="country",
                title="Documented records by primary country",
                color_continuous_scale=["#e8e5dd", "#7aa59e", "#1d625d"],
            )
            fig_map.update_layout(
                margin=dict(l=0, r=0, t=45, b=0),
                paper_bgcolor="#f7f5ef",
                plot_bgcolor="#f7f5ef",
                coloraxis_colorbar_title="Records",
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("No records match the current filters.")

    with right:
        timeline = (
            f.dropna(subset=["year"])
            .groupby("year", as_index=False)
            .size()
            .rename(columns={"size": "records"})
        )
        if not timeline.empty:
            fig_t = px.bar(
                timeline,
                x="year",
                y="records",
                text_auto=True,
                title="Records by year",
            )
            fig_t.update_traces(marker_color="#1d625d")
            fig_t.update_layout(
                xaxis_title=None,
                yaxis_title="Records",
                margin=dict(l=0, r=0, t=45, b=0),
                paper_bgcolor="#f7f5ef",
                plot_bgcolor="#f7f5ef",
                bargap=.28,
            )
            st.plotly_chart(fig_t, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        sector = (
            f.groupby("sector", as_index=False)
            .size()
            .rename(columns={"size": "records"})
            .sort_values("records", ascending=True)
        )
        if not sector.empty:
            fig_s = px.bar(
                sector,
                x="records",
                y="sector",
                orientation="h",
                title="Where documented incidents are showing up",
            )
            fig_s.update_traces(marker_color="#b88234")
            fig_s.update_layout(
                xaxis_title="Records",
                yaxis_title=None,
                margin=dict(l=0, r=0, t=45, b=0),
                paper_bgcolor="#f7f5ef",
                plot_bgcolor="#f7f5ef",
            )
            st.plotly_chart(fig_s, use_container_width=True)

    with c2:
        sev_order = ["Low", "Limited", "Moderate", "High", "Critical"]
        sev = (
            f.assign(severity_band=pd.Categorical(f["severity_band"], sev_order, ordered=True))
            .groupby("severity_band", observed=False, as_index=False)
            .size()
            .rename(columns={"size": "records"})
        )
        fig_v = px.bar(
            sev,
            x="severity_band",
            y="records",
            text_auto=True,
            title="AAIO severity distribution",
        )
        fig_v.update_traces(marker_color="#516b78")
        fig_v.update_layout(
            xaxis_title=None,
            yaxis_title="Records",
            margin=dict(l=0, r=0, t=45, b=0),
            paper_bgcolor="#f7f5ef",
            plot_bgcolor="#f7f5ef",
        )
        st.plotly_chart(fig_v, use_container_width=True)

    st.markdown("### Read the gaps, not just the bars")
    st.write(
        "The dataset remains weighted toward incidents that leave public evidence. v0.2.0 begins to reduce that bias by adding deployed-healthcare and professional-use failures, but internal failures in lenders, employers, education and public services remain harder to observe. That skew is itself a research finding, not a prevalence ranking."
    )

with tab_explorer:
    st.subheader("Inspect individual records")
    st.caption("Every core record is linked back to public evidence and carries a separate evidence-confidence grade.")

    export_cols = [
        "incident_id", "incident_date", "country", "sector", "title",
        "system_type", "severity_score", "severity_band", "evidence_confidence",
        "source_1_url", "source_2_url", "aiid_url"
    ]
    download = f[export_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered CSV",
        download,
        file_name=f"aaio_v{version}_filtered_incidents.csv",
        mime="text/csv",
    )

    display = f[
        [
            "incident_id", "incident_date", "country", "sector", "title",
            "severity_band", "severity_score", "evidence_confidence"
        ]
    ].sort_values("incident_date", ascending=False)
    st.dataframe(display, use_container_width=True, hide_index=True)

    if not f.empty:
        options = {
            f"{row.incident_id} · {row.title}": idx
            for idx, row in f.sort_values("incident_date", ascending=False).iterrows()
        }
        selected = st.selectbox("Open a record", list(options.keys()))
        r = f.loc[options[selected]]

        st.markdown(f"## {r['incident_id']} — {r['title']}")
        a, b, c, d = st.columns(4)
        a.metric("Country", r["country"])
        b.metric("Evidence", r["evidence_confidence"])
        c.metric("Severity", f"{r['severity_band']} · {r['severity_score']}/100")
        d.metric("Year", int(r["year"]) if pd.notna(r["year"]) else "Unknown")

        st.write(r["summary"])
        st.markdown(f"**System / tool:** {r['system_type']} · {r['ai_system_or_tool']}")
        st.markdown(f"**Harm types:** {r['harm_types'].replace('|', ' · ')}")
        st.markdown(f"**Affected parties:** {r['affected_parties'].replace('|', ' · ')}")
        st.markdown(f"**Reported intent:** {r['reported_intent']}")
        st.markdown(f"**Public response:** {r['response']}")
        st.markdown(f"**Why it qualifies:** {r['qualification_basis']}")
        st.markdown(f"**Caveat:** {r['notes']}")

        links = [
            f"[Primary evidence]({r['source_1_url']})",
            f"[Secondary evidence]({r['source_2_url']})",
        ]
        if pd.notna(r.get("aiid_url")) and str(r.get("aiid_url", "")).strip():
            links.append(f"[AIID cross-reference]({r['aiid_url']})")
        st.markdown(" · ".join(links))

with tab_evidence:
    st.subheader("Evidence quality is not severity")
    st.write(
        "AAIO deliberately separates how serious an event appears from how strongly the public evidence supports the record. A high-impact allegation with weak evidence should not become a high-confidence fact."
    )

    e1, e2 = st.columns(2)
    with e1:
        conf = (
            f.groupby("evidence_confidence", as_index=False)
            .size()
            .rename(columns={"size": "records"})
            .sort_values("evidence_confidence")
        )
        fig_c = px.bar(conf, x="evidence_confidence", y="records", text_auto=True, title="Evidence-confidence grades")
        fig_c.update_traces(marker_color="#1d625d")
        fig_c.update_layout(
            xaxis_title="Grade",
            yaxis_title="Records",
            paper_bgcolor="#f7f5ef",
            plot_bgcolor="#f7f5ef",
        )
        st.plotly_chart(fig_c, use_container_width=True)

    with e2:
        source_types = pd.concat(
            [f["source_1_type"], f["source_2_type"]], ignore_index=True
        ).dropna()
        src = source_types.value_counts().rename_axis("source type").reset_index(name="references")
        fig_src = px.bar(src.sort_values("references"), x="references", y="source type", orientation="h", title="Source types used by the core records")
        fig_src.update_traces(marker_color="#b88234")
        fig_src.update_layout(
            xaxis_title="References",
            yaxis_title=None,
            paper_bgcolor="#f7f5ef",
            plot_bgcolor="#f7f5ef",
        )
        st.plotly_chart(fig_src, use_container_width=True)

    st.markdown("#### AAIO evidence grades")
    st.markdown(
        "**A — Strong:** primary/official evidence, direct admission, court or regulator material, peer-reviewed deployment evidence, or strong corroboration.  \n"
        "**B — Good:** credible independent reporting or fact-checking supports the incident, but some attribution or technical detail remains unresolved.  \n"
        "**C — Limited but credible:** one credible source supports inclusion, with meaningful uncertainty explicitly preserved.  \n"
        "**D — Unverified/disputed:** excluded from the core dataset."
    )

with tab_pipeline:
    st.subheader("See what entered the dataset — and what has not")
    st.write(
        "AAIO keeps evidence review visible. Operational cases retain their staging IDs after promotion, multilingual source candidates stay separate until they satisfy the core threshold, and material core-record changes are logged rather than silently overwritten."
    )

    p1, p2, p3 = st.columns(3)
    p1.metric("Operational review records", len(operational))
    p2.metric("Multilingual evidence candidates", len(multilingual))
    p3.metric("Material history entries", len(history))

    st.markdown("#### Operational evidence and promotion status")
    operational_cols = [
        col for col in [
            "incident_id", "country", "sector", "title", "evidence_confidence",
            "core_promotion_status", "promoted_core_id", "promoted_in_release"
        ] if col in operational.columns
    ]
    st.dataframe(operational[operational_cols], use_container_width=True, hide_index=True)

    st.markdown("#### Multilingual evidence layer")
    preferred_multilingual = [
        "incident_id", "country", "language", "original_language", "title",
        "source_language", "translation_uncertainty", "ai_attribution_strength",
        "core_promotion_status"
    ]
    multilingual_cols = [col for col in preferred_multilingual if col in multilingual.columns]
    if not multilingual_cols:
        multilingual_cols = list(multilingual.columns[:8])
    st.dataframe(multilingual[multilingual_cols], use_container_width=True, hide_index=True)

    st.markdown("#### Material record history")
    st.dataframe(history.sort_values("changed_on", ascending=False), use_container_width=True, hide_index=True)
    st.caption("The history ledger starts with material v0.2.0 promotions and is intended to remain append-only for substantive record changes.")

with tab_watchlist:
    st.subheader("Cases we deliberately did not call AI incidents")
    st.write(
        "A conservative incident dataset needs a place for important cases that matter to technology governance but do not yet satisfy the AI-linkage threshold. AAIO keeps these cases visible without mislabelling them."
    )
    st.dataframe(watch, use_container_width=True, hide_index=True)
    st.markdown(
        "This includes automated or biometric-system cases where the public evidence does not yet establish AI involvement strongly enough for core inclusion. They remain outside the core dataset unless stronger evidence establishes AI causation."
    )

with tab_method:
    st.subheader("A small dataset with explicit rules")
    st.markdown(
        "A core record must satisfy five conditions: **credible AI linkage, a realised event, a material African nexus, traceable public evidence, and wording calibrated to what the evidence actually establishes.**"
    )
    st.markdown("#### Severity model")
    st.code(
        "score = round((35*magnitude + 25*scale + 25*criticality + 15*irreversibility) / 4)",
        language="text",
    )
    st.write(
        "The score is an AAIO research aid, not an official legal or regulatory rating. Users should inspect the component dimensions and source evidence rather than treating one number as ground truth."
    )
    st.markdown(f"[Read the full methodology]({REPO}/blob/main/docs/methodology.md)")
    st.markdown(f"[Read the severity and confidence rubric]({REPO}/blob/main/docs/severity-and-confidence.md)")
    st.markdown(f"[Read the release and provenance policy]({REPO}/blob/main/docs/release-policy.md)")

st.divider()
st.markdown(
    f'<div class="aaio-small"><strong>Curated by Blessing Ezeobioha.</strong> AAIO v{version} is an independent research project. Missing records do not imply missing harm, and country comparisons should not be interpreted as prevalence rankings.</div>',
    unsafe_allow_html=True,
)
