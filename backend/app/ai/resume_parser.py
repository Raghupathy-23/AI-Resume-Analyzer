from io import BytesIO
from pypdf import PdfReader

def extract_pdf_text(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    if reader.is_encrypted:
        raise ValueError("Encrypted PDFs are not supported.")
    text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
    if not text:
        raise ValueError("No readable text found. Scanned PDFs require OCR and are not supported yet.")
    return text[:60000]
