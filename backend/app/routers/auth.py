"""
Authentication router with registration and login endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_database
from app.schemas.auth import UserCreate, UserLogin, AuthResponse, ErrorResponse, TokenData
from app.services.auth import AuthService
from app.models.user import User
from typing import Optional


router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_database)
):
    """
    Register a new user account
    
    Args:
        user_data: User registration data (username, email, password)
        db: Database session
        
    Returns:
        AuthResponse with user info and JWT token
        
    Raises:
        HTTPException: If username or email already exists
    """
    try:
        # Check if user already exists
        existing_user_email = AuthService.get_user_by_email(db, user_data.email)
        if existing_user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": "Email already registered",
                    "details": {"field": "email", "code": "unique_constraint"}
                }
            )
        
        existing_user_username = AuthService.get_user_by_username(db, user_data.username)
        if existing_user_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": "Username already taken",
                    "details": {"field": "username", "code": "unique_constraint"}
                }
            )
        
        # Create new user
        new_user = AuthService.create_user(db, user_data)
        
        # Generate JWT token
        token_data = {"user_id": new_user.id, "username": new_user.username}
        access_token = AuthService.create_access_token(data=token_data)
        
        return AuthResponse(
            user_id=new_user.id,
            username=new_user.username,
            token=access_token
        )
        
    except IntegrityError as e:
        db.rollback()
        # Handle database constraint violations
        if "username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": "Username already taken",
                    "details": {"field": "username", "code": "unique_constraint"}
                }
            )
        elif "email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": "Email already registered",
                    "details": {"field": "email", "code": "unique_constraint"}
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "database_error",
                    "message": "Failed to create user account",
                    "details": None
                }
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred",
                "details": None
            }
        )


@router.post("/login", response_model=AuthResponse)
async def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_database)
):
    """
    Authenticate user and return JWT token
    
    Args:
        login_data: User login credentials (email, password)
        db: Database session
        
    Returns:
        AuthResponse with user info and JWT token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        # Authenticate user
        user = AuthService.authenticate_user(db, login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "authentication_error",
                    "message": "Invalid email or password",
                    "details": None
                }
            )
        
        # Generate JWT token
        token_data = {"user_id": user.id, "username": user.username}
        access_token = AuthService.create_access_token(data=token_data)
        
        return AuthResponse(
            user_id=user.id,
            username=user.username,
            token=access_token
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred during login",
                "details": None
            }
        )


@router.get("/verify")
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database)
):
    """
    Verify JWT token and return user information
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        User information if token is valid
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        # Verify token
        token_data = AuthService.verify_token(credentials.credentials)
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "authentication_error",
                    "message": "Invalid or expired token",
                    "details": None
                }
            )
        
        # Get user from database
        user = db.query(User).filter(User.id == token_data.user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "authentication_error",
                    "message": "User not found",
                    "details": None
                }
            )
        
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "valid": True
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred during token verification",
                "details": None
            }
        )