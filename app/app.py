import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.gemini_client import generate_text_with_gemini

from .api_router import api_router
from .core.app_config import app_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(title="TOEIC API", version="1.0.0", root_path="/fastapi")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.router.redirect_slashes = False
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}


@app.post("/gemini/health")
def is_gemini_healthy():
    prompt = 'Hello. Is Gemini service available now ?'
    response = generate_text_with_gemini(prompt)
    return response