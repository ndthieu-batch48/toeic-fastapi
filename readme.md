# FastAPI TOEIC Application - Dependency Overview

## Project Description
This is a FastAPI-based TOEIC (Test of English for International Communication) application that integrates with Google's Gemini AI for language processing capabilities. The application provides web APIs for TOEIC test management with database storage and AI-powered features.

## Core Dependencies

### Web Framework & API
- **FastAPI (0.115.6)** - Modern, fast web framework for building APIs with Python
  - **Starlette (0.41.3)** - ASGI framework underlying FastAPI
  - **Pydantic (2.11.7)** - Data validation and settings management using Python type annotations
  - **Pydantic-settings (2.10.1)** - Settings management using Pydantic models
  - **Uvicorn (0.34.0)** - ASGI web server for running FastAPI applications

### Database & Storage
- **mysql-connector-python (9.3.0)** - Official MySQL driver for Python
- **Pillow (11.3.0)** - Python Imaging Library for image processing and base64 image handling

### AI & Machine Learning
- **google-genai (1.24.0)** - Google's Generative AI SDK for integrating with Gemini AI models
  - Includes authentication, HTTP client, and WebSocket support
  - Provides async capabilities for AI operations
- **google-auth (2.40.3)** - Google authentication library

### Security & Authentication
- **bcrypt (4.3.0)** - Password hashing library for secure user authentication
- **cryptography (45.0.5)** - Cryptographic recipes and primitives
- **python-jose (3.5.0)** - JSON Web Token implementation for JWT handling
- **passlib (1.7.4)** - Password hashing utilities with multiple algorithm support

### HTTP & Networking
- **aiohttp (3.12.15)** - Async HTTP client/server framework
- **aiosmtplib (4.0.1)** - Async SMTP client for email functionality
- **httpcore (1.0.9)** - HTTP client core library
- **httpx (0.28.1)** - Modern HTTP client with async support
- **requests (2.32.4)** - Traditional HTTP library for synchronous requests
- **urllib3 (2.5.0)** - HTTP client library for Python

### Configuration & Utilities
- **python-dotenv (1.1.1)** - Load environment variables from .env files
- **email_validator (2.2.0)** - Email validation with DNS checking
- **tenacity (8.5.0)** - Retry library for handling transient failures
- **cachetools (5.5.2)** - Caching utilities for API responses

### Development & Debugging Tools
- **pipdeptree (2.28.0)** - Display dependency tree (development utility)


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

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### API Endpoints Overview

#### 1. Authentication Endpoints (`/auth`)

| Method | Endpoint                    | Description                                  |
| ------ | --------------------------- | -------------------------------------------- |
| `POST` | `/auth/register`            | Register a new user                          |
| `POST` | `/auth/login`               | User login with email/username and password  |
| `POST` | `/auth/refresh-token`       | Refresh JWT access token using refresh token |
| `POST` | `/auth/password/otp`        | Request OTP for password reset               |
| `POST` | `/auth/password/otp/verify` | Verify OTP and get reset password token      |
| `PUT`  | `/auth/password/reset`      | Reset password using verified token          |

**Key Features:**
- JWT token-based authentication
- Password hashing with bcrypt
- OTP-based password reset via email
- Access token and refresh token mechanism

---

#### 2. History Endpoints (`/histories`)

| Method | Endpoint                   | Description                                     |
| ------ | -------------------------- | ----------------------------------------------- |
| `POST` | `/histories`               | Create or update test attempt history           |
| `GET`  | `/histories/save`          | Get saved progress history (for current test)   |
| `GET`  | `/histories/result/list`   | Get list of all submitted test results          |
| `GET`  | `/histories/result/detail` | Get detailed analysis of a specific test result |

**Query Parameters:**
- `test_id` (integer): Required for `/histories/save` endpoint
- `history_id` (integer): Required for `/histories/result/detail` endpoint

**Response Includes:**
- Test scores and accuracy
- Question breakdown by part
- Correct/incorrect/no answer counts
- Time duration for practice and exam modes

---

#### 3. Test Endpoints (`/tests`)

| Method | Endpoint                                       | Description                                                |
| ------ | ---------------------------------------------- | ---------------------------------------------------------- |
| `GET`  | `/tests`                                       | Get all available TOEIC tests                              |
| `GET`  | `/tests/{id}`                                  | Get detailed test information with all parts and questions |
| `GET`  | `/tests/{test_id}/part/{part_id}/audio/url`    | Get audio streaming URL for a part                         |
| `GET`  | `/tests/{test_id}/part/{part_id}/audio/stream` | Stream audio file for a test part                          |
| `POST` | `/tests/gemini/translate/question`             | Translate a question using Gemini AI                       |
| `POST` | `/tests/gemini/explain/question`               | Get AI explanation for a question                          |
| `POST` | `/tests/gemini/translate/image`                | Get base64 image data for a media                          |
| `POST` | `/tests/gemini/translate/audio-script`         | Get English transcript of audio                            |

**Request/Response Examples:**

**Translate Question Request:**
```json
{
  "question_id": 1,
  "language_id": "vi"
}
```

**Explain Question Request:**
```json
{
  "question_id": 1,
  "language_id": "vi"
}
```

**Translate Image Request:**
```json
{
  "media_id": 1
}
```

**Translate Audio Script Request:**
```json
{
  "media_id": 1
}
```

---

### Authentication

**Protected Endpoints:**
- All `/histories` endpoints require authentication via JWT bearer token
- TODO: Add authentication dependency for `/tests` endpoints

**How to Authenticate:**
1. Register or login to get `access_token`
2. Include token in request header:
   ```
   Authorization: Bearer {access_token}
   ```

---

### Response Format

**Success Response:**
```json
{
  "status": 200,
  "data": {...},
  "message": "Operation successful"
}
```

**Error Response:**
```json
{
  "detail": {
    "message": "Error description",
    "error": "Detailed error message"
  }
}
```

---

### Interactive API Documentation

Once the application is running, you can explore the API interactively:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These tools allow you to:
- View all available endpoints
- See request/response schemas
- Test endpoints directly from the browser
- View detailed error messages
