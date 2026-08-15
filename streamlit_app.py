"""
ResumeIQ — Resume Screening & Job Matching Tool
Modern Streamlit web UI for screening resumes against a job description.
Run: streamlit run app/streamlit_app.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import plotly.express as px
import streamlit as st

from src.resume_parser import parse_document, extract_skills
from src.matcher import rank_resumes

st.set_page_config(
    page_title="ResumeIQ | AI Resume Screening",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------- Styling ---------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #f7f9fc;
  --card: #ffffff;
  --ink: #101828;
  --muted: #667085;
  --line: #e7eaf0;
  --primary: #635bff;
  --primary-dark: #5147e8;
  --soft: #f0efff;
  --success: #12b76a;
  --warning: #f79009;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: var(--bg); color: var(--ink); }
.block-container { padding: 1.2rem 3.2rem 3rem; max-width: 1500px; }

/* Hide Streamlit chrome */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #111827; border-right: 0; }
[data-testid="stSidebar"] * { color: #eef2ff !important; }
[data-testid="stSidebar"] .stRadio label { color: #d7dded !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #aeb8cc !important; }
[data-testid="stSidebar"] hr { border-color: #2b3548; }

/* Sidebar */
.sidebar-brand { padding: 0.5rem 0.2rem 1.3rem; }
.brand-mark {
  display: inline-flex; align-items: center; justify-content: center;
  width: 40px; height: 40px; border-radius: 12px;
  background: linear-gradient(135deg, #7c6cff, #4f46e5);
  color: white; font-size: 20px; font-weight: 800;
  margin-right: 10px; vertical-align: middle;
  box-shadow: 0 8px 22px rgba(99,91,255,.35);
}
.brand-name { font-size: 20px; font-weight: 800; vertical-align: middle; }
.sidebar-section { color: #8f9ab0 !important; font-size: 11px !important; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; margin: 1rem 0 .55rem; }

/* Buttons */
.stButton > button, .stDownloadButton > button {
  border-radius: 10px !important; border: 1px solid var(--line) !important;
  min-height: 42px; font-weight: 700 !important;
  transition: .18s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-1px); }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--primary), #7c6cff) !important; border: 0 !important; color: white !important; }

/* Hero */
.hero {
  background: linear-gradient(135deg, #111827 0%, #1e2142 55%, #3d35a6 100%);
  border-radius: 24px; padding: 34px 38px; color: white;
  box-shadow: 0 18px 45px rgba(17,24,39,.15); margin-bottom: 24px;
  position: relative; overflow: hidden;
}
.hero:after { content: ''; position: absolute; width: 300px; height: 300px; border-radius: 50%; background: rgba(124,108,255,.18); right: -90px; top: -120px; }
.hero-eyebrow { color: #b9b4ff; font-size: 12px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 8px; }
.hero h1 { color: white; font-size: 34px; line-height: 1.1; margin: 0 0 10px; font-weight: 800; }
.hero p { color: #cbd1e1; font-size: 15px; max-width: 700px; margin: 0; line-height: 1.6; }

/* Cards */
.card { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 20px; box-shadow: 0 5px 20px rgba(16,24,40,.035); }
.metric-card { background: white; border: 1px solid var(--line); border-radius: 16px; padding: 18px 20px; min-height: 110px; }
.metric-label { color: var(--muted); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; }
.metric-value { color: var(--ink); font-size: 28px; font-weight: 800; margin-top: 7px; }
.metric-note { color: #98a2b3; font-size: 12px; margin-top: 3px; }
.section-title { font-size: 18px; font-weight: 800; margin: 5px 0 4px; }
.section-subtitle { color: var(--muted); font-size: 13px; margin-bottom: 16px; }

/* Upload / input area — high contrast in the dark sidebar */
.upload-card { background: #182236; border: 1px solid #34415b; border-radius: 16px; padding: 12px; }
[data-testid="stFileUploaderDropzone"] {
  background: linear-gradient(145deg, #202b42, #182236) !important;
  border: 1.5px dashed #8b82ff !important;
  border-radius: 14px !important;
  min-height: 112px;
  box-shadow: inset 0 0 0 1px rgba(139,130,255,.08), 0 8px 24px rgba(0,0,0,.18);
}
[data-testid="stFileUploaderDropzone"]:hover {
  background: linear-gradient(145deg, #283452, #1d2940) !important;
  border-color: #b0a9ff !important;
}
[data-testid="stFileUploaderDropzone"] * { color: #eef2ff !important; }
[data-testid="stFileUploaderDropzone"] small { color: #aeb8cc !important; }
[data-testid="stFileUploaderDropzone"] button {
  background: #635bff !important; color: white !important; border: 0 !important;
  border-radius: 9px !important; font-weight: 700 !important;
}
[data-testid="stFileUploaderDropzone"] button:hover { background: #7c6cff !important; }
[data-testid="stTextArea"] textarea {
  background: #182236 !important; color: #f8fafc !important;
  border: 1px solid #46536d !important; border-radius: 12px !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: #9aa7bd !important; }
[data-testid="stTextArea"] textarea:focus { border-color: #8b82ff !important; box-shadow: 0 0 0 1px #8b82ff !important; }

/* Tables / expanders */
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }
.streamlit-expanderHeader { border-radius: 12px !important; font-weight: 700 !important; }

/* Pills */
.pill { display: inline-block; padding: 6px 10px; border-radius: 999px; background: var(--soft); color: #5147e8; font-size: 12px; font-weight: 700; margin: 3px 4px 3px 0; }
.pill-green { background: #e9f9f1; color: #087443; }
.pill-red { background: #fff0f0; color: #c43232; }

/* Empty state */
.empty { text-align: center; background: white; border: 1px solid var(--line); border-radius: 20px; padding: 54px 24px; margin-top: 10px; }
.empty-icon { width: 64px; height: 64px; margin: auto auto 15px; display: flex; align-items: center; justify-content: center; border-radius: 18px; background: var(--soft); font-size: 28px; }
.empty h3 { margin: 0 0 8px; font-size: 20px; }
.empty p { color: var(--muted); margin: 0 auto; max-width: 570px; line-height: 1.6; }

/* Motion + interactive cards */
@keyframes fadeUp { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
@keyframes floatSoft { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-5px); } }
.hero, .metric-card, .card, .empty { animation: fadeUp .5s ease both; }
.metric-card { transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
.metric-card:hover { transform: translateY(-5px); box-shadow: 0 14px 32px rgba(16,24,40,.10); border-color:#d9d6ff; }
.card { transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
.card:hover { transform: translateY(-3px); box-shadow: 0 14px 32px rgba(16,24,40,.09); border-color:#d9d6ff; }
.hero:after { animation: floatSoft 5s ease-in-out infinite; }
.hero-cta { display:inline-flex; align-items:center; gap:8px; margin-top:20px; padding:10px 15px; border-radius:10px; background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.18); color:#fff; font-size:13px; font-weight:700; }
.feature-card { background:white; border:1px solid var(--line); border-radius:18px; padding:22px; height:100%; transition:all .22s ease; }
.feature-card:hover { transform:translateY(-6px); box-shadow:0 16px 34px rgba(16,24,40,.10); border-color:#d9d6ff; }
.feature-icon { width:42px; height:42px; border-radius:12px; display:flex; align-items:center; justify-content:center; background:var(--soft); color:#5147e8; font-size:20px; margin-bottom:14px; }
.feature-card h3 { margin:0 0 7px; font-size:16px; }
.feature-card p { margin:0; color:var(--muted); font-size:13px; line-height:1.6; }
.home-title { font-size:46px; line-height:1.05; font-weight:850; letter-spacing:-.04em; margin:0; }
.home-gradient { background:linear-gradient(90deg,#635bff,#9b8cff); -webkit-background-clip:text; background-clip:text; color:transparent; }
.search-box { background:#fff; border:1px solid var(--line); border-radius:14px; padding:14px; box-shadow:0 5px 18px rgba(16,24,40,.04); }
.stProgress > div > div { border-radius:99px; }
/* Responsive */
@media (max-width: 900px) {
  .block-container { padding: .8rem .8rem 2rem; }
  .hero { padding: 24px; border-radius:18px; }
  .hero h1 { font-size: 28px; }
  .home-title { font-size:34px; }
  [data-testid="stSidebar"] { min-width: 250px; max-width: 82vw; }
  .metric-card { min-height: 96px; }
}
@media (max-width: 600px) {
  .block-container { padding: .65rem .55rem 1.5rem; }
  .hero p { font-size:14px; }
  .section-title { font-size:16px; }
  .home-title { font-size:30px; }
}

</style>
""",
    unsafe_allow_html=True,
)


