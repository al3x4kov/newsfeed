# """minio.py"""
# import boto3
#
# def create_s3_client(
#         aws_type,
#         endpoint_url,
#         aws_access_key_id,
#         aws_secret_access_key,
#         config,
#         minio_bucket,
# ):
#     s3_client = boto3.client(
#         aws_type,
#         endpoint_url=endpoint_url,
#         aws_access_key_id=aws_access_key_id,
#         aws_secret_access_key=aws_secret_access_key,
#         config=config,
#     )
#
#     buckets = s3_client.list_buckets()
#     if minio_bucket not in [bucket["Name"] for bucket in buckets["Buckets"]]:
#         s3_client.create_bucket(Bucket=minio_bucket)
#
#     return s3_client
