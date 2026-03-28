import os
import re
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from app.utils.file_handler import save_upload_files, create_temp_file


def _html_to_text(html: str) -> str:
    try:
        from lxml import html as lxml_html
        return lxml_html.fromstring(html).text_content()
    except Exception:
        return re.sub(r"<[^>]+>", "", html)


async def run(files: List[UploadFile], options: Optional[dict] = None) -> str:
    paths: List[str] = []
    try:
        paths = await save_upload_files(files, allowed_exts=[".html", ".htm"])
        out_path, out_id = create_temp_file(".pdf")
        with open(paths[0], "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
        text = _html_to_text(html)
        c = canvas.Canvas(out_path, pagesize=A4)
        width, height = A4
        x_margin = 0.75 * inch
        y_margin = 0.75 * inch
        y = height - y_margin
        for line in text.splitlines():
            if y < y_margin + 12:
                c.showPage()
                y = height - y_margin
            c.drawString(x_margin, y, line)
            y -= 14
        c.save()
        return out_id
    finally:
        for p in paths:
            try:
                os.remove(p)
            except Exception:
                pass
