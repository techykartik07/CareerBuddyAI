from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import ai, resume
# from dotenv import load_dotenv

# load_dotenv()  # reads .env file
app = FastAPI(title="CareerBuddy AI", version="1.0")

app.include_router(ai.router)
app.include_router(resume.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tighten this before production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "CareerBuddyAI backend is running 🚀"}


@app.get("/health")
def health_check():
    """Global health check for the backend."""
    return {"status": "ok", "service": "CareerBuddy AI Backend"}

from routers.resume import router as resume_router
from routers.ai     import router as ai_router

app.include_router(resume_router)
app.include_router(ai_router)