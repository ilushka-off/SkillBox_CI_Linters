from fastapi import APIRouter
from api.v1.client import router as client_router
from api.v1.parking import router as parking_router
from api.v1.client_parking import router as client_parking_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(client_router)
v1_router.include_router(parking_router)
v1_router.include_router(client_parking_router)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
