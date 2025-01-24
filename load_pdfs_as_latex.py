import google.generativeai as genai
from pdf2image import convert_from_path
import os
import base64

# Configure the generative AI
with open("api.key", "r") as file:
    API_KEY = file.read().strip()
genai.configure(api_key=API_KEY)

# Load the Gemini model
base_model = "models/gemini-1.5-flash"
model = genai.GenerativeModel(model_name=base_model)

# Directories
PDF_DIR = "documents"
IMAGE_DIR = "documents_images"
LATEX_DIR = "documents_latex"

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LATEX_DIR, exist_ok=True)

def pdf_to_image(pdf_path, image_output_dir):
    """
    Converts a PDF to images (one per page) and saves them in the given directory.
    """
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Extract filename without extension
    save_dir = os.path.join(image_output_dir, pdf_name)
    os.makedirs(save_dir, exist_ok=True)

    images = convert_from_path(pdf_path)
    image_paths = []
    
    for i, image in enumerate(images):
        img_path = os.path.join(save_dir, f"page_{i + 1}.png")
        image.save(img_path, "PNG")
        image_paths.append(img_path)
    
    return image_paths

def image_to_latex(image_path):
    """
    Converts an image to LaTeX using the Gemini model.
    """
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = "Convert this image to LaTeX code."
    response = model.generate_content([
        {'mime_type': 'image/png', 'data': encoded_image}, 
        prompt
    ])
    
    return response.text if response else ""

def process_pdfs():
    """
    Converts all PDFs in the `documents/` directory to images, extracts LaTeX, and saves output.
    """
    for pdf_file in os.listdir(PDF_DIR):
        if pdf_file.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, pdf_file)
            print(f"Processing: {pdf_file}")

            # Convert PDF to images
            image_paths = pdf_to_image(pdf_path, IMAGE_DIR)

            # Convert images to LaTeX
            latex_code = ""
            for img_path in image_paths:
                latex_code += image_to_latex(img_path) + "\n\n"

            # Save LaTeX file
            latex_file_path = os.path.join(LATEX_DIR, os.path.splitext(pdf_file)[0] + ".tex")
            with open(latex_file_path, "w", encoding="utf-8") as tex_file:
                tex_file.write(latex_code)
            
            print(f"Saved LaTeX: {latex_file_path}")

if __name__ == "__main__":
    process_pdfs()