def metric_card(label, value, note=""):
    st.markdown(
        f"""<div class='metric-card'><div class='metric-label'>{label}</div>
        <div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>""",
        unsafe_allow_html=True,
    )


def skills_pills(skills, green=False):
    if not skills:
        return "<span style='color:#98a2b3'>None detected</span>"
    cls = "pill pill-green" if green else "pill"
    return "".join(f"<span class='{cls}'>{str(s).title()}</span>" for s in skills)


# --------------------------- Sidebar ---------------------------
with st.sidebar:
    st.markdown("""<div class='sidebar-brand'><span class='brand-mark'>✦</span><span class='brand-name'>ResumeIQ</span></div>""", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section'>Workspace</div>", unsafe_allow_html=True)
    page = st.radio("Navigate", ["Home", "Screening workspace"], label_visibility="collapsed")

    jd_text = ""
    resume_files = []
    run = False

    if page == "Screening workspace":
        st.markdown("<div class='sidebar-section'>Screening setup</div>", unsafe_allow_html=True)
        jd_input_mode = st.radio("Job description", ["Paste text", "Upload file"], horizontal=True)
        if jd_input_mode == "Paste text":
            st.markdown("<div style='color:#eef2ff;font-weight:700;font-size:13px;margin:0 0 7px'>📝 Job description</div>", unsafe_allow_html=True)
            jd_text = st.text_area("Job description", height=220, placeholder="Paste the role description here...\n\nExample: Python, machine learning, SQL, communication...", label_visibility="collapsed")
        else:
            st.markdown("<div style='color:#eef2ff;font-weight:700;font-size:13px;margin:0 0 7px'>📄 Job description file</div>", unsafe_allow_html=True)
            jd_file = st.file_uploader("Upload job description", type=["pdf", "docx", "txt"], label_visibility="collapsed")
            if jd_file:
                from src.resume_parser import extract_text
                jd_text = extract_text(jd_file, jd_file.name)

        st.markdown("<div class='sidebar-section'>Candidate resumes</div>", unsafe_allow_html=True)
        st.markdown("<div style='color:#aeb8cc;font-size:12px;margin:-2px 0 8px'>📎 Add one or multiple resumes</div>", unsafe_allow_html=True)
        resume_files = st.file_uploader("Upload resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True, label_visibility="collapsed")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("✦  Analyze candidates", type="primary", use_container_width=True):
            st.session_state["run_analysis"] = True
        run = st.session_state.get("run_analysis", False)
        st.markdown("<div class='sidebar-section'>Scoring model</div>", unsafe_allow_html=True)
        st.markdown("""<div style='font-size:12px;line-height:1.7;color:#aeb8cc'><b style='color:#eef2ff'>40%</b> Text similarity<br><b style='color:#eef2ff'>60%</b> Skill match<br><br>Results are ranked automatically and each candidate includes a clear skill-gap explanation.</div>""", unsafe_allow_html=True)

# --------------------------- Landing page ---------------------------
if page == "Home":
    st.markdown("""<div class='hero' style='padding:48px 44px'>
      <div class='hero-eyebrow'>RESUMEIQ • AI RECRUITING WORKSPACE</div>
      <div class='home-title'>Find the right candidates <span class='home-gradient'>faster.</span></div>
      <p style='margin-top:14px;max-width:760px'>Turn a job description and a folder of resumes into a clear, ranked shortlist. ResumeIQ combines text similarity and skill matching so you can spend less time screening and more time interviewing.</p>
      <div class='hero-cta'>✦ Explainable matching • Fast screening • Skill gaps</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='font-size:22px;font-weight:800;margin:25px 0 6px'>Everything you need to screen better</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#667085;font-size:13px;margin-bottom:16px'>A clean recruiting workflow designed for speed, clarity and better decisions.</div>", unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col,icon,title,desc in [(a,'⚡','Screen in seconds','Upload multiple resumes and get an automatically ranked shortlist.'),(b,'🎯','Match the right skills','See matched and missing skills for every candidate at a glance.'),(c,'📊','Make decisions with data','Compare match, skill and text scores with clear visual insights.')]:
        with col:
            st.markdown(f"<div class='feature-card'><div class='feature-icon'>{icon}</div><h3>{title}</h3><p>{desc}</p></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><div style='font-size:18px;font-weight:800;margin-bottom:6px'>How it works</div><div style='color:#667085;font-size:13px;line-height:1.8'>1. Add a job description → 2. Upload candidate resumes → 3. Analyze → 4. Search, filter and sort your shortlist → 5. Export results.</div></div>", unsafe_allow_html=True)
    st.stop()

# --------------------------- Hero ---------------------------
st.markdown(
    """<div class='hero'>
      <div class='hero-eyebrow'>AI-powered hiring workspace</div>
      <h1>Screen smarter. Shortlist faster.</h1>
      <p>Compare resumes against a job description, surface the strongest candidates, and understand exactly which skills match or are missing.</p>
    </div>""",
    unsafe_allow_html=True,
)

# --------------------------- Empty / setup state ---------------------------
if not run:
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Step 01", "Add role", "Paste or upload a job description")
    with c2:
        metric_card("Step 02", "Add resumes", "Upload one or multiple candidates")
    with c3:
        metric_card("Step 03", "Analyze", "Get ranked, explainable results")

    st.markdown(
        """<div class='empty'>
          <div class='empty-icon'>⌕</div>
          <h3>Your candidate dashboard is ready</h3>
          <p>Use the setup panel on the left to add a job description and resumes. ResumeIQ will calculate a weighted match score and show the strongest candidates first.</p>
        </div>""",
        unsafe_allow_html=True,
    )
    st.stop()

# --------------------------- Validation ---------------------------
if not jd_text.strip():
    st.error("Please provide a job description before analyzing candidates.")
    st.stop()
if not resume_files:
    st.error("Please upload at least one resume before analyzing candidates.")
    st.stop()

# --------------------------- Processing ---------------------------
with st.spinner("Analyzing the job description..."):
    jd_skills = extract_skills(jd_text)
    jd = {"text": jd_text, "skills": jd_skills}

with st.spinner(f"Parsing {len(resume_files)} resume(s)..."):
    resumes = [parse_document(f, f.name) for f in resume_files]

with st.spinner("Calculating candidate match scores..."):
    results = rank_resumes(resumes, jd)

# --------------------------- Dashboard ---------------------------
# Build a stable dataframe schema even when no results are returned.
# This prevents Plotly/Pandas from raising KeyError for missing score columns.
result_rows = [
    {
        "Rank": i + 1,
        "Candidate": r.get("filename", "Unknown"),
        "Match Score (%)": float(r.get("final_score", 0)),
        "Skill Match (%)": float(r.get("skill_match_pct", 0)),
        "Text Similarity (%)": float(r.get("text_similarity", 0)),
        "Email": r.get("email") or "—",
        "Phone": r.get("phone") or "—",
    }
    for i, r in enumerate(results)
]

result_columns = [
    "Rank", "Candidate", "Match Score (%)", "Skill Match (%)",
    "Text Similarity (%)", "Email", "Phone"
]
df = pd.DataFrame(result_rows, columns=result_columns)

best = results[0] if results else None
avg_score = round(float(df["Match Score (%)"].mean()), 1) if not df.empty else 0
high_matches = int((df["Match Score (%)"] >= 70).sum()) if not df.empty else 0

st.markdown("<div class='section-title'>Screening overview</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle'>A quick view of the current candidate pool.</div>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("Candidates", len(results), "Resumes analyzed")
with m2:
    metric_card("Required skills", len(jd_skills), "Detected from the role")
with m3:
    metric_card("Average match", f"{avg_score}%", "Across all candidates")
with m4:
    metric_card("Strong matches", high_matches, "Candidates scoring 70%+")

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

if best:
    left, right = st.columns([1.55, 1])
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Top candidate</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:22px;font-weight:800;margin:8px 0'>{best['filename']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='color:#667085;font-size:13px'>Overall match <b style='color:#5147e8'>{best['final_score']}%</b> · Skill match <b>{best['skill_match_pct']}%</b> · Text similarity <b>{best['text_similarity']}%</b></div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("<b>Matched skills</b>", unsafe_allow_html=True)
        st.markdown(skills_pills(best["matched_skills"], True), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Role skill profile</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Skills detected in the job description.</div>", unsafe_allow_html=True)
        st.markdown(skills_pills(jd_skills), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# --------------------------- Tabs ---------------------------
tab_overview, tab_candidates, tab_skills = st.tabs(["Overview", "Candidates", "Skill gaps"])

with tab_overview:
    if df.empty:
        st.info("No candidate results are available yet. Add resumes and run the analysis.")
    else:
        chart_df = df.sort_values(by="Match Score (%)", ascending=True)
        fig = px.bar(
            chart_df,
            x="Match Score (%)",
            y="Candidate",
            orientation="h",
            text="Match Score (%)",
            template="plotly_white",
            color="Match Score (%)",
            color_continuous_scale=[[0, "#d9d7ff"], [0.55, "#8b84ff"], [1, "#5147e8"]],
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False)
        fig.update_layout(
            height=max(340, 75 * len(df)),
            margin=dict(l=10, r=45, t=10, b=10),
            coloraxis_showscale=False,
            xaxis=dict(range=[0, max(100, float(df["Match Score (%)"].max()) + 8)], title=None),
            yaxis=dict(title=None),
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with tab_candidates:
    st.markdown("<div class='section-title'>Ranked candidate list</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Search candidates, filter by match strength, and sort the shortlist your way.</div>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns([2.2, 1, 1.2])
    with f1:
        search = st.text_input("Search candidates", placeholder="Search by filename, email or phone...", label_visibility="collapsed")
    with f2:
        min_match = st.slider("Minimum match", 0, 100, 0, 5)
    with f3:
        sort_by = st.selectbox("Sort by", ["Match score", "Skill match", "Text similarity", "Candidate name"])
    filtered = df.copy()
    if search.strip():
        q = search.strip().lower()
        mask = filtered.astype(str).apply(lambda col: col.str.lower().str.contains(q, na=False))
        filtered = filtered[mask.any(axis=1)]
    filtered = filtered[filtered["Match Score (%)"] >= min_match]
    sort_map = {"Match score":"Match Score (%)", "Skill match":"Skill Match (%)", "Text similarity":"Text Similarity (%)", "Candidate name":"Candidate"}
    filtered = filtered.sort_values(sort_map[sort_by], ascending=(sort_by == "Candidate name")).reset_index(drop=True)
    filtered["Rank"] = range(1, len(filtered)+1)
    st.caption(f"Showing {len(filtered)} of {len(df)} candidates")
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("#", width="small"),
            "Match Score (%)": st.column_config.ProgressColumn("Match", min_value=0, max_value=100, format="%d%%"),
            "Skill Match (%)": st.column_config.ProgressColumn("Skills", min_value=0, max_value=100, format="%d%%"),
            "Text Similarity (%)": st.column_config.ProgressColumn("Text", min_value=0, max_value=100, format="%d%%"),
        },
    )

with tab_skills:
    for i, r in enumerate(results):
        score = r["final_score"]
        label = "Strong match" if score >= 70 else "Potential match" if score >= 50 else "Needs review"
        with st.expander(f"#{i + 1}  {r['filename']}  ·  {score}%  ·  {label}", expanded=(i == 0)):
            a, b = st.columns(2)
            with a:
                st.markdown("**Matched skills**")
                st.markdown(skills_pills(r["matched_skills"], True), unsafe_allow_html=True)
            with b:
                st.markdown("**Missing skills**")
                st.markdown(
                    "".join(f"<span class='pill pill-red'>{str(s).title()}</span>" for s in r["missing_skills"])
                    if r["missing_skills"] else "<span style='color:#12b76a;font-weight:700'>No missing required skills</span>",
                    unsafe_allow_html=True,
                )

# --------------------------- Export ---------------------------
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
ex1, ex2 = st.columns([1, 4])
with ex1:
    st.download_button(
        "↓  Export CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="resume_matching_results.csv",
        mime="text/csv",
        use_container_width=True,
    )
with ex2:
    st.caption("Export the ranked shortlist and scoring details for your records.")
