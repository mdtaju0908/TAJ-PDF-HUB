import io
from typing import List
from pdf2image import convert_from_path
import pytesseract
from pypdf import PdfReader, PdfWriter

from app.models.schemas import OcrOptions
from app.utils.file_handler import create_temp_file


def ocr_pdf_to_searchable(pdf_path: str, opts: OcrOptions) -> str:
    # Performs OCR by converting pages to images and embedding recognized text into a new PDF
    pages = convert_from_path(pdf_path)
    writer = PdfWriter()
    for img in pages:
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf", lang=opts.language)
        reader = PdfReader(io.BytesIO(pdf_bytes))
        writer.add_page(reader.pages[0])
    out_path, out_id = create_temp_file(".pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_id

