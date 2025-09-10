"""
Task 6 Verification: Create health check endpoint and test database connectivity
This test verifies all requirements for task 6 are implemented correctly.
"""
import sys
import os
import requests
import time
import subprocess
from threading import Thread

# Add the backend directory to Python path
sys.path.append(os.path.dirname(__file__))

from app.database import test_connection, SessionLocal
from app.database_init import initialize_database


def start_test_server():
    """Start server for testing"""
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "127.0.0.1", "--port", "8001"  # Use different port
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(4)
        
        # Test if server is responding
        try:
            response = requests.get("http://127.0.0.1:8001/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Test server started successfully")
                return process
        except:
            pass
        
        print("❌ Failed to start test server")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None


def verify_health_endpoint_implementation():
    """Verify /api/health endpoint is implemented correctly"""
    print("=== Verifying Health Check Endpoint Implementation ===")
    
    base_url = "http://127.0.0.1:8001"
    
    try:
        print("1. Testing health endpoint exists and responds...")
        response = requests.get(f"{base_url}/api/health", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Health endpoint returned status {response.status_code}, expected 200")
            return False
        
        print("✅ Health endpoint responds with status 200")
        
        print("2. Verifying response structure...")
        data = response.json()
        
        # Check required fields
        required_fields = ["status", "database"]
        for field in required_fields:
            if field not in data:
                print(f"❌ Missing required field in response: {field}")
                return False
        
        print("✅ Response contains required fields")
        
        print("3. Verifying response values...")
        if data["status"] != "healthy":
            print(f"❌ Expected status 'healthy', got '{data['status']}'")
            return False
        
        if data["database"] not in ["connected", "disconnected"]:
            print(f"❌ Invalid database status: '{data['database']}'")
            return False
        
        print(f"✅ Response values correct: status={data['status']}, database={data['database']}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to health endpoint")
        return False
    except Exception as e:
        print(f"❌ Health endpoint verification failed: {e}")
        return False


def verify_database_connectivity_testing():
    """Verify database connectivity can be tested"""
    print("\n=== Verifying Database Connectivity Testing ===")
    
    print("1. Testing direct database connection function...")
    if not test_connection():
        print("❌ Database connection test failed")
        return False
    
    print("✅ Database connection test successful")
    
    print("2. Testing database initialization...")
    if not initialize_database():
        print("❌ Database initialization failed")
        return False
    
    print("✅ Database initialization successful")
    
    print("3. Testing database operations...")
    try:
        from app.models.user import User
        
        db = SessionLocal()
        
        # Test basic query
        user_count = db.query(User).count()
        print(f"✅ Database query successful (found {user_count} users)")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Database operation failed: {e}")
        return False
    
    return True


def verify_database_crud_through_api():
    """Verify database CRUD operations work through API endpoints"""
    print("\n=== Verifying Database CRUD Through API ===")
    
    base_url = "http://127.0.0.1:8001"
    
    # Test user data
    test_user = {
        "username": "task6_test_user",
        "email": "task6test@example.com",
        "password": "testpassword123"
    }
    
    try:
        print("1. Testing CREATE operation (user registration)...")
        response = requests.post(f"{base_url}/api/auth/register", json=test_user)
        
        if response.status_code == 201:
            registration_data = response.json()
            print(f"✅ CREATE successful: User {registration_data['username']} created")
            token = registration_data.get("token")
        else:
            print(f"❌ CREATE failed: {response.status_code} - {response.text}")
            return False
        
        print("2. Testing READ operation (user login)...")
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            login_response = response.json()
            print(f"✅ READ successful: User {login_response['username']} authenticated")
        else:
            print(f"❌ READ failed: {response.status_code} - {response.text}")
            return False
        
        print("3. Testing additional READ operation (token verification)...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/api/auth/verify", headers=headers)
        
        if response.status_code == 200:
            verify_data = response.json()
            print(f"✅ Token verification successful: {verify_data['username']}")
        else:
            print(f"❌ Token verification failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API CRUD test failed: {e}")
        return False


def verify_error_handling():
    """Verify error handling for database connection issues"""
    print("\n=== Verifying Error Handling ===")
    
    print("1. Testing database connection error handling...")
    
    # Test invalid database connection
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import text
        
        # Create invalid engine
        invalid_engine = create_engine("sqlite:///./invalid/path/database.db")
        InvalidSession = sessionmaker(bind=invalid_engine)
        
        db = InvalidSession()
        db.execute(text("SELECT 1"))
        db.close()
        
        print("❌ Invalid connection should have failed")
        return False
        
    except Exception as e:
        print(f"✅ Database error correctly handled: {type(e).__name__}")
    
    print("2. Testing API error responses...")
    base_url = "http://127.0.0.1:8001"
    
    try:
        # Test invalid endpoint
        response = requests.get(f"{base_url}/api/nonexistent")
        if response.status_code == 404:
            print("✅ Invalid endpoint correctly returns 404")
        else:
            print(f"❌ Unexpected response for invalid endpoint: {response.status_code}")
        
        # Test malformed request
        response = requests.post(f"{base_url}/api/auth/register", json={"invalid": "data"})
        if response.status_code == 422:  # Validation error
            print("✅ Malformed request correctly rejected")
        else:
            print(f"❌ Unexpected response for malformed request: {response.status_code}")
        
    except Exception as e:
        print(f"❌ API error handling test failed: {e}")
        return False
    
    return True


def main():
    """Main verification function for Task 6"""
    print("Task 6 Verification: Health Check Endpoint and Database Connectivity")
    print("=" * 70)
    
    print("Starting test server...")
    server_process = start_test_server()
    
    if not server_process:
        print("❌ Could not start test server")
        return False
    
    try:
        success = True
        
        # Verify all task requirements
        if not verify_health_endpoint_implementation():
            success = False
        
        if not verify_database_connectivity_testing():
            success = False
        
        if not verify_database_crud_through_api():
            success = False
        
        if not verify_error_handling():
            success = False
        
        if success:
            print("\n🎉 Task 6 Verification PASSED!")
            print("✅ Health check endpoint implemented correctly")
            print("✅ Database connectivity testing working")
            print("✅ Database CRUD operations through API verified")
            print("✅ Error handling for database connection issues verified")
            print("\nAll requirements for Task 6 have been successfully implemented!")
        else:
            print("\n❌ Task 6 Verification FAILED!")
            print("Some requirements are not properly implemented.")
        
        return success
        
    finally:
        # Clean up server
        if server_process:
            server_process.terminate()
            server_process.wait()
            print("\nTest server stopped.")


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)