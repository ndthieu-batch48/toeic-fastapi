
from fastapi import APIRouter


from app.features.auth.router import router as auth_router
from app.features.history.router import router as history_router
from app.features.test.router import router as test_router


api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(history_router, prefix="/history", tags=["History"])
api_router.include_router(test_router, prefix="/test", tags=["Test"])
