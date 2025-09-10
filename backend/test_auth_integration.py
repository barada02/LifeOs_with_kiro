"""
Integration test for authentication endpoints with database
"""
from fastapi.testclient import TestClient
from app.database import SessionLocal, init_database
from app.models.user import User
from main import app
import os


def test_auth_integration():
    """Test authentication endpoints with database"""
    
    # Initialize database
    init_database()
    
    print("Running authentication integration tests...")
    
    # Test data
    test_user = {
        "username": "integrationtest",
        "email": "integration@test.com",
        "password": "testpassword123"
    }
    
    try:
        # Clean up any existing test user
        db = SessionLocal()
        existing_user = db.query(User).filter(User.email == test_user["email"]).first()
        if existing_user:
            db.delete(existing_user)
            db.commit()
        db.close()
        
        # Create test client
        client = TestClient(app)
        
        # Test 1: Health check
        print("\n1. Testing health endpoint...")
        response = client.get("/api/health")
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["status"] == "healthy"
        print("✅ Health check passed")
        
        # Test 2: User registration
        print("\n2. Testing user registration...")
        response = client.post("/api/auth/register", json=test_user)
        assert response.status_code == 201
        registration_data = response.json()
        assert "token" in registration_data
        assert registration_data["username"] == test_user["username"]
        token = registration_data["token"]
        print("✅ User registration passed")
        
        # Test 3: User login
        print("\n3. Testing user login...")
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        login_response = response.json()
        assert "token" in login_response
        assert login_response["username"] == test_user["username"]
        print("✅ User login passed")
        
        # Test 4: Token verification
        print("\n4. Testing token verification...")
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/verify", headers=headers)
        assert response.status_code == 200
        verify_data = response.json()
        assert verify_data["valid"] == True
        assert verify_data["username"] == test_user["username"]
        print("✅ Token verification passed")
        
        # Test 5: Duplicate registration
        print("\n5. Testing duplicate registration...")
        response = client.post("/api/auth/register", json=test_user)
        assert response.status_code == 400
        error_data = response.json()
        assert "error" in error_data["detail"]
        print("✅ Duplicate registration correctly rejected")
        
        # Test 6: Invalid login
        print("\n6. Testing invalid login...")
        invalid_login = {
            "email": test_user["email"],
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", json=invalid_login)
        assert response.status_code == 401
        print("✅ Invalid login correctly rejected")
        
        # Test 7: Invalid token
        print("\n7. Testing invalid token...")
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/verify", headers=invalid_headers)
        assert response.status_code == 401
        print("✅ Invalid token correctly rejected")
        
        print("\n🎉 All integration tests passed!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test assertion failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    finally:
        # Clean up test user
        try:
            db = SessionLocal()
            test_user_obj = db.query(User).filter(User.email == test_user["email"]).first()
            if test_user_obj:
                db.delete(test_user_obj)
                db.commit()
            db.close()
        except:
            pass


if __name__ == "__main__":
    success = test_auth_integration()
    if not success:
        exit(1)