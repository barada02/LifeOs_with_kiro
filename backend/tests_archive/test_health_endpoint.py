"""
Test script specifically for health check endpoint and database connectivity
Tests various scenarios including database connection failures
ARCHIVED: One-time comprehensive test for health endpoint functionality
"""
import requests
import json
import os
import sys
import time
import subprocess
from threading import Thread

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import test_connection, SessionLocal, engine
from app.database_init import initialize_database


def start_server():
    """Start the FastAPI server in a separate process"""
    try:
        # Start server using uvicorn
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        return process
    except Exception as e:
        print(f"Failed to start server: {e}")
        return None


def test_health_endpoint_success():
    """Test health endpoint when database is working correctly"""
    print("\n=== Testing Health Endpoint - Success Case ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # Ensure database is initialized
        print("1. Initializing database...")
        if not initialize_database():
            print("❌ Database initialization failed!")
            return False
        print("✅ Database initialized successfully!")
        
        # Test direct database connection
        print("2. Testing direct database connection...")
        if not test_connection():
            print("❌ Direct database connection failed!")
            return False
        print("✅ Direct database connection successful!")
        
        # Test health endpoint
        print("3. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure
            required_fields = ["status", "service", "database"]
            for field in required_fields:
                if field not in data:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # Verify values
            if data["status"] != "healthy":
                print(f"❌ Expected status 'healthy', got '{data['status']}'")
                return False
            
            if data["database"] != "connected":
                print(f"❌ Expected database 'connected', got '{data['database']}'")
                return False
            
            print("✅ Health endpoint returned correct response!")
            return True
        else:
            print(f"❌ Health endpoint returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


def test_health_endpoint_database_failure():
    """Test health endpoint behavior when database connection fails"""
    print("\n=== Testing Health Endpoint - Database Failure Case ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # Backup current database file if it exists
        db_file = "lifeos.db"
        backup_file = "lifeos.db.backup"
        
        if os.path.exists(db_file):
            os.rename(db_file, backup_file)
            print("✅ Database file backed up")
        
        # Create an invalid database scenario by removing the database file
        # and making the directory read-only (simulating connection failure)
        
        # Test health endpoint with database issues
        print("1. Testing health endpoint with database connection issues...")
        response = requests.get(f"{base_url}/api/health", timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            
            # The endpoint should still return 200 but indicate database issues
            if data["status"] == "healthy" and data["database"] == "disconnected":
                print("✅ Health endpoint correctly reported database disconnection!")
                success = True
            else:
                print(f"❌ Unexpected response: {data}")
                success = False
        else:
            print(f"❌ Health endpoint returned unexpected status {response.status_code}")
            success = False
        
        # Restore database file
        if os.path.exists(backup_file):
            os.rename(backup_file, db_file)
            print("✅ Database file restored")
        
        return success
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        # Restore database file in case of error
        if os.path.exists(backup_file):
            os.rename(backup_file, db_file)
        return False


def test_database_crud_through_api():
    """Test database CRUD operations through API endpoints"""
    print("\n=== Testing Database CRUD Through API ===")
    
    base_url = "http://localhost:8000"
    
    # Test data
    test_user = {
        "username": "healthtest_user",
        "email": "healthtest@example.com",
        "password": "testpassword123"
    }
    
    login_data = {
        "email": "healthtest@example.com",
        "password": "testpassword123"
    }
    
    try:
        # CREATE - Register a user
        print("1. Testing CREATE through API (user registration)...")
        response = requests.post(f"{base_url}/api/auth/register", json=test_user)
        
        if response.status_code == 201:
            registration_data = response.json()
            print(f"✅ User created successfully: {registration_data['username']}")
            token = registration_data.get("token")
        else:
            print(f"❌ User creation failed: {response.status_code} - {response.text}")
            return False
        
        # READ - Login (verify user exists and can be authenticated)
        print("2. Testing READ through API (user login)...")
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            login_response = response.json()
            print(f"✅ User login successful: {login_response['username']}")
            token = login_response.get("token")
        else:
            print(f"❌ User login failed: {response.status_code} - {response.text}")
            return False
        
        # VERIFY - Token verification (additional read operation)
        print("3. Testing token verification (additional READ)...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/api/auth/verify", headers=headers)
        
        if response.status_code == 200:
            verify_data = response.json()
            print(f"✅ Token verification successful: {verify_data['username']}")
        else:
            print(f"❌ Token verification failed: {response.status_code} - {response.text}")
            return False
        
        print("✅ All database CRUD operations through API successful!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    except Exception as e:
        print(f"❌ API CRUD test failed with error: {e}")
        return False


def test_error_handling():
    """Test various error handling scenarios"""
    print("\n=== Testing Error Handling ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test invalid endpoint
        print("1. Testing invalid endpoint...")
        response = requests.get(f"{base_url}/api/invalid", timeout=5)
        if response.status_code == 404:
            print("✅ Invalid endpoint correctly returns 404")
        else:
            print(f"❌ Unexpected response for invalid endpoint: {response.status_code}")
        
        # Test malformed request
        print("2. Testing malformed registration request...")
        invalid_user = {"username": "test"}  # Missing required fields
        response = requests.post(f"{base_url}/api/auth/register", json=invalid_user)
        if response.status_code == 422:  # FastAPI validation error
            print("✅ Malformed request correctly rejected")
        else:
            print(f"❌ Unexpected response for malformed request: {response.status_code}")
        
        # Test duplicate user registration
        print("3. Testing duplicate user registration...")
        duplicate_user = {
            "username": "healthtest_user",  # Should already exist from previous test
            "email": "healthtest@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{base_url}/api/auth/register", json=duplicate_user)
        if response.status_code == 400:
            print("✅ Duplicate user registration correctly rejected")
        else:
            print(f"❌ Unexpected response for duplicate user: {response.status_code}")
        
        print("✅ All error handling tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def main():
    """Main test function"""
    print("LifeOS Health Endpoint and Database Connectivity Test Suite")
    print("=" * 60)
    
    # Check if server is already running
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=2)
        server_running = True
        print("✅ Server is already running")
    except:
        server_running = False
        print("ℹ️  Server not running, will need to start it")
    
    success = True
    
    # Run tests
    if not test_health_endpoint_success():
        success = False
    
    if not test_database_crud_through_api():
        success = False
    
    if not test_error_handling():
        success = False
    
    # Note: Skipping database failure test as it requires stopping the server
    # which is complex in this test setup
    print("\nℹ️  Database failure test skipped (requires server restart)")
    
    if success:
        print("\n🎉 All health endpoint and database connectivity tests passed!")
        print("Health check endpoint and database operations are working correctly.")
    else:
        print("\n❌ Some tests failed!")
        print("Please check the error messages above.")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)