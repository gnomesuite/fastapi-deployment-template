#!/usr/bin/env python3
"""
Script to create a blank FastAPI API template
"""
import os
import sys
from pathlib import Path

def create_blank_api(api_name="my-api"):
    """Create a blank FastAPI API structure"""
    
    # Create directory structure
    api_dir = Path(api_name)
    app_dir = api_dir / "app"
    tests_dir = api_dir / "tests"
    
    # Create directories
    api_dir.mkdir(exist_ok=True)
    app_dir.mkdir(exist_ok=True)
    tests_dir.mkdir(exist_ok=True)
    
    # Create __init__.py files
    (app_dir / "__init__.py").write_text("# API package\n")
    (tests_dir / "__init__.py").write_text("# Test package\n")
    
    # Create main.py
    main_content = '''"""
Blank FastAPI API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Blank API",
    description="A blank FastAPI template to get you started",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to your blank API!", "status": "running"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
'''
    
    (app_dir / "main.py").write_text(main_content)
    
    # Create models.py
    models_content = '''"""
Data models for your API
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    """Example item model"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime = None
    
    def __init__(self, **data):
        if 'created_at' not in data:
            data['created_at'] = datetime.utcnow()
        super().__init__(**data)

class ItemCreate(BaseModel):
    """Model for creating a new item"""
    name: str
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    """Model for updating an item"""
    name: Optional[str] = None
    description: Optional[str] = None
'''
    
    (app_dir / "models.py").write_text(models_content)
    
    # Create schemas.py
    schemas_content = '''"""
Pydantic schemas for API responses
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemResponse(BaseModel):
    """Schema for item API responses"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

class HealthResponse(BaseModel):
    """Schema for health check responses"""
    status: str
    message: str
    timestamp: datetime = None
    
    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)
'''
    
    (app_dir / "schemas.py").write_text(schemas_content)
    
    # Create requirements.txt
    requirements_content = '''# FastAPI and ASGI server
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Data validation
pydantic==2.5.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development tools
python-multipart==0.0.6
'''
    
    (api_dir / "requirements.txt").write_text(requirements_content)
    
    # Create test file
    test_content = '''"""
Test cases for the blank API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to your blank API!"
    assert data["status"] == "running"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "API is running" in data["message"]
'''
    
    (tests_dir / "test_main.py").write_text(test_content)
    
    # Create run.py
    run_content = '''#!/usr/bin/env python3
"""
Simple script to run the FastAPI application
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
'''
    
    (api_dir / "run.py").write_text(run_content)
    
    # Create .gitignore
    gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log
'''
    
    (api_dir / ".gitignore").write_text(gitignore_content)
    
    # Create README.md
    readme_content = f'''# {api_name.title()} - Blank FastAPI API

A blank FastAPI template to get you started quickly.

## 🚀 Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API**
   ```bash
   python run.py
   # or
   uvicorn app.main:app --reload
   ```

3. **Access the API**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## 📁 Project Structure

```
{api_name}/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── models.py        # Data models
│   └── schemas.py       # Response schemas
├── tests/
│   ├── __init__.py
│   └── test_main.py     # Test cases
├── requirements.txt     # Dependencies
├── run.py              # Run script
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Customization

1. **Add your endpoints** in `app/main.py`
2. **Define your models** in `app/models.py`
3. **Create response schemas** in `app/schemas.py`
4. **Add tests** in `tests/test_main.py`

## 🚀 Deploy with Gnome Suite

Ready to deploy? Use Gnome Suite for easy deployment:

[![Deploy with Gnome Suite](https://img.shields.io/badge/Deploy%20with-Gnome%20Suite-00D4AA?style=for-the-badge&logo=gnome&logoColor=white)](https://gnomesuite.com/deploy)

---

**Start building your API today!** 🚀
'''
    
    (api_dir / "README.md").write_text(readme_content)
    
    print(f"✅ Blank API '{api_name}' created successfully!")
    print(f"📁 Location: {api_dir.absolute()}")
    print(f"🚀 To get started:")
    print(f"   cd {api_name}")
    print(f"   pip install -r requirements.txt")
    print(f"   python run.py")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        api_name = sys.argv[1]
    else:
        api_name = input("Enter API name (default: my-api): ").strip() or "my-api"
    
    # Validate API name
    if not api_name.replace("-", "").replace("_", "").isalnum():
        print("❌ Error: API name can only contain letters, numbers, hyphens, and underscores")
        sys.exit(1)
    
    if Path(api_name).exists():
        response = input(f"❌ Directory '{api_name}' already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Operation cancelled")
            sys.exit(1)
    
    create_blank_api(api_name)

if __name__ == "__main__":
    main()
