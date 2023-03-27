import os
from pydantic import BaseSettings


class Config(BaseSettings):
    # Service
    SERVICE_NAME: str = os.environ.get("EPA_PROXY_SERVICE_NAME", "this_test_service")
    SERVICE_HOST: str = os.environ.get("EPA_PROXY_HOST", "0.0.0.0")
    SERVICE_PORT: int = os.environ.get("EPA_PROXY_SRVC_ENDPOINT_PORT", 8080)
    SERVICE_UVICORN_WORKERS: int = os.environ.get("EPA_PROXY_SRVC_UVICORN_WORKERS", 1)

    # Minio
    MINIO_ENDPOINT: str = os.environ.get("MINIO_ENDPOINT", "localhost:9000")  # Адрес MinIO сервера
    MINIO_ACCESS_KEY: str = os.environ.get("MINIO_ACCESS_KEY", "uLKXTM3qVkhSWqCn")
    MINIO_SECRET_KEY: str = os.environ.get("MINIO_SECRET_KEY", "NDz1A6KsmZunmqnFdPvZ3H9VNjdjV40m")
    MINIO_BUCKET_IMAGES: str = os.environ.get("MINIO_BUCKET_IMAGES", "photos")

    # Logger
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
