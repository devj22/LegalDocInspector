import easyocr
import pdfplumber
import os
from docx import Document

reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path):
    """Extract text from an image using EasyOCR."""
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extract text from a Word document (DOCX) using python-docx."""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_file(file_path):
    """Extract text from various document formats."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(file_path)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format."
