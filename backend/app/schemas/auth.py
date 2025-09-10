"""
Pydantic schemas for authentication endpoints
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re


class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50, description="Username must be 3-50 characters")
    email: str = Field(..., description="Valid email address")
    
    @validator('email')
    def validate_email(cls, v):
        """Basic email validation"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")


class UserLogin(BaseModel):
    """Schema for user login"""
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=1, description="Password is required")
    
    @validator('email')
    def validate_email(cls, v):
        """Basic email validation"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v


class UserResponse(UserBase):
    """Schema for user data in responses (excludes password)"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Schema for authentication response with token"""
    user_id: int
    username: str
    token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    message: str
    details: Optional[dict] = None