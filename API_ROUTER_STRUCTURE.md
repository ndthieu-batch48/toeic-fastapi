# API Router Structure

This file documents the complete API router structure for the TOEIC FastAPI application.

## Main API Router

The main API router is located at `app/api_router.py` and includes all feature routers:

```python
from app.features.auth.router import router as auth_router
from app.features.history.router import router as history_router  
from app.features.test.router import router as test_router

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(history_router, prefix="/history", tags=["History"])
api_router.include_router(test_router, prefix="/tests", tags=["Tests"])
```

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

## Directory Structure

```
app/
├── api_router.py          # Main API router (aggregates all feature routers)
├── app.py                 # FastAPI app initialization
├── features/              # Feature-based modules
│   ├── auth/              # Authentication & User Management
│   │   ├── router.py      # Auth endpoints
│   │   ├── schemas.py     # Auth Pydantic models
│   │   ├── queries.py     # Auth database queries
│   │   ├── dependencies.py # Auth dependencies (get_current_user)
│   │   ├── smtp.py        # Email services
│   │   ├── const/         # Auth constants
│   │   └── helper/        # Auth helpers (JWT, OTP, etc.)
│   ├── history/           # Test History & Progress  
│   │   ├── router.py      # History endpoints
│   │   ├── schemas.py     # History Pydantic models
│   │   └── queries.py     # History database queries
│   └── test/              # Test Management & Gemini Services
│       ├── router.py      # Test & Gemini endpoints
│       ├── schemas.py     # Test & Gemini Pydantic models
│       ├── queries.py     # Test database queries
│       └── prompt_helper.py # Gemini prompt utilities
├── core/                  # Shared core functionality
├── util/                  # Utility functions
└── __init__.py files      # All directories have proper __init__.py
```

## Missing __init__.py Files Added

- `app/util/__init__.py`
- `app/features/auth/const/__init__.py`

## Changes Made

1. **Created main API router** at `app/api_router.py`
2. **Updated app.py imports** to use the new api_router
3. **Added missing __init__.py files** for proper Python module structure
4. **Moved Gemini health endpoint** from app.py to test router
5. **Organized all routers** under appropriate feature prefixes
6. **Removed duplicate imports** and cleaned up app.py

The application now has a clean, feature-based router structure that's easy to maintain and extend.