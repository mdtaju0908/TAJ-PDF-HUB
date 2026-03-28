from fastapi import APIRouter, UploadFile, File, Depends, Form
import asyncio

from app.utils.file_handler import save_upload_files, resolve_download_path
from app.utils.response import success_response
from app.services.edit_service import rotate_pdf, add_page_numbers, add_watermark, protect_pdf, unlock_pdf
from app.models.schemas import RotateOptions, PageNumberOptions, WatermarkOptions, ProtectOptions, UnlockOptions
from app.core.config import settings
from app.utils.s3_client import upload_file as s3_upload_file, generate_signed_url as s3_signed_url, delete_local_file as s3_delete_local

router = APIRouter()


def _rotate_opts(degrees: int = Form(...)) -> RotateOptions:
    return RotateOptions(degrees=degrees)


@router.post("/rotate")
async def rotate(
    file: UploadFile = File(...),
    options: RotateOptions = Depends(_rotate_opts),
):
    paths = await save_upload_files([file], allowed_exts=[".pdf"])
    out_id = await asyncio.to_thread(rotate_pdf, paths[0], options)
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


def _page_number_opts(
    position: str = Form("bottom-right"),
    start: int = Form(1),
    font_size: int = Form(12),
) -> PageNumberOptions:
    return PageNumberOptions(position=position, start=start, font_size=font_size)


@router.post("/add-page-numbers")
async def add_numbers(
    file: UploadFile = File(...),
    options: PageNumberOptions = Depends(_page_number_opts),
):
    paths = await save_upload_files([file], allowed_exts=[".pdf"])
    out_id = await asyncio.to_thread(add_page_numbers, paths[0], options)
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


def _watermark_opts(
    text: str = Form(...),
    opacity: float = Form(0.2),
    font_size: int = Form(36),
) -> WatermarkOptions:
    return WatermarkOptions(text=text, opacity=opacity, font_size=font_size)


@router.post("/add-watermark")
async def watermark(
    file: UploadFile = File(...),
    options: WatermarkOptions = Depends(_watermark_opts),
):
    paths = await save_upload_files([file], allowed_exts=[".pdf"])
    out_id = await asyncio.to_thread(add_watermark, paths[0], options)
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


def _protect_opts(
    owner_password: str | None = Form(None),
    user_password: str = Form(...),
) -> ProtectOptions:
    return ProtectOptions(owner_password=owner_password, user_password=user_password)


@router.post("/protect")
async def protect(
    file: UploadFile = File(...),
    options: ProtectOptions = Depends(_protect_opts),
):
    paths = await save_upload_files([file], allowed_exts=[".pdf"])
    out_id = await asyncio.to_thread(protect_pdf, paths[0], options)
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


def _unlock_opts(password: str = Form(...)) -> UnlockOptions:
    return UnlockOptions(password=password)


@router.post("/unlock")
async def unlock(
    file: UploadFile = File(...),
    options: UnlockOptions = Depends(_unlock_opts),
):
    paths = await save_upload_files([file], allowed_exts=[".pdf"])
    out_id = await asyncio.to_thread(unlock_pdf, paths[0], options)
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
