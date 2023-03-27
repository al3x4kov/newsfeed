from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .api import router

api_router = APIRouter()

api_router.include_router(router, tags=["api methods"])

