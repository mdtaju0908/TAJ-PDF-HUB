from typing import List, Tuple
import re
from pypdf import PdfReader, PdfWriter

from app.utils.file_handler import create_temp_file


def parse_ranges(ranges: str) -> List[Tuple[int, int]]:
    # Parses range string into list of (start, end) 1-based inclusive
    parts = [p.strip() for p in ranges.split(",") if p.strip()]
    result: List[Tuple[int, int]] = []
    for part in parts:
        m = re.match(r"^(\d+)-(\d+)$", part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if a > b:
                a, b = b, a
            result.append((a, b))
        else:
            if part.isdigit():
                n = int(part)
                result.append((n, n))
    return result


def split_pdf(path: str, ranges: str) -> List[str]:
    # Splits a PDF into multiple PDFs according to ranges
    reader = PdfReader(path)
    outputs: List[str] = []
    for a, b in parse_ranges(ranges):
        writer = PdfWriter()
        for i in range(a - 1, min(b, len(reader.pages))):
            writer.add_page(reader.pages[i])
        out_path, out_id = create_temp_file(".pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        outputs.append(out_id)
    return outputs

