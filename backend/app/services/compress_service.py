import os
import shutil
import subprocess
from typing import Optional
from pypdf import PdfReader, PdfWriter

from app.utils.file_handler import create_temp_file


def _ghostscript_cmd(input_path: str, output_path: str, quality: str) -> Optional[list]:
    # Builds Ghostscript command; returns None if executable not found
    candidates = ["gs", "gswin64c", "gswin32c"]
    exe = None
    for c in candidates:
        if shutil.which(c):
            exe = c
            break
    if not exe:
        return None
    return [
        exe,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path,
    ]


def compress_pdf(path: str, quality: str = "screen") -> str:
    # Compresses a PDF using Ghostscript if available; otherwise rewrites via pypdf
    out_path, out_id = create_temp_file(".pdf")
    cmd = _ghostscript_cmd(path, out_path, quality)
    if cmd:
        try:
            subprocess.run(cmd, check=True)
            return out_id
        except Exception:
            pass
    # Fallback: simple rewrite (minor compression if any)
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_id

