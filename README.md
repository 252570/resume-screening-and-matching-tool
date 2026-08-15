# Resume Screening & Job Matching Tool

A mini-project for CS(AI/ML): an NLP-based tool that screens and ranks
resumes against a job description, highlighting skill matches and gaps.

## What it does
1. Takes a Job Description (pasted text or uploaded file) and one or more
   resumes (PDF / DOCX / TXT).
2. Extracts text, contact info, and known skills from each document.
3. Scores every resume against the JD using two signals:
   - **TF-IDF + cosine similarity** (overall content overlap) — 40% weight
   - **Skill overlap** (fraction of JD skills present in resume) — 60% weight
4. Shows a ranked table, a bar chart, and a per-candidate skill gap
   breakdown (matched vs. missing skills).
5. Lets you export results as CSV.

## Tech stack
- **Python** — core logic
- **scikit-learn** — TF-IDF vectorization + cosine similarity
- **pdfplumber / python-docx** — resume/JD text extraction
- **Streamlit** — web UI
- **Plotly** — charts
- **pandas** — results table + CSV export

## Project structure
```
resume-matcher/
├── app/
│   └── streamlit_app.py     # Streamlit UI (entry point)
├── src/
│   ├── resume_parser.py     # text extraction + skill/email/phone parsing
│   ├── matcher.py           # TF-IDF similarity + skill overlap scoring
│   └── skills_db.py         # curated skills database (7 categories)
├── data/
│   ├── sample_jd.txt        # sample job description
│   ├── sample_resume_1.txt  # sample strong-match resume
│   └── sample_resume_2.txt  # sample weak-match resume
├── requirements.txt
└── README.md
```

## How to run

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app/streamlit_app.py
```

The app opens at `http://localhost:8501`. Paste the sample JD from
`data/sample_jd.txt` and upload `sample_resume_1.txt` /
`sample_resume_2.txt` to see it work immediately.

## Scoring formula
```
final_score = 0.4 × text_similarity + 0.6 × skill_overlap
```
Skill overlap is weighted higher because it's more interpretable and
directly explainable in a viva — you can literally show which required
skills a candidate has and which they're missing.

## Possible extensions (good for "Future Scope" in your report)
- Swap the skills database for spaCy Named Entity Recognition to catch
  skills not in a fixed list.
- Add experience-level extraction (years of experience) as a third
  scoring signal.
- Use sentence embeddings (e.g. `sentence-transformers`) instead of
  TF-IDF for better semantic matching (catches "ML" ≈ "machine learning"
  even with different phrasing).
- Add resume-side "how to improve your match score" suggestions.
- Deploy on Streamlit Community Cloud for a live demo link in your report.

## Notes for your report/viva
- **Problem statement**: manual resume screening is slow and inconsistent;
  this automates initial shortlisting using NLP.
- **Novelty angle**: combines statistical text similarity with an
  explainable, category-tagged skill database — so results aren't a
  black box, you can show exactly *why* a candidate scored what they did.
- **Dataset**: works with any resumes/JDs; no training data needed since
  it uses TF-IDF (unsupervised) rather than a trained classifier — makes
  it easy to demo with your own or classmates' resumes.
