# Pet Store API - FastAPI Deployment Template

A production-ready FastAPI Pet Store API template with comprehensive deployment configurations, testing setup, and Gnome Suite integration.

## 🚀 Features

- **Pet Store API**: Complete CRUD operations for pets, orders, and users
- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Pydantic Models**: Type-safe data validation and serialization
- **OpenAPI Documentation**: Auto-generated Swagger UI and ReDoc
- **Comprehensive Testing**: Full test suite with pytest
- **Gnome Suite Ready**: Optimized for Gnome Suite deployment platform
- **Production Ready**: Proper error handling, validation, and monitoring

## 📁 Project Structure

```
fastapi-deployment-template/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── models.py              # Pet Store data models
│   └── schemas.py             # Pydantic schemas
├── tests/
│   ├── __init__.py
│   └── test_main.py           # Test cases
├── requirements.txt           # Python dependencies
├── .gitignore               # Git ignore rules
├── run.py                   # Simple startup script
└── README.md                # This file
```

## 🛠️ Local Development

### Prerequisites

- Python 3.11+
- pip or poetry
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/gnomesuite/fastapi-deployment-template.git
   cd fastapi-deployment-template
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v
```

### Test Coverage

The template includes comprehensive test coverage:
- Unit tests for all endpoints
- Integration tests for API flows
- Error handling tests
- Validation tests

## 🧙‍♂️ Gnome Suite Deployment

### Deploy via Gnome Suite Dashboard

1. **Connect GitHub Repository**
   - Go to your [Gnome Suite dashboard](https://dashboard.gnomesuite.com)
   - Click "New Project"
   - Connect your GitHub repository
   - Select this FastAPI template

2. **Automatic Deployment**
   - Gnome Suite will automatically:
     - 🐳 Build your Docker container
     - ☁️ Deploy to GCP Cloud Run
     - 🔐 Configure Apigee API Gateway
     - 📊 Set up monitoring and logging
     - 🛡️ Apply security policies
     - 📈 Configure auto-scaling

3. **Access Your API**
   - Your API will be available at: `https://your-api.gnomesuite.com`
   - Swagger documentation: `https://your-api.gnomesuite.com/docs`
   - Monitoring dashboard in Gnome Suite

### What Gnome Suite Handles for You

- 🔐 **Authentication**: Apigee handles JWT validation, OAuth, API keys
- ⚡ **Rate Limiting**: Automatic rate limiting policies
- 🛡️ **Security**: DDoS protection, CORS, input validation
- 📊 **Monitoring**: Real-time metrics, logs, and alerts
- 📈 **Scaling**: Auto-scaling based on traffic patterns
- 🔒 **SSL/TLS**: Automatic certificate management
- 💾 **Backup & Recovery**: Automated backup strategies
- ⚖️ **Load Balancing**: Intelligent traffic distribution

## 📋 API Endpoints

### 🐕 Pet Management
- `GET /pets` - 📋 Get all pets (with filtering)
- `GET /pets/{pet_id}` - 🔍 Get specific pet
- `POST /pets` - ➕ Create new pet
- `PUT /pets/{pet_id}` - ✏️ Update pet
- `DELETE /pets/{pet_id}` - 🗑️ Delete pet

### 📦 Order Management
- `GET /orders` - 📋 Get all orders
- `GET /orders/{order_id}` - 🔍 Get specific order
- `POST /orders` - ➕ Create new order
- `DELETE /orders/{order_id}` - 🗑️ Delete order

### 👥 User Management
- `GET /users` - 📋 Get all users
- `GET /users/{user_id}` - 🔍 Get specific user
- `POST /users` - ➕ Create new user
- `DELETE /users/{user_id}` - 🗑️ Delete user

### 📊 Inventory
- `GET /inventory` - 📈 Get pet inventory by status

## 🐳 Docker Support

The template includes a production-ready Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run with Docker

```bash
# Build the image
docker build -t pet-store-api .

# Run the container
docker run -p 8000:8000 pet-store-api

# Run with environment variables
docker run -p 8000:8000 -e DEBUG=false pet-store-api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support:
- **Gnome Suite Documentation**: [https://docs.gnomesuite.com](https://docs.gnomesuite.com)
- **Community Forum**: [https://community.gnomesuite.com](https://community.gnomesuite.com)
- **FastAPI Documentation**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **GitHub Issues**: [https://github.com/gnomesuite/fastapi-deployment-template/issues](https://github.com/gnomesuite/fastapi-deployment-template/issues)

---

**Start building your Pet Store API today with Gnome Suite!** 🚀

[![Deploy with Gnome Suite](https://img.shields.io/badge/Deploy%20with-Gnome%20Suite-00D4AA?style=for-the-badge&logo=gnome&logoColor=white)](https://gnomesuite.com/deploy)