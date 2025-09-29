# FastAPI TOEIC Application - Dependency Overview

## Project Description
This is a FastAPI-based TOEIC (Test of English for International Communication) application that integrates with Google's Gemini AI for language processing capabilities. The application provides web APIs for TOEIC test management with database storage and AI-powered features.

## Core Dependencies

### Web Framework & API
- **FastAPI (0.115.6)** - Modern, fast web framework for building APIs with Python
  - **Starlette** - ASGI framework underlying FastAPI
  - **Pydantic** - Data validation and settings management using Python type annotations
  - **Uvicorn (0.34.0)** - ASGI web server for running FastAPI applications

### Database & Storage
- **MySQL Connectors**:
  - **mysql-connector-python (9.3.0)** - Official MySQL driver for Python
  - **mysqlclient (2.2.7)** - C extension for MySQL connectivity (performance-focused)
  - **aiomysql (0.2.0)** - Async MySQL client built on PyMySQL
- **Pillow (11.3.0)** - Python Imaging Library for image processing

### AI & Machine Learning
- **google-genai (1.24.0)** - Google's Generative AI SDK for integrating with Gemini AI models
  - Includes authentication, HTTP client, and WebSocket support
  - Provides async capabilities for AI operations

### Security & Authentication
- **bcrypt (4.3.0)** - Password hashing library for secure user authentication
- **cryptography (45.0.5)** - Cryptographic recipes and primitives
- **python-jose (3.5.0)** - JSON Web Token implementation for JWT handling
- **passlib (1.7.4)** - Password hashing utilities with multiple algorithm support

### HTTP & Networking
- **aiohttp (3.12.15)** - Async HTTP client/server framework
- **aiosmtplib (4.0.1)** - Async SMTP client for email functionality
- **httpx** - Modern HTTP client with async support (via google-genai)
- **requests (2.32.4)** - Traditional HTTP library for synchronous requests

### Configuration & Utilities
- **pydantic-settings (2.10.1)** - Settings management using Pydantic models
- **python-dotenv** - Load environment variables from .env files
- **email_validator (2.2.0)** - Email validation with DNS checking
- **tenacity** - Retry library for handling transient failures

### Development Tools
- **pipdeptree (2.28.0)** - Display dependency tree (development utility)

### Database Drivers
- **mysql-connector-python**: Official driver for standard operations


## Installation Guide

### Prerequisites
- **Python 3.8+** (recommended 3.9+)
- **MySQL Server** (5.7+ or 8.0+)
- **Google Cloud Account** with Gemini API access

### Environment Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate     # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment variables** (create `.env` file):
   ```env
   # Database Configuration
   MYSQL_HOST=localhost
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=toeic_db
   
   # AI Integration
   GEMINI_API_KEY=your_gemini_api_key
   
   # Security
   SECRET_KEY=your_jwt_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Email Configuration (if using SMTP)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email
   SMTP_PASSWORD=your_app_password
   
   # Media Storage
   MEDIA_DIRECTORY=./media
   ```

4. **Database setup**:
   ```sql
   CREATE DATABASE toeic_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Run the application**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```


### API Documentation
Once running, access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues
1. **MySQL Connection**: Ensure MySQL service is running and credentials are correct
2. **Google API**: Verify API key has Gemini access enabled
3. **Dependencies**: Use Python 3.8+ and ensure all packages install cleanly
4. **Media Directory**: Create and set proper permissions for media storage path

### Development vs Production
- Development: Use `--reload` flag with uvicorn
- Production: Use proper ASGI server like Gunicorn with uvicorn workers
- Database: Consider connection pooling configuration for production loads

# tab API Documentation

## Feature Routers

### 1. Authentication Router (`/auth`)
**File:** `app/features/auth/router.py`
**Endpoints:**
- `POST /auth/register` - User registration
- `POST /auth/login` - User login  
- `POST /auth/refresh-token` - Refresh JWT token
- `POST /auth/reset-password` - Reset user password
- `POST /auth/send-reset-password-otp` - Send password reset OTP
- `POST /auth/verify-reset-password-otp` - Verify password reset OTP

### 2. History Router (`/history`) 
**File:** `app/features/history/router.py`
**Endpoints:**
- `POST /history` - Create/save history entry
- `GET /history/save` - Get saved history
- `GET /history/result/list` - Get history results list
- `GET /history/result/detail` - Get detailed history results

### 3. Test Router (`/tests`)
**File:** `app/features/test/router.py`  
**Endpoints:**
- `POST /tests/gemini/health` - Check Gemini service health
- `GET /tests/all` - Get all tests
- `GET /tests/{id}` - Get specific test by ID
- `GET /tests/{id}/parts/{part_id}/detail` - Get test part details
- `POST /tests/gemini/translate/question` - Translate questions using Gemini
- `POST /tests/gemini/translate/image` - Translate images using Gemini
