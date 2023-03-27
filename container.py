"""Containers module."""
from dependency_injector import containers, providers
from config import Config as App_Config

from botocore.client import Config as Boto_Config
from connectors.minio import MinioConnector
import boto3.session


class Container(containers.DeclarativeContainer):
    config = App_Config()

    session = providers.Resource(
        boto3.session.Session,
        aws_access_key_id=config.MINIO_ACCESS_KEY,
        aws_secret_access_key=config.MINIO_SECRET_KEY,
    )

    s3_client = providers.Resource(
        session.provided.client.call(),
        service_name="s3",
        endpoint_url=f"http://{config.MINIO_ENDPOINT}",
        config=Boto_Config(signature_version="s3v4"),
    )

    minio_connector = providers.Factory(
        MinioConnector,
        s3_client=s3_client,
    )
