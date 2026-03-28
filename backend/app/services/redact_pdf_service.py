import os
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from app.utils.file_handler import save_upload_files, create_temp_file


async def run(files: List[UploadFile], options: Optional[dict] = None) -> str:
    paths: List[str] = []
    try:
        paths = await save_upload_files(files, allowed_exts=[".pdf"])
        out_path, out_id = create_temp_file(".pdf")
        try:
            import fitz
            doc = fitz.open(paths[0])
            terms = (options or {}).get("terms", ["CONFIDENTIAL"])
            for page in doc:
                for t in terms:
                    rects = page.search_for(t)
                    for r in rects:
                        page.add_redact_annot(r, fill=(0, 0, 0))
                page.apply_redactions()
            doc.save(out_path)
            doc.close()
        except Exception:
            raise HTTPException(status_code=400, detail="PyMuPDF not available")
        return out_id
    finally:
        for p in paths:
            try:
                os.remove(p)
            except Exception:
                pass
