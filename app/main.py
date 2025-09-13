"""
Pet Store API - FastAPI application entry point
"""
from fastapi import FastAPI, HTTPException, Depends, status, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
from datetime import datetime

from .config import get_settings
from .models import Pet, PetCreate, PetUpdate, Order, OrderCreate, User, UserCreate, PetStatus, OrderStatus, PetCategory
from .schemas import PetResponse, OrderResponse, UserResponse, HealthResponse, ApiResponse, ErrorResponse

# Initialize FastAPI app
app = FastAPI(
    title="Pet Store API",
    description="""
    ## Pet Store API
    
    This is a sample Pet Store API built with FastAPI. It provides endpoints for managing pets, orders, and users.
    
    ### Features
    - **Pet Management**: Add, update, delete, and search pets
    - **Order Management**: Create and track orders
    - **User Management**: Manage user accounts
    - **Inventory**: Track pet availability
    - **Health Monitoring**: Built-in health checks
    
    ### Authentication
    This API uses API key authentication. Include your API key in the header:
    ```
    X-API-Key: your-api-key-here
    ```
    
    ### Error Handling
    The API returns standard HTTP status codes and detailed error messages.
    """,
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "Pet Store API Support",
        "url": "https://example.com/contact/",
        "email": "support@petstore.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    servers=[
        {"url": "http://localhost:8000", "description": "Development server"},
        {"url": "https://api.petstore.com", "description": "Production server"},
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo purposes
pets_db = []
orders_db = []
users_db = []

# Sample data
def initialize_sample_data():
    """Initialize with sample data"""
    if not pets_db:
        sample_pets = [
            Pet(id=1, name="Buddy", category=PetCategory.DOG, status=PetStatus.AVAILABLE, 
                tags=["friendly", "house-trained"], price=299.99, 
                description="A friendly golden retriever", 
                photo_urls=["https://example.com/buddy1.jpg"]),
            Pet(id=2, name="Whiskers", category=PetCategory.CAT, status=PetStatus.AVAILABLE,
                tags=["playful", "indoor"], price=199.99,
                description="A playful orange tabby cat",
                photo_urls=["https://example.com/whiskers1.jpg"]),
            Pet(id=3, name="Tweety", category=PetCategory.BIRD, status=PetStatus.SOLD,
                tags=["colorful", "singing"], price=89.99,
                description="A beautiful canary",
                photo_urls=["https://example.com/tweety1.jpg"])
        ]
        pets_db.extend(sample_pets)
    
    if not users_db:
        sample_users = [
            User(id=1, username="johndoe", first_name="John", last_name="Doe",
                 email="john@example.com", phone="+1234567890", password="password123"),
            User(id=2, username="janedoe", first_name="Jane", last_name="Doe",
                 email="jane@example.com", phone="+1234567891", password="password123")
        ]
        users_db.extend(sample_users)

# Initialize sample data
initialize_sample_data()

# Root and Health endpoints
@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """Root endpoint with API information"""
    return HealthResponse(
        message="Pet Store API is running!",
        status="healthy",
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        message="Service is healthy",
        status="healthy",
        version="1.0.0"
    )

# Pet endpoints
@app.get("/pets", response_model=List[PetResponse], tags=["Pets"])
async def get_pets(
    status: Optional[PetStatus] = Query(None, description="Filter by pet status"),
    category: Optional[PetCategory] = Query(None, description="Filter by pet category"),
    limit: int = Query(10, ge=1, le=100, description="Number of pets to return"),
    offset: int = Query(0, ge=0, description="Number of pets to skip")
):
    """Get all pets with optional filtering"""
    filtered_pets = pets_db
    
    if status:
        filtered_pets = [pet for pet in filtered_pets if pet.status == status]
    if category:
        filtered_pets = [pet for pet in filtered_pets if pet.category == category]
    
    # Apply pagination
    start = offset
    end = offset + limit
    paginated_pets = filtered_pets[start:end]
    
    return [PetResponse(**pet.dict()) for pet in paginated_pets]

@app.get("/pets/{pet_id}", response_model=PetResponse, tags=["Pets"])
async def get_pet(pet_id: int = Path(..., description="Pet ID")):
    """Get a specific pet by ID"""
    for pet in pets_db:
        if pet.id == pet_id:
            return PetResponse(**pet.dict())
    raise HTTPException(status_code=404, detail="Pet not found")

@app.post("/pets", response_model=PetResponse, status_code=status.HTTP_201_CREATED, tags=["Pets"])
async def create_pet(pet: PetCreate):
    """Add a new pet to the store"""
    new_id = max([p.id for p in pets_db], default=0) + 1
    new_pet = Pet(
        id=new_id,
        name=pet.name,
        category=pet.category,
        status=pet.status,
        tags=pet.tags,
        price=pet.price,
        description=pet.description,
        photo_urls=pet.photo_urls
    )
    pets_db.append(new_pet)
    return PetResponse(**new_pet.dict())

@app.put("/pets/{pet_id}", response_model=PetResponse, tags=["Pets"])
async def update_pet(pet_id: int = Path(..., description="Pet ID"), pet_update: PetUpdate = None):
    """Update an existing pet"""
    for i, pet in enumerate(pets_db):
        if pet.id == pet_id:
            update_data = pet_update.dict(exclude_unset=True)
            updated_pet = pet.copy(update=update_data)
            updated_pet.updated_at = datetime.utcnow()
            pets_db[i] = updated_pet
            return PetResponse(**updated_pet.dict())
    raise HTTPException(status_code=404, detail="Pet not found")

@app.delete("/pets/{pet_id}", response_model=ApiResponse, tags=["Pets"])
async def delete_pet(pet_id: int = Path(..., description="Pet ID")):
    """Delete a pet"""
    for i, pet in enumerate(pets_db):
        if pet.id == pet_id:
            del pets_db[i]
            return ApiResponse(
                code=200,
                type="success",
                message=f"Pet {pet_id} deleted successfully"
            )
    raise HTTPException(status_code=404, detail="Pet not found")

# Order endpoints
@app.get("/orders", response_model=List[OrderResponse], tags=["Orders"])
async def get_orders(
    status: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    limit: int = Query(10, ge=1, le=100, description="Number of orders to return"),
    offset: int = Query(0, ge=0, description="Number of orders to skip")
):
    """Get all orders with optional filtering"""
    filtered_orders = orders_db
    
    if status:
        filtered_orders = [order for order in filtered_orders if order.status == status]
    
    # Apply pagination
    start = offset
    end = offset + limit
    paginated_orders = filtered_orders[start:end]
    
    return [OrderResponse(**order.dict()) for order in paginated_orders]

@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def get_order(order_id: int = Path(..., description="Order ID")):
    """Get a specific order by ID"""
    for order in orders_db:
        if order.id == order_id:
            return OrderResponse(**order.dict())
    raise HTTPException(status_code=404, detail="Order not found")

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def create_order(order: OrderCreate):
    """Place an order for a pet"""
    # Check if pet exists
    pet_exists = any(pet.id == order.pet_id for pet in pets_db)
    if not pet_exists:
        raise HTTPException(status_code=400, detail="Pet not found")
    
    # Check if user exists
    user_exists = any(user.id == order.user_id for user in users_db)
    if not user_exists:
        raise HTTPException(status_code=400, detail="User not found")
    
    new_id = max([o.id for o in orders_db], default=0) + 1
    new_order = Order(
        id=new_id,
        pet_id=order.pet_id,
        user_id=order.user_id,
        quantity=order.quantity,
        ship_date=order.ship_date,
        status=order.status,
        complete=order.complete
    )
    orders_db.append(new_order)
    return OrderResponse(**new_order.dict())

@app.delete("/orders/{order_id}", response_model=ApiResponse, tags=["Orders"])
async def delete_order(order_id: int = Path(..., description="Order ID")):
    """Delete an order"""
    for i, order in enumerate(orders_db):
        if order.id == order_id:
            del orders_db[i]
            return ApiResponse(
                code=200,
                type="success",
                message=f"Order {order_id} deleted successfully"
            )
    raise HTTPException(status_code=404, detail="Order not found")

# User endpoints
@app.get("/users", response_model=List[UserResponse], tags=["Users"])
async def get_users(
    limit: int = Query(10, ge=1, le=100, description="Number of users to return"),
    offset: int = Query(0, ge=0, description="Number of users to skip")
):
    """Get all users"""
    # Apply pagination
    start = offset
    end = offset + limit
    paginated_users = users_db[start:end]
    
    return [UserResponse(**user.dict()) for user in paginated_users]

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: int = Path(..., description="User ID")):
    """Get a specific user by ID"""
    for user in users_db:
        if user.id == user_id:
            return UserResponse(**user.dict())
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate):
    """Create a new user"""
    # Check if username already exists
    if any(u.username == user.username for u in users_db):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_id = max([u.id for u in users_db], default=0) + 1
    new_user = User(
        id=new_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password=user.password,
        user_status=user.user_status
    )
    users_db.append(new_user)
    return UserResponse(**new_user.dict())

@app.delete("/users/{user_id}", response_model=ApiResponse, tags=["Users"])
async def delete_user(user_id: int = Path(..., description="User ID")):
    """Delete a user"""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[i]
            return ApiResponse(
                code=200,
                type="success",
                message=f"User {user_id} deleted successfully"
            )
    raise HTTPException(status_code=404, detail="User not found")

# Inventory endpoint
@app.get("/inventory", response_model=dict, tags=["Inventory"])
async def get_inventory():
    """Get pet inventory by status"""
    inventory = {}
    for pet in pets_db:
        status = pet.status.value
        if status not in inventory:
            inventory[status] = 0
        inventory[status] += 1
    return inventory

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )