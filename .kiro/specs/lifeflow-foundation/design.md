# Design Document

## Overview

The LifeOS Foundation design establishes a modern full-stack architecture using React + Vite for the frontend, FastAPI for the backend, and SQLite with SQLAlchemy for data persistence. The design prioritizes simplicity, rapid development, and a solid foundation for future feature expansion.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    HTTP/REST API    ┌─────────────────┐    SQLAlchemy ORM    ┌─────────────────┐
│   React + Vite  │ ◄─────────────────► │     FastAPI     │ ◄──────────────────► │  SQLite Database │
│    Frontend     │                     │     Backend     │                      │                 │
│   (Port 5173)   │                     │   (Port 8000)   │                      │   (lifeos.db)   │
└─────────────────┘                     └─────────────────┘                      └─────────────────┘
```

### Technology Stack

**Frontend:**
- React 18 with TypeScript
- Vite for build tooling and dev server
- Axios for HTTP client
- React Router for navigation
- Tailwind CSS for styling

**Backend:**
- FastAPI with Python 3.9+
- SQLAlchemy 2.0 for ORM
- Pydantic for data validation
- Uvicorn as ASGI server
- Python virtual environment for dependency isolation

**Database:**
- SQLite for local development
- SQLAlchemy migrations for schema management
- Initial schema.sql for database setup

## Components and Interfaces

### Frontend Components

#### 1. App Component
- Main application wrapper
- Handles routing between Landing and Dashboard
- Manages global authentication state

#### 2. Landing Page Component
- Welcome section with LifeOS branding
- Toggle between Login and Signup forms
- Basic form validation and error display

#### 3. Auth Forms Components
- **LoginForm**: Email and password fields
- **SignupForm**: Username, email, and password fields
- Form validation and submission handling

#### 4. Dashboard Component
- Welcome message with user information
- Logout functionality
- Placeholder for future feature navigation

#### 5. API Service
- Centralized HTTP client configuration
- Authentication token management
- API endpoint abstractions

### Backend API Endpoints

#### Authentication Endpoints
```
POST /api/auth/register
- Body: { username: str, email: str, password: str }
- Response: { user_id: int, username: str, token: str }

POST /api/auth/login
- Body: { email: str, password: str }
- Response: { user_id: int, username: str, token: str }

GET /api/auth/verify
- Headers: Authorization: Bearer <token>
- Response: { user_id: int, username: str, valid: bool }
```

#### Health Check Endpoint
```
GET /api/health
- Response: { status: "healthy", database: "connected" }
```

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Data Models

### Frontend Models (TypeScript)

```typescript
interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthResponse {
  user_id: number;
  username: string;
  token: string;
}

interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}
```

### Backend Models (Pydantic)

```python
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

class AuthResponse(BaseModel):
    user_id: int
    username: str
    token: str
```

### SQLAlchemy Models

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## Error Handling

### Frontend Error Handling
- Form validation errors displayed inline
- API errors shown as toast notifications or alert messages
- Network errors handled with retry mechanisms
- Loading states during API calls

### Backend Error Handling
- HTTP status codes for different error types
- Structured error responses with detail messages
- Input validation using Pydantic
- Database constraint error handling

### Error Response Format
```json
{
  "error": "validation_error",
  "message": "Email already exists",
  "details": {
    "field": "email",
    "code": "unique_constraint"
  }
}
```

## Testing Strategy

### Frontend Testing
- Component unit tests using React Testing Library
- Integration tests for authentication flow
- API service mocking for isolated testing
- E2E tests for critical user paths

### Backend Testing
- Unit tests for API endpoints using pytest
- Database integration tests with test database
- Authentication middleware testing
- API contract testing

### Database Testing
- Schema validation tests
- Migration testing
- Data integrity constraints testing
- Performance testing for basic operations

## Development Workflow

### Project Structure
```
lifeos/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── types/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   └── main.py
│   ├── requirements.txt
│   └── schema.sql
└── README.md
```

### Development Setup Steps
1. Create project directories and virtual environment
2. Initialize React + Vite frontend with TypeScript
3. Set up FastAPI backend with SQLAlchemy
4. Create database schema and initial migration
5. Implement basic authentication endpoints
6. Build frontend authentication components
7. Test full-stack data flow
8. Implement basic dashboard and routing

### Environment Configuration
- Frontend: Environment variables for API base URL
- Backend: Database URL and JWT secret configuration
- Development: Local SQLite database file
- CORS configuration for frontend-backend communication

## Security Considerations

### Authentication
- Simple JWT token-based authentication
- Password hashing using bcrypt
- Token expiration and refresh (future enhancement)
- Basic input validation and sanitization

### Data Protection
- SQL injection prevention through SQLAlchemy ORM
- XSS protection through React's built-in escaping
- CORS configuration for API access control
- Environment variable protection for secrets

## Performance Considerations

### Frontend Performance
- Vite's fast development server and HMR
- Code splitting for future feature modules
- Optimized bundle size with tree shaking
- Efficient state management for authentication

### Backend Performance
- FastAPI's async capabilities for future scaling
- SQLAlchemy connection pooling
- Efficient database queries with proper indexing
- Response caching for static data (future enhancement)

### Database Performance
- Primary key indexing on users table
- Unique constraints for username and email
- Prepared statements through SQLAlchemy
- Database file optimization for SQLite