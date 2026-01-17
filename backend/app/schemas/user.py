"""User schemas for API requests/responses."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""

    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""

    username: str | None = None
