from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import get_database, test_connection, init_database
from app.models.user import User
from app.routers import auth

# Create FastAPI app instance
app = FastAPI(
    title="LifeOS API",
    description="Backend API for LifeOS productivity and life management application",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication router
app.include_router(auth.router)

@app.get("/")
async def root():
    """Root endpoint to verify API is running"""
    return {"message": "LifeOS API is running"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint with database connectivity check"""
    db_status = "connected" if test_connection() else "disconnected"
    return {
        "status": "healthy", 
        "service": "lifeos-api",
        "database": db_status
    }

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    print("Initializing database...")
    init_database()
    print("Database initialization complete!")

if __name__ == "__main__":
    print("Starting LifeOS API server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)