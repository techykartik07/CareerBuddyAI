import pdfplumber, io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF given its raw bytes."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text.strip())
    
    full_text = "\n\n".join(text_parts)
    if not full_text.strip():
        raise ValueError("Could not extract text. PDF may be image based or scanned.")
    return full_text
