import io
from typing import Optional
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color, black

from app.models.schemas import RotateOptions, PageNumberOptions, WatermarkOptions, ProtectOptions, UnlockOptions
from app.utils.file_handler import create_temp_file


def rotate_pdf(path: str, options: RotateOptions) -> str:
    # Rotates all pages of a PDF by specified degrees
    reader = PdfReader(path)
    writer = PdfWriter()
    deg = options.degrees % 360
    for page in reader.pages:
        page.rotate(deg)
        writer.add_page(page)
    out_path, out_id = create_temp_file(".pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_id


def _make_number_overlay(w: float, h: float, number: int, opts: PageNumberOptions) -> bytes:
    # Creates a single-page PDF overlay with a page number
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    c.setFont("Helvetica", opts.font_size)
    text = str(number)
    x, y = w - 40, 20
    if opts.position == "bottom-left":
        x, y = 20, 20
    elif opts.position == "top-right":
        x, y = w - 40, h - 20
    elif opts.position == "top-left":
        x, y = 20, h - 20
    c.setFillColor(black)
    c.drawString(x, y, text)
    c.save()
    return buf.getvalue()


def add_page_numbers(path: str, opts: PageNumberOptions) -> str:
    # Adds page numbers to each page via overlay
    reader = PdfReader(path)
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        overlay_pdf = _make_number_overlay(w, h, opts.start + idx - 1, opts)
        overlay_reader = PdfReader(io.BytesIO(overlay_pdf))
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)
    out_path, out_id = create_temp_file(".pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_id


def _make_watermark_overlay(w: float, h: float, opts: WatermarkOptions) -> bytes:
    # Creates a watermark overlay PDF for a single page
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    c.setFont("Helvetica", opts.font_size)
    c.saveState()
    c.translate(w / 2, h / 2)
    c.rotate(45)
    color = Color(0, 0, 0, alpha=opts.opacity)
    c.setFillColor(color)
    c.drawCentredString(0, 0, opts.text)
    c.restoreState()
    c.save()
    return buf.getvalue()


def add_watermark(path: str, opts: WatermarkOptions) -> str:
    # Adds a text watermark to each page
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        overlay_pdf = _make_watermark_overlay(w, h, opts)
        overlay_reader = PdfReader(io.BytesIO(overlay_pdf))
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)
    out_path, out_id = create_temp_file(".pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_id


def protect_pdf(path: str, opts: ProtectOptions) -> str:
    # Encrypts a PDF with user and optional owner passwords
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(user_password=opts.user_password, owner_password=opts.owner_password or opts.user_password)
    out_path, out_id = create_temp_file(".pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_id


def unlock_pdf(path: str, opts: UnlockOptions) -> str:
    # Removes password from a protected PDF given correct password
    reader = PdfReader(path)
    if reader.is_encrypted:
        try:
            reader.decrypt(opts.password)
        except Exception:
            pass
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    out_path, out_id = create_temp_file(".pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_id

