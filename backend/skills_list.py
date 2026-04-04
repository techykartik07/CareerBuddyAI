# backend/skills_list.py
TECH_SKILLS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c", "go", "rust",
    "kotlin", "swift", "r", "scala", "sql", "html", "css",
    # ML / AI
    "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
    "scikit-learn", "nlp", "computer vision", "transformers",
    # Data
    "pandas", "numpy", "matplotlib", "data analysis", "data science",
    "power bi", "tableau", "excel", "spark", "hadoop",
    # Web / Backend
    "fastapi", "django", "flask", "node.js", "react", "vue", "angular",
    "data scientist", "software engineer", "frontend developer", "backend developer",
    "fullstack developer", "data engineer", "machine learning engineer",
    "rest api", "graphql", "docker", "kubernetes", "aws", "azure", "gcp",
    # Tools
    "git", "github", "linux", "bash", "postman", "jira", "agile",
]

import re as _re

def extract_skills(text: str) -> list:
    """Extract skills using whole-word / whole-phrase matching.

    Uses word boundaries so e.g. 'data science' won't match inside
    'data structure', and single-char skills like 'r', 'c' are skipped
    to avoid false positives.
    """
    text_lower = text.lower()
    matched = []
    for skill in TECH_SKILLS:
        # Build pattern: word boundary on both sides, handle special chars
        pattern = r'(?<![\w-])' + _re.escape(skill) + r'(?![\w-])'
        if _re.search(pattern, text_lower):
            matched.append(skill)
    return matched

def extract_sections(text: str) -> dict:
    sections = {"education": "", "experience": "", "projects": ""}
    lines = text.split('\n')
    current = None
    buffer = []

    section_headers = {
        "education": ["education", "academic", "qualification"],
        "experience": ["experience", "employment", "work history"],
        "projects": ["project", "portfolio"],
    }
    
    for line in lines:
        lower = line.lower().strip()
        matched = False
        for key, keywords in section_headers.items():
            if any(kw in lower for kw in keywords):
                if current:
                    sections[current] = "\n".join(buffer).strip()
                current, buffer, matched = key, [], True
                break
        if not matched and current:
            buffer.append(line)
            
    if current:
        sections[current] = "\n".join(buffer).strip()
    return sections
