import os
import mimetypes
from typing import Optional
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.core.config import settings
from app.utils.file_handler import resolve_download_path, secure_filename


def _infer_content_type(path: str) -> str:
    ctype, _ = mimetypes.guess_type(path)
    return ctype or "application/octet-stream"


def _get_s3_client():
    kwargs = {
        "region_name": settings.AWS_REGION,
    }
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
    if settings.AWS_S3_ENDPOINT_URL:
        kwargs["endpoint_url"] = settings.AWS_S3_ENDPOINT_URL
    return boto3.client("s3", **kwargs)


def upload_file_to_s3(local_path: str, key: str, content_type: Optional[str] = None) -> str:
    if not settings.AWS_S3_BUCKET:
        raise RuntimeError("AWS_S3_BUCKET is not configured")
    client = _get_s3_client()
    extra = {}
    ct = content_type or _infer_content_type(local_path)
    if ct:
        extra["ContentType"] = ct
    client.upload_file(local_path, settings.AWS_S3_BUCKET, key, ExtraArgs=extra or None)
    return key


def generate_presigned_url(key: str, expires_seconds: int = 300) -> str:
    if not settings.AWS_S3_BUCKET:
        raise RuntimeError("AWS_S3_BUCKET is not configured")
    client = _get_s3_client()
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.AWS_S3_BUCKET, "Key": key},
        ExpiresIn=expires_seconds,
    )
    return url


def upload_processed_file_and_presign(file_id: str, expires_seconds: int = 300) -> str:
    path = resolve_download_path(file_id)
    if not os.path.exists(path):
        raise FileNotFoundError("Processed file not found")
    key = f"{settings.AWS_S3_PREFIX}{secure_filename(file_id)}"
    try:
        upload_file_to_s3(path, key)
        return generate_presigned_url(key, expires_seconds=expires_seconds)
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"S3 error: {str(e)}")
