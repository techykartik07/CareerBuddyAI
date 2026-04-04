from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ai, resume

load_dotenv()
app = FastAPI(title="CareerBuddy AI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "CareerBuddy AI Backend"}