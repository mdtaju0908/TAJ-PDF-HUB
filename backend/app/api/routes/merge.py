from fastapi import APIRouter, UploadFile, File
from typing import List
import asyncio

from app.utils.file_handler import save_upload_files, resolve_download_path
from app.utils.response import success_response
from app.services.merge_service import merge_pdfs
from app.core.config import settings
from app.utils.s3_client import upload_file as s3_upload_file, generate_signed_url as s3_signed_url, delete_local_file as s3_delete_local

router = APIRouter()


@router.post("/merge")
async def merge(files: List[UploadFile] = File(...)):
    paths = await save_upload_files(files, allowed_exts=[".pdf"])
    out_id = await asyncio.to_thread(merge_pdfs, paths)
    if settings.AWS_S3_BUCKET:
        file_path = resolve_download_path(out_id)
        try:
            file_id = s3_upload_file(file_path)
            key = f"{settings.AWS_S3_PREFIX}{file_id}"
            url = s3_signed_url(key, expires_seconds=600)
            s3_delete_local(file_path)
            return success_response("Conversion completed successfully", url, file_id)
        except Exception:
            url = f"/api/download/{out_id}"
            return success_response("Conversion completed successfully", url, out_id)
    else:
        url = f"/api/download/{out_id}"
        return success_response("Conversion completed successfully", url, out_id)
