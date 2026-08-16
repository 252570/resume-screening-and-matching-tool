"""
A curated skills database used for extracting and matching skills
from resumes and job descriptions.

Organized by category so the app can also show a category-wise
breakdown of matched/missing skills.
"""

SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "c++", "c", "c#", "javascript", "typescript",
        "sql", "r", "matlab", "go", "rust", "kotlin", "swift", "php", "scala"
    ],
    "AI/ML & Data Science": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "natural language processing", "computer vision", "tensorflow",
        "pytorch", "keras", "scikit-learn", "sklearn", "pandas", "numpy",
        "opencv", "data analysis", "data visualization", "statistics",
        "regression", "classification", "clustering", "reinforcement learning",
        "transformers", "llm", "generative ai", "feature engineering"
    ],
    "Web Development": [
        "html", "css", "react", "angular", "vue", "node.js", "nodejs",
        "django", "flask", "fastapi", "rest api", "graphql", "streamlit",
        "bootstrap", "tailwind"
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "redis", "oracle",
        "firebase", "cassandra", "elasticsearch"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "ci/cd", "jenkins", "git", "github", "gitlab", "terraform", "linux"
    ],
    "Tools & Platforms": [
        "excel", "power bi", "tableau", "jupyter", "vs code", "jira",
        "figma", "postman"
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "project management", "time management", "collaboration",
        "critical thinking", "adaptability"
    ],
}


def get_all_skills():
    """Flat list of every skill in the database, lowercase."""
    all_skills = []
    for skills in SKILLS_DB.values():
        all_skills.extend(skills)
    return sorted(set(s.lower() for s in all_skills))


def get_skill_category(skill):
    """Return which category a skill belongs to."""
    skill_lower = skill.lower()
    for category, skills in SKILLS_DB.items():
        if skill_lower in [s.lower() for s in skills]:
            return category
    return "Other"
