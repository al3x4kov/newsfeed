# connectors/minio.py
import boto3
from typing import Any
from config import Config


class MinioConnector:
    def __init__(self, s3_client: boto3.client):
        self.s3_client = s3_client

    def upload_fileobj(self, file_obj: Any, bucket: str, key: str, extra_args: dict = None) -> None:
        if extra_args is None:
            extra_args = {}
        self.s3_client.upload_fileobj(
            file_obj,
            Bucket=bucket,
            Key=key,
            ExtraArgs=extra_args,
        )

    def delete_object(self, bucket: str, key: str) -> None:
        self.s3_client.delete_object(
            Bucket=bucket,
            Key=key,
        )
