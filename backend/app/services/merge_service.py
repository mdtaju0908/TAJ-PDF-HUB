from typing import List
import os
from pypdf import PdfReader, PdfWriter

from app.utils.file_handler import create_temp_file


def merge_pdfs(pdf_paths: List[str]) -> str:
    # Merges multiple PDFs into a single PDF
    writer = PdfWriter()
    for path in pdf_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    out_path, out_id = create_temp_file(".pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_id

