import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

# --- Part 1: Sentence similarity ---
print("--- Part 1: Sentence similarity ---")
model = SentenceTransformer('all-MiniLM-L6-v2')
resume_text  = "Python developer with machine learning experience"
job_desc     = "We need a Python engineer skilled in ML and AI"
emb1 = model.encode([resume_text])
emb2 = model.encode([job_desc])
score = cosine_similarity(emb1, emb2)[0][0]
print(f"Job Match Score: {round(score * 100, 1)}%")
print("Part 1: Success\n")

# --- Part 2: ATS keyword check ---
print("--- Part 2: ATS keyword check ---")
ats_keywords = ["python", "machine learning", "ai", "data"]
resume_lower = resume_text.lower()
matched = [k for k in ats_keywords if k in resume_lower]
ats_score = int(len(matched) / len(ats_keywords) * 100)
print(f"ATS Score: {ats_score}%  |  Matched: {matched}")
print("Part 2: Success\n")

# --- Part 3: Groq API ---
print("--- Part 3: Groq API ---")
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("Warning: GROQ_API_KEY not found in environment variables. Please check your .env file.")

client = Groq(api_key=api_key)
msg = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say: CareerBuddy AI is ready!"}]
)
print(msg.choices[0].message.content)
print("Part 3: Success")

print("\nIf all 3 parts print success, you are 100% ready for tomorrow!")
