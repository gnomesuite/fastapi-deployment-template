"""
Data models for the Pet Store API
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PetStatus(str, Enum):
    """Pet status enumeration"""
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"

class OrderStatus(str, Enum):
    """Order status enumeration"""
    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PetCategory(str, Enum):
    """Pet category enumeration"""
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    FISH = "fish"
    REPTILE = "reptile"
    OTHER = "other"

class Pet(BaseModel):
    """Pet model for internal use"""
    id: int
    name: str = Field(..., min_length=1, max_length=100, example="Buddy")
    category: PetCategory = Field(..., example="dog")
    status: PetStatus = Field(default=PetStatus.AVAILABLE, example="available")
    tags: List[str] = Field(default=[], example=["friendly", "house-trained"])
    price: float = Field(..., gt=0, example=299.99)
    description: Optional[str] = Field(None, max_length=1000, example="A friendly golden retriever")
    photo_urls: List[str] = Field(default=[], example=["https://example.com/photo1.jpg"])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class PetCreate(BaseModel):
    """Model for creating a new pet"""
    name: str = Field(..., min_length=1, max_length=100, example="Buddy")
    category: PetCategory = Field(..., example="dog")
    status: PetStatus = Field(default=PetStatus.AVAILABLE, example="available")
    tags: List[str] = Field(default=[], example=["friendly", "house-trained"])
    price: float = Field(..., gt=0, example=299.99)
    description: Optional[str] = Field(None, max_length=1000, example="A friendly golden retriever")
    photo_urls: List[str] = Field(default=[], example=["https://example.com/photo1.jpg"])

class PetUpdate(BaseModel):
    """Model for updating an existing pet"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Buddy")
    category: Optional[PetCategory] = Field(None, example="dog")
    status: Optional[PetStatus] = Field(None, example="available")
    tags: Optional[List[str]] = Field(None, example=["friendly", "house-trained"])
    price: Optional[float] = Field(None, gt=0, example=299.99)
    description: Optional[str] = Field(None, max_length=1000, example="A friendly golden retriever")
    photo_urls: Optional[List[str]] = Field(None, example=["https://example.com/photo1.jpg"])

class Order(BaseModel):
    """Order model for internal use"""
    id: int
    pet_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    quantity: int = Field(..., gt=0, example=1)
    ship_date: Optional[datetime] = None
    status: OrderStatus = Field(default=OrderStatus.PLACED, example="placed")
    complete: bool = Field(default=False, example=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class OrderCreate(BaseModel):
    """Model for creating a new order"""
    pet_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    quantity: int = Field(..., gt=0, example=1)
    ship_date: Optional[datetime] = None
    status: OrderStatus = Field(default=OrderStatus.PLACED, example="placed")
    complete: bool = Field(default=False, example=False)

class User(BaseModel):
    """User model for internal use"""
    id: int
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    first_name: str = Field(..., min_length=1, max_length=50, example="John")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    email: EmailStr = Field(..., example="john@example.com")
    phone: Optional[str] = Field(None, example="+1234567890")
    password: str = Field(..., min_length=6, example="password123")
    user_status: int = Field(default=1, example=1)  # 1=active, 0=inactive
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    first_name: str = Field(..., min_length=1, max_length=50, example="John")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    email: EmailStr = Field(..., example="john@example.com")
    phone: Optional[str] = Field(None, example="+1234567890")
    password: str = Field(..., min_length=6, example="password123")
    user_status: int = Field(default=1, example=1)
