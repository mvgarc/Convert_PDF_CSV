import fitz 
import os 

def extract_text_from_pdf(pdf_path, output_dir):
    text_data = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text_data.append(page.get_text())
    return text_data