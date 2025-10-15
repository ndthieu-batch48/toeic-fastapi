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



