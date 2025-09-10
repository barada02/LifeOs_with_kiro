"""
Database initialization script for LifeOS
"""
import os
import sqlite3
from app.database import engine, init_database, test_connection
from app.models.user import User  # Import to register the model

def run_schema_sql():
    """
    Execute the schema.sql file to create tables and indexes
    This is an alternative to SQLAlchemy's create_all for explicit schema control
    """
    schema_path = os.path.join(os.path.dirname(__file__), "..", "schema.sql")
    
    if not os.path.exists(schema_path):
        print(f"Schema file not found at: {schema_path}")
        return False
    
    try:
        # Get database URL from engine
        db_url = str(engine.url)
        if db_url.startswith("sqlite:///"):
            db_path = db_url.replace("sqlite:///", "")
            
            # Connect to SQLite database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Read and execute schema.sql
            with open(schema_path, 'r') as schema_file:
                schema_sql = schema_file.read()
                cursor.executescript(schema_sql)
            
            conn.commit()
            conn.close()
            print("Schema SQL executed successfully!")
            return True
        else:
            print("Schema SQL execution only supported for SQLite databases")
            return False
            
    except Exception as e:
        print(f"Error executing schema SQL: {e}")
        return False

def initialize_database():
    """
    Complete database initialization process
    """
    print("Starting database initialization...")
    
    # Initialize using SQLAlchemy (creates tables from models)
    init_database()
    
    # Test connection after initialization
    if not test_connection():
        print("Database connection test failed!")
        return False
    
    # Verify tables were created
    if verify_tables():
        print("Database initialization completed successfully!")
        return True
    else:
        print("Database initialization failed - tables not created properly")
        return False

def verify_tables():
    """
    Verify that required tables exist in the database
    """
    try:
        db_url = str(engine.url)
        if db_url.startswith("sqlite:///"):
            db_path = db_url.replace("sqlite:///", "")
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if users table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='users'
            """)
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                print("✓ Users table exists")
                return True
            else:
                print("✗ Users table not found")
                return False
                
    except Exception as e:
        print(f"Error verifying tables: {e}")
        return False

if __name__ == "__main__":
    initialize_database()