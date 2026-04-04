import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ── 1. LOAD DATA ──────────────────────────────────────────
print("Loading dataset...")
df = pd.read_csv("data/Resume.csv")

df = df.drop_duplicates(subset=["Resume"]).reset_index(drop=True)
print(f"Dataset loaded: {len(df)} resumes, {df['Category'].nunique()} job categories")

# Drop rows where Resume text is empty
df = df.dropna(subset=["Resume", "Category"])
df["Resume"] = df["Resume"].astype(str)

X = df["Resume"]
y = df["Category"]

# ── 2. SPLIT DATA ─────────────────────────────────────────
print("\nSplitting into train/test sets (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y        # ensures each category is represented in both sets
)
print(f"Training samples : {len(X_train)}")
print(f"Testing  samples : {len(X_test)}")

# ── 3. FEATURE EXTRACTION ─────────────────────────────────
print("\nExtracting TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=3000,       # top 3000 most important words
    stop_words="english",    # remove common words like "the", "and"
    ngram_range=(1, 2),      # capture single words AND two-word phrases
    sublinear_tf=True        # reduces impact of very frequent terms
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)
print(f"Feature matrix shape: {X_train_vec.shape}")

# ── 4. TRAIN MODEL ────────────────────────────────────────
print("\nTraining Logistic Regression classifier...")
model = LogisticRegression(
    max_iter=1000,
    C=5.0,                   # regularisation — higher = less penalty
    solver="lbfgs",
)
model.fit(X_train_vec, y_train)
print("Training complete.")

# ── 5. EVALUATE ───────────────────────────────────────────
print("\nEvaluating on test set...")
y_pred   = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "="*50)
print(f"  MODEL ACCURACY: {accuracy * 100:.1f}%")
print("="*50)
print("\nPer-category breakdown:")
print(classification_report(y_test, y_pred))

# ── 6. SAVE MODEL ─────────────────────────────────────────
os.makedirs("models", exist_ok=True)

with open("models/job_classifier.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Save class labels separately for easy reference
with open("models/categories.pkl", "wb") as f:
    pickle.dump(model.classes_.tolist(), f)

print("\nModel saved to models/job_classifier.pkl")
print("Vectorizer saved to models/tfidf_vectorizer.pkl")
print(f"Categories saved: {model.classes_.tolist()}")
print("\nDone. Training pipeline complete.")