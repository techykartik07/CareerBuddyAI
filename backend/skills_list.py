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

def extract_skills(text: str) -> list:
    text_lower = text.lower()
    return [skill for skill in TECH_SKILLS if skill in text_lower]

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
