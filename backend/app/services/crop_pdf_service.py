import os
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader, PdfWriter
from app.utils.file_handler import save_upload_files, create_temp_file


async def run(files: List[UploadFile], options: Optional[dict] = None) -> str:
    paths: List[str] = []
    try:
        paths = await save_upload_files(files, allowed_exts=[".pdf"])
        out_path, out_id = create_temp_file(".pdf")
        reader = PdfReader(paths[0])
        writer = PdfWriter()
        margin = float((options or {}).get("margin", 36))
        for page in reader.pages:
            box = page.cropbox if page.cropbox is not None else page.mediabox
            x0 = float(box.left) + margin
            y0 = float(box.bottom) + margin
            x1 = float(box.right) - margin
            y1 = float(box.top) - margin
            page.cropbox.lower_left = (x0, y0)
            page.cropbox.upper_right = (x1, y1)
            writer.add_page(page)
        with open(out_path, "wb") as f:
            writer.write(f)
        return out_id
    finally:
        for p in paths:
            try:
                os.remove(p)
            except Exception:
                pass
