from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from botocore.client import Config
import boto3

import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MINIO_ENDPOINT = "localhost:9000"  # Адрес MinIO сервера
MINIO_ACCESS_KEY = "O9wiTVeXo91tjcgi"
MINIO_SECRET_KEY = "LCC4WJwMakJyDZgRxsw1pZJgSafJfD3t"
MINIO_BUCKET = "photos"

s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
)


def create_bucket_if_not_exists():
    buckets = s3_client.list_buckets()
    if MINIO_BUCKET not in [bucket["Name"] for bucket in buckets["Buckets"]]:
        s3_client.create_bucket(Bucket=MINIO_BUCKET)


create_bucket_if_not_exists()


@app.post('/upload-image')
async def upload_image(image: UploadFile = File(...)):
    # Генерация уникального имени файла и формирование ключа
    file_extension = os.path.splitext(image.filename)[-1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    s3_key = f"images/{unique_filename}"

    # Загрузка файла в MinIO
    s3_client.upload_fileobj(
        image.file,
        Bucket=MINIO_BUCKET,
        Key=s3_key,
        ExtraArgs={'ACL': 'public-read', 'ContentType': image.content_type},
    )

    # Формирование URL картинки
    image_url = f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{s3_key}"
    print(image_url)

    return JSONResponse(content={'url': image_url})
