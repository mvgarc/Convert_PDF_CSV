import fitz 
import os 

def extract_text_from_pdf(pdf_path):
    text_data = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text_data.append(page.get_text())
    return text_data

def extract_images_from_pdf(pdf_path, output_folder="images"):
    os.makedirs(output_folder, exist_ok=True)
    images_info = []

    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_ext = base_image["ext"]
                img_filename = f"{output_folder}/page_{page_num}_img_{img_index}.{img_ext}"

                with open(img_filename, "wb") as f:
                    f.write(base_image["image"])

                images_info.append(img_filename)
    return images_info