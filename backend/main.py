from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

# Import routers
from routers.resume import router as resume_router
from routers.ai import router as ai_router

load_dotenv()
app = FastAPI(
    title="CareerBuddy AI", 
    version="1.0",
    docs_url="/docs",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://careerbuddyai-backend-kartik.onrender.com",
        "https://career-buddy-ai-kappa.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def root():
    """Beautiful landing page for the CareerBuddy AI Backend."""
    return """
    <html>
        <head>
            <title>CareerBuddy AI Backend 🚀</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    font-family: 'Outfit', sans-serif;
                    background: radial-gradient(circle at top right, #0f172a 0%, #020617 100%);
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    overflow: hidden;
                }
                .container {
                    text-align: center;
                    padding: 3rem;
                    background: rgba(30, 41, 59, 0.5);
                    backdrop-filter: blur(12px);
                    border-radius: 24px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                    max-width: 600px;
                    animation: fadeIn 1s ease-out;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                h1 {
                    font-size: 3rem;
                    margin: 0 0 1rem;
                    background: linear-gradient(to bottom right, #38bdf8, #818cf8);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                p {
                    font-size: 1.1rem;
                    color: #94a3b8;
                    line-height: 1.6;
                    margin-bottom: 2rem;
                }
                .badge {
                    display: inline-block;
                    padding: 0.5rem 1rem;
                    background: rgba(56, 189, 248, 0.1);
                    color: #38bdf8;
                    border-radius: 9999px;
                    font-size: 0.875rem;
                    font-weight: 600;
                    margin-bottom: 1.5rem;
                    border: 1px solid rgba(56, 189, 248, 0.2);
                }
                .button-group {
                    display: flex;
                    gap: 1rem;
                    justify-content: center;
                }
                .btn {
                    padding: 0.75rem 1.5rem;
                    border-radius: 12px;
                    text-decoration: none;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    font-size: 0.9rem;
                }
                .btn-primary {
                    background: #38bdf8;
                    color: #020617;
                }
                .btn-primary:hover {
                    background: #7dd3fc;
                    transform: scale(1.05);
                    box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
                }
                .btn-secondary {
                    background: rgba(255, 255, 255, 0.05);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                .btn-secondary:hover {
                    background: rgba(255, 255, 255, 0.1);
                    transform: scale(1.05);
                }
                .status {
                    margin-top: 2rem;
                    font-size: 0.8rem;
                    color: #475569;
                }
                .status span { color: #22c55e; margin-right: 4px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="badge">API Engine v1.0 • Live</div>
                <h1>CareerBuddy AI</h1>
                <p>Welcome to the core engine. This AI service parses resumes, matches jobs, and generates personalized career roadmaps.</p>
                
                <div class="button-group">
                    <a href="/docs" class="btn btn-primary">Interactive API Docs</a>
                    <a href="https://career-buddy-ai-kappa.vercel.app" class="btn btn-secondary">Open Main App</a>
                </div>
                
                <div class="status">
                    <span>●</span> Service Status: Operational
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "ok", "service": "CareerBuddy AI Backend"}

app.include_router(resume_router)
app.include_router(ai_router)