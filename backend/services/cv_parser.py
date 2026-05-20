import os
from docx import Document
import pypdf

def parse_cv(file_path: str, filename: str) -> str:
    """PDF veya Word dosyasından metni pürüzsüzce çıkaran fonksiyon"""
    ext = os.path.splitext(filename)[1].lower()
    text = ""
    
    if ext == ".docx":
        doc = Document(file_path)
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"
    elif ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    else:
        raise ValueError("Desteklenmeyen dosya formatı! Sadece PDF veya DOCX yükleyin.")
        
    if not text.strip():
        raise ValueError("CV dosyasının içi boş veya metin okunamadı.")
        
    return text