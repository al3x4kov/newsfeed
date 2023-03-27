import os
import uuid
from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from container import Container
import boto3
from connectors.minio import MinioConnector

router = APIRouter()


@router.post('/upload-image', response_class=JSONResponse)
@inject
async def upload_image(
        request: Request,
        image: UploadFile = File(...),
        minio_connector: MinioConnector = Depends(Provide[Container.minio_connector])
) -> JSONResponse:
    config = request.app.state.Config
    # Генерация уникального имени файла и формирование ключа
    file_extension = os.path.splitext(image.filename)[-1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    s3_key = f"images/{unique_filename}"

    # Загрузка файла в MinIO
    minio_connector.upload_fileobj(
        image.file,
        bucket=config.MINIO_BUCKET_IMAGES,
        key=s3_key,
        extra_args={'ACL': 'public-read', 'ContentType': image.content_type},
    )

    # Формирование URL картинки
    image_url = f"http://{config.MINIO_ENDPOINT}/{config.MINIO_BUCKET_IMAGES}/{s3_key}"

    return JSONResponse(content={'url': image_url}, status_code=200)
