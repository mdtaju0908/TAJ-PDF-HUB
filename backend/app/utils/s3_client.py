import os
import uuid
import mimetypes
from typing import Optional
import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError
from app.core.config import settings


def _client(region: Optional[str] = None):
    region_name = region or settings.AWS_REGION or "us-east-1"
    cfg = Config(signature_version="s3v4", s3={"addressing_style": "virtual"})
    kwargs = {"region_name": region_name, "config": cfg}
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
    if settings.AWS_S3_ENDPOINT_URL:
        kwargs["endpoint_url"] = settings.AWS_S3_ENDPOINT_URL
    return boto3.client("s3", **kwargs)


def _ctype(path: str) -> Optional[str]:
    ctype, _ = mimetypes.guess_type(path)
    return ctype


def upload_file(file_path: str) -> str:
    if not settings.AWS_S3_BUCKET:
        raise RuntimeError("AWS_S3_BUCKET not configured")
    client = _client()
    ext = os.path.splitext(file_path)[1].lower()
    file_id = uuid.uuid4().hex + ext
    key = f"{settings.AWS_S3_PREFIX}{file_id}"
    extra = {}
    ct = _ctype(file_path)
    if ct:
        extra["ContentType"] = ct
    client.upload_file(file_path, settings.AWS_S3_BUCKET, key, ExtraArgs=extra or None)
    return file_id


def _bucket_region() -> Optional[str]:
    try:
        global_client = _client()
        resp = global_client.get_bucket_location(Bucket=settings.AWS_S3_BUCKET)
        loc = resp.get("LocationConstraint")
        return loc or "us-east-1"
    except Exception:
        return settings.AWS_REGION or "us-east-1"


def generate_signed_url(key: str, expires_seconds: int = 600) -> str:
    if not settings.AWS_S3_BUCKET:
        raise RuntimeError("AWS_S3_BUCKET not configured")
    region = _bucket_region()
    client = _client(region)
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.AWS_S3_BUCKET, "Key": key},
        ExpiresIn=expires_seconds,
    )


def delete_local_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass
