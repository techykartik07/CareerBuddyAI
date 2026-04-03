"""
skills_list.py — Hardcoded skill vocabulary for resume matching.

Add or remove skills from the SKILLS list as needed.
These are matched case-insensitively against resume text.
"""

SKILLS: list[str] = [
    # Programming Languages
    "Python", "JavaScript", "TypeScript", "Java", "C", "C++", "C#",
    "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",
    "MATLAB", "Bash", "Shell", "PowerShell",

    # Web Development
    "HTML", "CSS", "React", "Next.js", "Vue.js", "Angular", "Svelte",
    "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot",
    "REST API", "GraphQL", "WebSockets",

    # Data & AI / ML
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "scikit-learn", "XGBoost",
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "OpenCV",
    "spaCy", "NLTK", "Hugging Face", "LangChain", "LLM",
    "RAG", "Prompt Engineering", "Fine-tuning",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis",
    "Firebase", "Cassandra", "DynamoDB", "Elasticsearch",

    # Cloud & DevOps
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform",
    "CI/CD", "GitHub Actions", "Jenkins", "Linux", "Nginx",

    # Tools & Practices
    "Git", "GitHub", "REST", "Agile", "Scrum", "JIRA",
    "Unit Testing", "Pytest", "Selenium", "Postman",

    # Soft Skills / Domains
    "Data Analysis", "Data Engineering", "Data Visualization",
    "Full Stack", "Backend", "Frontend", "Mobile Development",
    "Android", "iOS", "React Native", "Flutter",
    "System Design", "Problem Solving", "Communication",
]
