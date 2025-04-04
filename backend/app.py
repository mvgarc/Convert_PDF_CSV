import os
import pdfplumber
import fitz  # PyMuPDF
import pytesseract
import pandas as pd
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import io

app = Flask(__name__)

# Configuración de carpetas
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output_csv"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Extensiones permitidas
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_pdf(pdf_path):
    """Extrae datos del PDF y los guarda en un CSV."""
    extracted_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    parts = line.split("$")  # Ajustar si el formato varía
                    if len(parts) == 2:
                        description_code = parts[0].strip()
                        price = parts[1].strip()
                        words = description_code.split()
                        code = words[0] if words else ""
                        description = " ".join(words[1:])
                        extracted_data.append([code, description, price])
    
    if extracted_data:
        csv_filename = os.path.join(OUTPUT_FOLDER, os.path.basename(pdf_path).replace(".pdf", ".csv"))
        df = pd.DataFrame(extracted_data, columns=["Código", "Descripción", "Precio"])
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        return csv_filename
    return None

@app.route("/upload", methods=["POST"])
def upload_file():
    """Recibe archivos PDF y devuelve el CSV generado."""
    if "file" not in request.files:
        return jsonify({"error": "No se encontró archivo en la solicitud"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(pdf_path)

        csv_path = extract_text_pdf(pdf_path)
        if csv_path:
            return send_file(csv_path, as_attachment=True)
        else:
            return jsonify({"error": "No se pudo extraer información del PDF"}), 500
    
    return jsonify({"error": "Formato de archivo no permitido"}), 400

if __name__ == "__main__":
    app.run(debug=True)
