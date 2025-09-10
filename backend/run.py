#!/usr/bin/env python3
"""
Development server runner for LifeOS FastAPI backend
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting LifeOS API Development Server...")
    print("📍 Server URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/api/health")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )