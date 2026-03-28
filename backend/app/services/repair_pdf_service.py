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
        writer = PdfWriter()
        try:
            reader = PdfReader(paths[0], strict=False)
            for page in reader.pages:
                writer.add_page(page)
        except Exception:
            reader = PdfReader(paths[0])
            for page in reader.pages:
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
