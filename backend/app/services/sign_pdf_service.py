import os
import io
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from app.utils.file_handler import save_upload_files, create_temp_file


def _make_overlay(width: float, height: float, text: str) -> bytes:
    b = io.BytesIO()
    c = canvas.Canvas(b, pagesize=(width, height))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(width - 200, 30, text)
    c.save()
    return b.getvalue()


async def run(files: List[UploadFile], options: Optional[dict] = None) -> str:
    paths: List[str] = []
    try:
        paths = await save_upload_files(files, allowed_exts=[".pdf"])
        out_path, out_id = create_temp_file(".pdf")
        reader = PdfReader(paths[0])
        writer = PdfWriter()
        text = (options or {}).get("text", "Signed")
        for page in reader.pages:
            box = page.mediabox
            w = float(box.width)
            h = float(box.height)
            overlay = PdfReader(io.BytesIO(_make_overlay(w, h, text))).pages[0]
            page.merge_page(overlay)
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
