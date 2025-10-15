# src/run_voice_app.py
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Voice Math Tutor...")
    print("📍 Open your browser to: http://localhost:8000")
    print("🎤 Make sure to allow microphone access!")
    print("-" * 50)
    
    # Run without reload to avoid the warning
    uvicorn.run(
        "api.main:app",  # Import string instead of app object
        host="0.0.0.0",
        port=8000,
        reload=True  # Now this will work
    )