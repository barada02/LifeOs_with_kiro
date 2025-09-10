"""
Verify that all authentication endpoints are properly registered
"""
from main import app
from fastapi.routing import APIRoute


def verify_endpoints():
    """Verify that authentication endpoints are registered"""
    
    print("Verifying authentication endpoints registration...")
    
    # Get all routes
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })
    
    # Expected authentication endpoints
    expected_endpoints = [
        {"path": "/api/auth/register", "methods": ["POST"]},
        {"path": "/api/auth/login", "methods": ["POST"]},
        {"path": "/api/auth/verify", "methods": ["GET"]},
        {"path": "/api/health", "methods": ["GET"]},
    ]
    
    print("\nRegistered routes:")
    for route in routes:
        print(f"  {route['methods']} {route['path']} ({route['name']})")
    
    print("\nChecking expected endpoints:")
    all_found = True
    
    for expected in expected_endpoints:
        found = False
        for route in routes:
            if (route["path"] == expected["path"] and 
                any(method in route["methods"] for method in expected["methods"])):
                found = True
                break
        
        if found:
            print(f"✅ {expected['methods'][0]} {expected['path']} - Found")
        else:
            print(f"❌ {expected['methods'][0]} {expected['path']} - Missing")
            all_found = False
    
    if all_found:
        print("\n🎉 All expected endpoints are registered!")
        return True
    else:
        print("\n❌ Some endpoints are missing!")
        return False


if __name__ == "__main__":
    success = verify_endpoints()
    if not success:
        exit(1)