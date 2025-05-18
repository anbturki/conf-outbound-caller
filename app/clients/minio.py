from minio import Minio

from app.core.config import minio_config

bucket_name = minio_config.bucket_name

client = Minio(
    endpoint=minio_config.endpoint,
    access_key=minio_config.access_key,
    secret_key=minio_config.secret_key,
    secure=False,
)


if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
