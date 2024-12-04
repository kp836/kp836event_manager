from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re


from app.utils.nickname_gen import generate_nickname

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    """Validate URL format."""
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise ValueError(
            "Invalid URL format. URLs must start with 'http://' or 'https://' and be a valid web address."
        )
    return url


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname(), description="Nickname must contain only alphanumeric characters, underscores, or hyphens.")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.", description="Bio must not exceed 250 characters.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg", description="Profile picture URL must start with 'http://' or 'https://'.")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe", description="LinkedIn profile URL must start with 'http://' or 'https://'.")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe", description="Github profile URL must start with 'http://' or https://'.")

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)
 
    @validator("bio", pre=True, always=True)
    def validate_bio(cls, value):
        """Ensure bio does not exceed 250 characters."""
        if value and len(value) > 250:
            raise ValueError(
                "Bio must not exceed 250 characters. Please provide a concise description."
            )
        return value
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    nickname: str = Field(max_length=50, description="Nickname must be unique and not exceed 50 characters.")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234", description="Password must be strong and secure.")

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, max_length=20, pattern=r'^[a-zA-Z0-9](?:[a-zA-Z0-9-_]*[a-zA-Z0-9])?$', example="john_doe123", description="Nickname must be 3-20 characters long and contain only alphanumeric characters, underscores, or hyphens.")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        """Ensure at least one field is provided for updates."""
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED", description="User role indicating the access level.")
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname(), description="Nickname of the user.")    
    is_professional: Optional[bool] = Field(default=False, example=True, descripton="Indicates if the user is a professional.")

class LoginRequest(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., example=[{
        "id": uuid.uuid4(), "nickname": generate_nickname(), "email": "john.doe@example.com",
        "first_name": "John", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "last_name": "Doe", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "profile_picture_url": "https://example.com/profiles/john.jpg", 
        "linkedin_profile_url": "https://linkedin.com/in/johndoe", 
        "github_profile_url": "https://github.com/johndoe"
    }], description="List of users with their profiles.")
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)