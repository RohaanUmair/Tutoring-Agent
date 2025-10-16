# src/api/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

app = FastAPI(title="Voice Math Tutor API")

# CORS for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(src_dir) / "web" / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
else:
    print(f"Warning: Static path not found: {static_path}")

# Import routes
from api.routes import voice_routes, agent_routes, quiz_routes

app.include_router(voice_routes.router, prefix="/api/voice", tags=["voice"])
app.include_router(agent_routes.router, prefix="/api/agent", tags=["agent"])
app.include_router(quiz_routes.router, prefix="/api/quiz", tags=["quiz"])  # Add this line

# Serve main page
@app.get("/", response_class=HTMLResponse)
async def root():
    template_path = Path(src_dir) / "web" / "templates" / "index.html"
    if not template_path.exists():
        return "<h1>Template not found. Please create web/templates/index.html</h1>"
    
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)