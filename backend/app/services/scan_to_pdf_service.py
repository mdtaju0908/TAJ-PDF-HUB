import os
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from PIL import Image, ImageEnhance, ImageFilter
from app.utils.file_handler import save_upload_files, create_temp_file


async def run(files: List[UploadFile], options: Optional[dict] = None) -> str:
    paths: List[str] = []
    try:
        paths = await save_upload_files(files, allowed_exts=[".jpg", ".jpeg", ".png"])
        imgs = []
        for p in paths:
            img = Image.open(p)
            img = img.convert("L")
            img = ImageEnhance.Contrast(img).enhance(1.5)
            img = img.filter(ImageFilter.SHARPEN)
            imgs.append(img.convert("RGB"))
        out_path, out_id = create_temp_file(".pdf")
        first, rest = imgs[0], imgs[1:]
        first.save(out_path, save_all=True, append_images=rest)
        return out_id
    finally:
        for p in paths:
            try:
                os.remove(p)
            except Exception:
                pass
