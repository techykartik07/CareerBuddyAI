import pickle

# Load saved model and vectorizer
with open("models/job_classifier.pkl",  "rb") as f: model = pickle.load(f)
with open("models/tfidf_vectorizer.pkl","rb") as f: tfidf = pickle.load(f)

def predict(text):
    vec   = tfidf.transform([text])
    role  = model.predict(vec)[0]
    probs = model.predict_proba(vec)[0]
    top3  = sorted(zip(model.classes_, probs), key=lambda x: x[1], reverse=True)[:3]
    print(f"\nInput: {text[:80]}...")
    print(f"Predicted role: {role}")
    print("Top 3 matches:")
    for r, p in top3:
        bar = "█" * int(p * 30)
        print(f"  {r:30s} {bar} {p*100:.1f}%")

# Test 1: Should predict a Data Science role
predict("""
Experienced data scientist with 3 years in machine learning,
Python, TensorFlow, deep learning, statistical modelling,
pandas, numpy, data visualisation, scikit-learn, NLP projects.
""")

# Test 2: Should predict a Java/Backend Developer role
predict("""
Java backend developer skilled in Spring Boot, microservices,
REST APIs, SQL, Hibernate, Maven, Docker, CI/CD pipelines,
AWS deployment, unit testing with JUnit.
""")

# Test 3: Should predict a Web Designer or Frontend role
predict("""
Frontend developer with expertise in React, HTML5, CSS3,
JavaScript, UI/UX design, Figma, responsive design,
Tailwind CSS, accessibility standards.
""")