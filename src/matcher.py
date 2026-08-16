"""
Core matching engine. Combines two signals into a final match score:

1. Text similarity (TF-IDF + cosine similarity) between resume and
   job description — captures overall semantic/content overlap.
2. Skill overlap — the fraction of JD-required skills that are
   present in the resume, weighted more heavily since it's the
   most interpretable signal for a viva/demo.

Final score = 0.4 * text_similarity + 0.6 * skill_overlap
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_text_similarity(resume_text: str, jd_text: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(sim)


def compute_skill_overlap(resume_skills: list[str], jd_skills: list[str]) -> tuple[float, list[str], list[str]]:
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    if not jd_set:
        return 0.0, [], []

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    overlap_score = len(matched) / len(jd_set)

    return overlap_score, matched, missing


def match_resume_to_jd(resume: dict, jd: dict) -> dict:
    """
    resume, jd: dicts produced by resume_parser.parse_document(),
    each with 'text' and 'skills' keys.
    """
    text_sim = compute_text_similarity(resume["text"], jd["text"])
    skill_score, matched_skills, missing_skills = compute_skill_overlap(
        resume["skills"], jd["skills"]
    )

    final_score = 0.4 * text_sim + 0.6 * skill_score

    return {
        "filename": resume["filename"],
        "final_score": round(final_score * 100, 2),
        "text_similarity": round(text_sim * 100, 2),
        "skill_match_pct": round(skill_score * 100, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "email": resume.get("email"),
        "phone": resume.get("phone"),
    }


def rank_resumes(resumes: list[dict], jd: dict) -> list[dict]:
    """Score every resume against the JD and return sorted best-first."""
    results = [match_resume_to_jd(r, jd) for r in resumes]
    return sorted(results, key=lambda r: r["final_score"], reverse=True)
