"""
Script to run server and test authentication endpoints
"""
import subprocess
import time
import sys
import os
from threading import Thread
import requests


def run_server():
    """Run the FastAPI server"""
    try:
        subprocess.run([sys.executable, "main.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        pass


def wait_for_server(max_attempts=30):
    """Wait for server to be ready"""
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/api/health", timeout=1)
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except:
            pass
        time.sleep(1)
        print(f"Waiting for server... ({i+1}/{max_attempts})")
    return False


def main():
    """Main function to run tests"""
    print("Starting server and running authentication tests...")
    
    # Start server in background thread
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to be ready
    if not wait_for_server():
        print("❌ Server failed to start within timeout period")
        return False
    
    # Run tests
    from test_auth_endpoints import test_auth_endpoints
    return test_auth_endpoints()


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)