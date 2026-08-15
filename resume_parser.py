"""
Handles reading resumes (PDF / DOCX / TXT) and extracting
structured info: raw text, email, phone, and detected skills.
"""

import re
import pdfplumber
import docx

from src.skills_db import get_all_skills


def extract_text_from_pdf(file) -> str:
    text = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def extract_text_from_docx(file) -> str:
    document = docx.Document(file)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(file, filename: str) -> str:
    """Dispatch to the right extractor based on file extension."""
    filename = filename.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)
    elif filename.endswith(".txt"):
        raw = file.read()
        return raw.decode("utf-8") if isinstance(raw, bytes) else raw
    else:
        raise ValueError(f"Unsupported file type: {filename}")


def extract_email(text: str) -> str | None:
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = re.search(r"(\+?\d{1,3}[-.\s]?)?\d{10}", text)
    return match.group(0) if match else None


def extract_skills(text: str) -> list[str]:
    """
    Detect known skills present in the text using simple substring
    matching on a normalized version of the text. Good enough for a
    mini-project; a production system would use fuzzy matching / NER.
    """
    cleaned = re.sub(r"[^a-z0-9+#.\s]", " ", text.lower())
    normalized = " " + re.sub(r"\s+", " ", cleaned) + " "
    found = []
    for skill in get_all_skills():
        pattern = " " + skill + " "
        if pattern in normalized:
            found.append(skill)
    return sorted(set(found))


def parse_document(file, filename: str) -> dict:
    """Full parse pipeline: returns text + extracted metadata."""
    text = extract_text(file, filename)
    return {
        "filename": filename,
        "text": text,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "word_count": len(text.split()),
    }
