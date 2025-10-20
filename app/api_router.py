from fastapi import APIRouter


from app.features.auth.auth_router import router as auth_router
from app.features.history.history_router import router as history_router
from app.features.test.test_router import router as test_router


api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(history_router, prefix="/histories", tags=["History"])
api_router.include_router(test_router, prefix="/tests", tags=["Test"])
