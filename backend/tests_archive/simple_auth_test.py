"""
Simple authentication test without TestClient
ARCHIVED: One-time test for authentication functionality verification
"""
from app.database import SessionLocal, init_database
from app.models.user import User
from app.services.auth import AuthService
from app.schemas.auth import UserCreate
import json
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def test_auth_functionality():
    """Test authentication functionality directly"""
    
    print("Testing authentication functionality...")
    
    # Initialize database
    init_database()
    
    # Test data
    test_user_data = UserCreate(
        username="testuser123",
        email="test123@example.com",
        password="testpassword123"
    )
    
    try:
        db = SessionLocal()
        
        # Clean up any existing test user
        existing_user = db.query(User).filter(User.email == test_user_data.email).first()
        if existing_user:
            db.delete(existing_user)
            db.commit()
        
        print("\n1. Testing password hashing...")
        hashed_password = AuthService.hash_password(test_user_data.password)
        assert len(hashed_password) > 0
        print("✅ Password hashing works")
        
        print("\n2. Testing password verification...")
        is_valid = AuthService.verify_password(test_user_data.password, hashed_password)
        assert is_valid == True
        print("✅ Password verification works")
        
        print("\n3. Testing user creation...")
        new_user = AuthService.create_user(db, test_user_data)
        assert new_user.id is not None
        assert new_user.username == test_user_data.username
        assert new_user.email == test_user_data.email
        print("✅ User creation works")
        
        print("\n4. Testing user authentication...")
        authenticated_user = AuthService.authenticate_user(db, test_user_data.email, test_user_data.password)
        assert authenticated_user is not None
        assert authenticated_user.id == new_user.id
        print("✅ User authentication works")
        
        print("\n5. Testing JWT token creation...")
        token_data = {"user_id": new_user.id, "username": new_user.username}
        token = AuthService.create_access_token(token_data)
        assert len(token) > 0
        print("✅ JWT token creation works")
        
        print("\n6. Testing JWT token verification...")
        decoded_token = AuthService.verify_token(token)
        assert decoded_token is not None
        assert decoded_token.user_id == new_user.id
        assert decoded_token.username == new_user.username
        print("✅ JWT token verification works")
        
        print("\n7. Testing duplicate user detection...")
        existing_email_user = AuthService.get_user_by_email(db, test_user_data.email)
        assert existing_email_user is not None
        existing_username_user = AuthService.get_user_by_username(db, test_user_data.username)
        assert existing_username_user is not None
        print("✅ Duplicate user detection works")
        
        print("\n8. Testing invalid authentication...")
        invalid_auth = AuthService.authenticate_user(db, test_user_data.email, "wrongpassword")
        assert invalid_auth is None
        print("✅ Invalid authentication correctly rejected")
        
        print("\n9. Testing invalid token...")
        invalid_token_data = AuthService.verify_token("invalid_token")
        assert invalid_token_data is None
        print("✅ Invalid token correctly rejected")
        
        print("\n🎉 All authentication functionality tests passed!")
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
            test_user_obj = db.query(User).filter(User.email == test_user_data.email).first()
            if test_user_obj:
                db.delete(test_user_obj)
                db.commit()
            db.close()
        except:
            pass


if __name__ == "__main__":
    success = test_auth_functionality()
    if not success:
        exit(1)