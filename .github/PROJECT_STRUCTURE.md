
## Project Structure

```
app/
├── features/
│   ├── auth/           # Authentication and User Management
│   │   ├── __init__.py
│   │   ├── router.py           # Auth endpoints (login, register, etc.)
│   │   ├── schemas.py          # Auth/User Pydantic models
│   │   ├── queries.py          # Database queries for auth/users
│   │   ├── jwt_helper.py       # JWT token utilities
│   │   ├── otp_helper.py       # OTP generation/validation
│   │   ├── smtp.py             # Email services
│   │   └── dependencies.py     # Auth dependencies (get_current_user)
│   │
│   ├── test/           # Test Management
│   │   ├── __init__.py
│   │   ├── router.py           # Test endpoints
│   │   ├── schemas.py          # Test Pydantic models
│   │   └── queries.py          # Database queries for tests
│   │
│   ├── history/        # Test History & Progress
│   │   ├── __init__.py
│   │   ├── router.py           # History endpoints
│   │   ├── schemas.py          # History Pydantic models
│   │   └── queries.py          # Database queries for history
│   │
│   └── gemini/         # AI/Translation Services
│       ├── __init__.py
│       ├── router.py           # Gemini API endpoints
│       ├── schemas.py          # Gemini Pydantic models
│       ├── client.py           # Gemini client utilities
│       └── prompt_helper.py    # Prompt building utilities
│
├── core/               # Shared core functionality (unchanged)
├── const/              # Constants (unchanged)
└── api/
    └── router.py       # Main API router (updated imports)

```
