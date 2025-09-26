# Feature-Based Project Structure

This project has been reorganized from a category-based structure to a feature-based structure for better maintainability and modularity.

## New Structure

```
app/
├── features/
│   ├── auth/           # Authentication and User Management
│   │   ├── __init__.py
│   │   ├── router.py           # Auth endpoints (login, register, etc.)
│   │   ├── users.py            # User-related endpoints
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

## Benefits of Feature-Based Structure

1. **Better Organization**: Related functionality is grouped together
2. **Easier Maintenance**: Changes to a feature are contained within its folder
3. **Improved Modularity**: Features can be developed and tested independently
4. **Clearer Dependencies**: Import relationships are more explicit
5. **Scalability**: New features can be added as separate modules

## Migration Notes

- All imports have been updated to use the new structure
- The `core` folder remains unchanged as requested
- Old category-based folders (`api/endpoints`, `schemas`, `database/queries`, `helpers`, `auth`) can be removed
- The main API router has been updated to import from feature modules

## Feature Definitions

- **auth**: Includes authentication, authorization, user management, JWT, OTP, SMTP
- **test**: TOEIC test management and test-related operations  
- **history**: User test history, progress tracking, and results
- **gemini**: AI-powered translation and question explanation services