import boto3
from botocore.config import Config
from app.core.config import settings

def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
        config=Config(signature_version="s3v4"),
    )

def ensure_bucket():
    client = s3_client()
    buckets = client.list_buckets().get("Buckets", [])
    if not any(b["Name"] == settings.s3_bucket for b in buckets):
        client.create_bucket(Bucket=settings.s3_bucket)

def put_bytes(key: str, body: bytes, content_type: str) -> None:
    s3_client().put_object(Bucket=settings.s3_bucket, Key=key, Body=body, ContentType=content_type)

def delete_object(key: str | None) -> None:
    if key:
        s3_client().delete_object(Bucket=settings.s3_bucket, Key=key)

def presigned_get(key: str, expires: int = 300) -> str:
    return s3_client().generate_presigned_url(
        "get_object", Params={"Bucket": settings.s3_bucket, "Key": key}, ExpiresIn=expires
    )

def get_bytes(key: str) -> bytes:
    response = s3_client().get_object(Bucket=settings.s3_bucket, Key=key)
    return response["Body"].read()
