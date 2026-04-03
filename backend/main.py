from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()  # reads .env file
app = FastAPI(title="CareerBuddy AI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tighten this before production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "CareerBuddy AI Backend"}

# Routers registered here after M2 creates his files:
# from routers.resume import router as resume_router
# from routers.ai     import router as ai_router
# app.include_router(resume_router)
# app.include_router(ai_router)