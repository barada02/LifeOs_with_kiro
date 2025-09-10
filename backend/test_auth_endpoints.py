"""
Test script for authentication endpoints
"""
import requests
import json
import time
import subprocess
import sys
from threading import Thread


def test_auth_endpoints():
    """Test the authentication endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing authentication endpoints...")
    
    # Test data
    test_user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        # Test health endpoint first
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health")
        print(f"Health check status: {response.status_code}")
        print(f"Health response: {response.json()}")
        
        # Test user registration
        print("\n2. Testing user registration...")
        response = requests.post(f"{base_url}/api/auth/register", json=test_user)
        print(f"Registration status: {response.status_code}")
        
        if response.status_code == 201:
            registration_data = response.json()
            print(f"Registration successful: {registration_data}")
            token = registration_data.get("token")
        else:
            print(f"Registration failed: {response.text}")
            return False
        
        # Test user login
        print("\n3. Testing user login...")
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"Login status: {response.status_code}")
        
        if response.status_code == 200:
            login_response = response.json()
            print(f"Login successful: {login_response}")
            token = login_response.get("token")
        else:
            print(f"Login failed: {response.text}")
            return False
        
        # Test token verification
        print("\n4. Testing token verification...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/api/auth/verify", headers=headers)
        print(f"Token verification status: {response.status_code}")
        
        if response.status_code == 200:
            verify_data = response.json()
            print(f"Token verification successful: {verify_data}")
        else:
            print(f"Token verification failed: {response.text}")
            return False
        
        # Test duplicate registration (should fail)
        print("\n5. Testing duplicate registration...")
        response = requests.post(f"{base_url}/api/auth/register", json=test_user)
        print(f"Duplicate registration status: {response.status_code}")
        
        if response.status_code == 400:
            print("Duplicate registration correctly rejected")
        else:
            print(f"Unexpected response for duplicate registration: {response.text}")
        
        # Test invalid login
        print("\n6. Testing invalid login...")
        invalid_login = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = requests.post(f"{base_url}/api/auth/login", json=invalid_login)
        print(f"Invalid login status: {response.status_code}")
        
        if response.status_code == 401:
            print("Invalid login correctly rejected")
        else:
            print(f"Unexpected response for invalid login: {response.text}")
        
        print("\n✅ All authentication endpoint tests completed successfully!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    # Wait a moment for server to start if needed
    time.sleep(2)
    test_auth_endpoints()