"""
Database configuration and connection setup for LifeOS
"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lifeos.db")

# Create SQLAlchemy engine
# For SQLite, we use StaticPool to ensure connection persistence
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    poolclass=StaticPool,
    echo=False  # Set to True for SQL query logging during development
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Metadata for database operations
metadata = MetaData()

def get_database():
    """
    Dependency function to get database session
    Yields a database session and ensures it's closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all tables defined in the models
    """
    Base.metadata.create_all(bind=engine)

def init_database():
    """
    Initialize the database by creating all tables
    """
    print("Initializing database...")
    create_tables()
    print("Database initialized successfully!")

def test_connection():
    """
    Test database connection
    Returns True if connection is successful, False otherwise
    """
    try:
        from sqlalchemy import text
        db = SessionLocal()
        # Execute a simple query to test connection
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False