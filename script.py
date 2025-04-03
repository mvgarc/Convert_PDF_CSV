import os
import pdfplumber
import fitz  # PyMuPDF
import pytesseract
import pandas as pd
from PIL import Image
import io

# Definir rutas de carpetas
pdf_folder = "input_pdfs/"  # Carpeta con PDFs
csv_folder = "output_csv/"   # Carpeta donde se guardarán los CSVs
image_folder = "extracted_images/"  # Carpeta para imágenes extraídas

# Crear carpetas si no existen
os.makedirs(csv_folder, exist_ok=True)
os.makedirs(image_folder, exist_ok=True)

def extract_text_pdfplumber(pdf_path):
    """Extrae texto estructurado de un PDF usando pdfplumber"""
    extracted_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    parts = line.split("$")  # Ajustar según formato del PDF
                    if len(parts) == 2:
                        description_code = parts[0].strip()
                        price = parts[1].strip()
                        words = description_code.split()
                        code = words[0] if words else ""
                        description = " ".join(words[1:])
                        extracted_data.append([code, description, price])
    return extracted_data

def extract_text_ocr(pdf_path):
    """Convierte el PDF a imágenes y usa OCR para extraer texto"""
    extracted_data = []
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        image_list = page.get_images(full=True)
        if image_list:
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))

                # Guardar la imagen extraída
                image_path = os.path.join(image_folder, f"{os.path.basename(pdf_path)}_page_{i+1}_img_{img_index+1}.{image_ext}")
                image.save(image_path)
                print(f"Imagen guardada en: {image_path}")

                # Aplicar OCR para extraer texto
                text = pytesseract.image_to_string(image)
                lines = text.split("\n")
                for line in lines:
                    parts = line.split("$")
                    if len(parts) == 2:
                        description_code = parts[0].strip()
                        price = parts[1].strip()
                        words = description_code.split()
                        code = words[0] if words else ""
                        description = " ".join(words[1:])
                        extracted_data.append([code, description, price])
    return extracted_data

# Procesar todos los PDFs en la carpeta
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"Procesando: {pdf_file}")

        # Intentar extraer texto con pdfplumber
        data = extract_text_pdfplumber(pdf_path)

        # Si no se encontraron datos, intentar con OCR
        if not data:
            print(f"No se pudo extraer texto con pdfplumber, probando OCR para {pdf_file}...")
            data = extract_text_ocr(pdf_path)

        # Guardar en CSV
        csv_path = os.path.join(csv_folder, f"{os.path.splitext(pdf_file)[0]}.csv")
        df = pd.DataFrame(data, columns=["Código", "Descripción", "Precio"])
        df.to_csv(csv_path, index=False, encoding="utf-8")

        print(f"Datos guardados en {csv_path}")

print("Proceso finalizado.")
