"""
Pydantic schemas for Pet Store API responses
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .models import PetStatus, OrderStatus, PetCategory

class PetResponse(BaseModel):
    """Schema for pet API responses"""
    id: int = Field(..., example=1)
    name: str = Field(..., example="Buddy")
    category: PetCategory = Field(..., example="dog")
    status: PetStatus = Field(..., example="available")
    tags: List[str] = Field(..., example=["friendly", "house-trained"])
    price: float = Field(..., example=299.99)
    description: Optional[str] = Field(None, example="A friendly golden retriever")
    photo_urls: List[str] = Field(..., example=["https://example.com/photo1.jpg"])
    created_at: datetime
    updated_at: Optional[datetime] = None

class OrderResponse(BaseModel):
    """Schema for order API responses"""
    id: int = Field(..., example=1)
    pet_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    quantity: int = Field(..., example=1)
    ship_date: Optional[datetime] = None
    status: OrderStatus = Field(..., example="placed")
    complete: bool = Field(..., example=False)
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserResponse(BaseModel):
    """Schema for user API responses"""
    id: int = Field(..., example=1)
    username: str = Field(..., example="johndoe")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email: str = Field(..., example="john@example.com")
    phone: Optional[str] = Field(None, example="+1234567890")
    user_status: int = Field(..., example=1)
    created_at: datetime
    updated_at: Optional[datetime] = None

class HealthResponse(BaseModel):
    """Schema for health check responses"""
    message: str = Field(..., example="Service is healthy")
    status: str = Field(..., example="healthy")
    version: str = Field(..., example="1.0.0")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ApiResponse(BaseModel):
    """Generic API response schema"""
    code: int = Field(..., example=200)
    type: str = Field(..., example="success")
    message: str = Field(..., example="Operation completed successfully")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    code: int = Field(..., example=400)
    type: str = Field(..., example="error")
    message: str = Field(..., example="Invalid input")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
