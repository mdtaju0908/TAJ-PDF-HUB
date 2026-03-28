import os
from typing import List, Optional
from fastapi import UploadFile, HTTPException
import pdfplumber
from openpyxl import Workbook
from app.utils.file_handler import save_upload_files, create_temp_file


async def run(files: List[UploadFile], options: Optional[dict] = None) -> str:
    paths: List[str] = []
    try:
        paths = await save_upload_files(files, allowed_exts=[".pdf"])
        out_path, out_id = create_temp_file(".xlsx")
        wb = Workbook()
        ws = wb.active
        ws.title = "Page1"
        with pdfplumber.open(paths[0]) as pdf:
            idx = 1
            for page in pdf.pages:
                tbls = page.extract_tables() or []
                target = ws if idx == 1 else wb.create_sheet(title=f"Page{idx}")
                if tbls:
                    for tbl in tbls:
                        for row in tbl:
                            target.append([cell if cell is not None else "" for cell in row])
                else:
                    text = page.extract_text() or ""
                    for line in text.splitlines():
                        target.append([line])
                idx += 1
        wb.save(out_path)
        return out_id
    finally:
        for p in paths:
            try:
                os.remove(p)
            except Exception:
                pass
