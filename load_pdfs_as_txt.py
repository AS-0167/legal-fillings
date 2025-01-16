import os
from PyPDF2 import PdfReader

def save_pdf_as_text(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        # Check if the file has a .pdf extension
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(output_dir, output_filename)
            try:
                # Read the PDF
                reader = PdfReader(input_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                # Save the extracted text to a .txt file
                with open(output_path, "w", encoding="utf-8") as text_file:
                    text_file.write(text)
                print(f"Converted: {filename} -> {output_filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Define input and output directories
input_directory = "documents"
output_directory = "documents_txt"

# Convert PDFs to text
save_pdf_as_text(input_directory, output_directory)
