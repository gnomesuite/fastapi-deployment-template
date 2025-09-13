# FastAPI Deployment Template

A production-ready FastAPI template with comprehensive deployment configurations, testing setup, and best practices.

## 🚀 Features

- **FastAPI Application**: Modern, fast web framework for building APIs
- **Pydantic Models**: Type-safe data validation and serialization
- **Configuration Management**: Environment-based settings with Pydantic Settings
- **Testing Framework**: Comprehensive test suite with pytest
- **CORS Support**: Cross-origin resource sharing configuration
- **Health Checks**: Built-in health monitoring endpoints
- **Documentation**: Auto-generated API documentation with Swagger UI
- **Production Ready**: Optimized for deployment with proper error handling

## 📁 Project Structure

```
fastapi-deployment-template/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py              # Configuration management
│   ├── models.py              # Data models
│   └── schemas.py             # Pydantic schemas
├── tests/
│   ├── __init__.py
│   └── test_main.py           # Test cases
├── requirements.txt           # Python dependencies
├── env.example               # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
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

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

## 🚀 Running the Application

### Development Mode
```bash
python -m app.main
```

### Using Uvicorn directly
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app
```

Run specific test file:
```bash
pytest tests/test_main.py
```

## 📋 API Endpoints

### Health & Status
- `GET /` - Root endpoint with basic info
- `GET /health` - Health check for monitoring

### Items Management
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get specific item
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

## 🔧 Configuration

The application uses environment variables for configuration. Copy `env.example` to `.env` and modify as needed:

```env
# Application Configuration
APP_NAME=FastAPI Deployment Template
DEBUG=false
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

## 🚀 Deployment

### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and run**
   ```bash
   docker build -t fastapi-template .
   docker run -p 8000:8000 fastapi-template
   ```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - ENVIRONMENT=production
    volumes:
      - .:/app
```

### Cloud Deployment

#### Heroku
1. Create `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. Deploy:
   ```bash
   git push heroku main
   ```

#### AWS/GCP/Azure
- Use container services (ECS, Cloud Run, Container Instances)
- Configure load balancers and auto-scaling
- Set up monitoring and logging

## 🔒 Security Considerations

- Change the `SECRET_KEY` in production
- Configure proper CORS origins
- Use HTTPS in production
- Implement authentication/authorization as needed
- Validate and sanitize all inputs
- Use environment variables for sensitive data

## 📊 Monitoring

The application includes:
- Health check endpoint (`/health`)
- Structured logging support
- Error handling with proper HTTP status codes
- Request/response validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support:
- Create an issue in the repository
- Check the FastAPI documentation: https://fastapi.tiangolo.com/
- Review the test cases for usage examples

## 🔄 Updates

To update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

Remember to test thoroughly after updates and update your deployment accordingly.
