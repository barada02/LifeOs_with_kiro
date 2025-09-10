"""
Database testing script for LifeOS
Tests database connection and basic CRUD operations
"""
import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(__file__))

from app.database import SessionLocal, test_connection, init_database
from app.models.user import User
from app.database_init import initialize_database

def test_database_operations():
    """
    Test basic database operations (CRUD)
    """
    print("\n=== Testing Database Operations ===")
    
    # Test connection
    print("1. Testing database connection...")
    if not test_connection():
        print("❌ Database connection failed!")
        return False
    print("✅ Database connection successful!")
    
    # Initialize database
    print("\n2. Initializing database...")
    if not initialize_database():
        print("❌ Database initialization failed!")
        return False
    print("✅ Database initialization successful!")
    
    # Test CRUD operations
    print("\n3. Testing CRUD operations...")
    
    db = SessionLocal()
    try:
        # CREATE - Insert a test user
        print("   Testing CREATE operation...")
        test_user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_here"
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"   ✅ User created with ID: {test_user.id}")
        
        # READ - Query the user
        print("   Testing READ operation...")
        retrieved_user = db.query(User).filter(User.username == "testuser").first()
        if retrieved_user:
            print(f"   ✅ User retrieved: {retrieved_user}")
            print(f"   User dict: {retrieved_user.to_dict()}")
        else:
            print("   ❌ User not found!")
            return False
        
        # UPDATE - Modify the user
        print("   Testing UPDATE operation...")
        retrieved_user.email = "updated@example.com"
        db.commit()
        db.refresh(retrieved_user)
        print(f"   ✅ User updated: {retrieved_user.email}")
        
        # READ ALL - Query all users
        print("   Testing READ ALL operation...")
        all_users = db.query(User).all()
        print(f"   ✅ Total users in database: {len(all_users)}")
        
        # DELETE - Remove the test user
        print("   Testing DELETE operation...")
        db.delete(retrieved_user)
        db.commit()
        
        # Verify deletion
        deleted_user = db.query(User).filter(User.username == "testuser").first()
        if deleted_user is None:
            print("   ✅ User deleted successfully!")
        else:
            print("   ❌ User deletion failed!")
            return False
            
    except Exception as e:
        print(f"   ❌ Database operation failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    print("\n✅ All database tests passed!")
    return True

def test_database_constraints():
    """
    Test database constraints (unique username, email)
    """
    print("\n=== Testing Database Constraints ===")
    
    db = SessionLocal()
    try:
        # Create first user
        user1 = User(
            username="constrainttest",
            email="constraint@example.com",
            password_hash="hash1"
        )
        db.add(user1)
        db.commit()
        print("✅ First user created successfully")
        
        # Try to create user with duplicate username
        try:
            user2 = User(
                username="constrainttest",  # Duplicate username
                email="different@example.com",
                password_hash="hash2"
            )
            db.add(user2)
            db.commit()
            print("❌ Duplicate username constraint failed!")
            return False
        except Exception as e:
            db.rollback()
            print("✅ Username uniqueness constraint working")
        
        # Try to create user with duplicate email
        try:
            user3 = User(
                username="differentuser",
                email="constraint@example.com",  # Duplicate email
                password_hash="hash3"
            )
            db.add(user3)
            db.commit()
            print("❌ Duplicate email constraint failed!")
            return False
        except Exception as e:
            db.rollback()
            print("✅ Email uniqueness constraint working")
        
        # Clean up
        db.delete(user1)
        db.commit()
        
    except Exception as e:
        print(f"❌ Constraint test failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    print("✅ All constraint tests passed!")
    return True

if __name__ == "__main__":
    print("LifeOS Database Test Suite")
    print("=" * 40)
    
    success = True
    
    # Run basic operations test
    if not test_database_operations():
        success = False
    
    # Run constraints test
    if not test_database_constraints():
        success = False
    
    if success:
        print("\n🎉 All database tests completed successfully!")
        print("Database setup is working correctly.")
    else:
        print("\n❌ Some database tests failed!")
        print("Please check the error messages above.")
        sys.exit(1)