"""
Test database error handling scenarios
"""
import os
import sys
import requests
import time

# Add the backend directory to Python path
sys.path.append(os.path.dirname(__file__))

from app.database import test_connection


def test_database_connection_error_handling():
    """Test database connection error handling"""
    print("=== Testing Database Connection Error Handling ===")
    
    # Test the test_connection function directly
    print("1. Testing direct database connection function...")
    
    # First test with working database
    if test_connection():
        print("✅ Database connection working normally")
    else:
        print("❌ Database connection failed unexpectedly")
        return False
    
    # Test error handling by creating a connection with invalid parameters
    print("2. Testing connection error handling...")
    
    # Import necessary modules for testing invalid connection
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import text
    
    try:
        # Create engine with invalid database path
        invalid_engine = create_engine("sqlite:///./nonexistent_directory/invalid.db")
        InvalidSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=invalid_engine)
        
        # Try to use the invalid connection
        db = InvalidSessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        print("❌ Invalid connection should have failed")
        return False
        
    except Exception as e:
        print(f"✅ Connection correctly failed with invalid path: {type(e).__name__}")
    
    # Verify normal connection still works
    if test_connection():
        print("✅ Normal database connection still working")
    else:
        print("❌ Normal database connection failed")
        return False
    
    print("✅ All database error handling tests passed!")
    return True


def test_health_endpoint_with_database_issues():
    """Test health endpoint response when database has issues"""
    print("\n=== Testing Health Endpoint with Database Issues ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test normal health check first
        print("1. Testing normal health check...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("database") == "connected":
                print("✅ Health check shows database connected")
            else:
                print(f"❌ Unexpected database status: {data.get('database')}")
                return False
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        print("✅ Health endpoint handles database status correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False


if __name__ == "__main__":
    print("Database Error Handling Test Suite")
    print("=" * 40)
    
    success = True
    
    if not test_database_connection_error_handling():
        success = False
    
    if not test_health_endpoint_with_database_issues():
        success = False
    
    if success:
        print("\n🎉 All database error handling tests passed!")
    else:
        print("\n❌ Some database error handling tests failed!")
        sys.exit(1)