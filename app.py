import streamlit as st
import os
from fpdf import FPDF  # To generate PDF files
import google.generativeai as genai
from io import BytesIO  # For PDF download
from charset_normalizer import from_path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Configure the generative AI
with open("api.key", "r") as file:
    API_KEY = file.read().strip()
genai.configure(api_key=API_KEY)
base_model = "models/gemini-1.5-flash-001-tuning"
model = genai.GenerativeModel(model_name=base_model)

# List of document names
documents = [
    'affiidavit_rawalpindi',
    'application_for_certificate_of_domicile',
    'application_for_copy_of_domicile_certificate',
    'application_for_permission_to_build',
    'application_for_wood_transit_permit',
    'assets_form',
    'certificate_of_domicile',
    'police_character_certificate',
    'undertaking_for_construction'
]

def get_info_file(doc_name):
    """Get the path to the info file of the document"""
    return f"informations/{doc_name}_info.txt"

def get_filled_info_file(doc_name):
    """Get the path to save the filled info"""
    return f"informations_filled/{doc_name}_info_filled.txt"

def get_filled_pdf_file(doc_name):
    """Get the path to save the PDF"""
    return f"documents_filled/{doc_name}.pdf"


def get_pdf_file(doc_name):
    """Get the path to save the PDF"""
    return f"documents_txt/{doc_name}.txt"



def extract_required_information(document_text, output_path):
    """Uses Gemini AI to extract required information fields from a legal document."""
    
    prompt = f"""
    You are an AI assistant specialized in analyzing legal documents. Your task is to extract 
    the required information fields that a user needs to fill in a given legal document.

    **Instructions:**
    1. Read the provided legal document.
    2. Identify all the placeholders, underscores, or missing information that a user must fill.
    3. Return only a list of required fields, without explaining anything else.
    4. Each extracted field should be a short, clear phrase (e.g., "Full Name", "Father’s Name", "NIC Number").
    5. If the document does not require any user input, return an empty list.

    **Example Input Document:**
    ```
    A F F I D A V I T  
    I, _______________ S/o _________________ resident of 
    __________________________________________________________ do hereby solemnly  
    affirm and declare as under: - 
    1. That I am residing in district Rawalpindi since _____________ .
    2. That I never migrated to India on or after 1st March 1947.  
    3. That the particulars furnished by me in the application forms for the grant of 
    domicile certificate are correct.  
    4. That I neither obtained nor shall obtain the same from any other district of  
    Pakistan after having been granted this one.  
    Deponent.  __________________________  
    NIC NO.  __________________________  
    ```

    **Expected Output:**
    ```
    Full Name of Deponent
    Father’s Name
    Residential Address
    Duration of residence in District Rawalpindi
    NIC Number
    ```

    **Now process the following document and extract required fields:**
    ```
    {document_text}
    ```
    """

    response = model.generate_content(prompt)
    
    try:
        extracted_fields = response.text.strip().split("\n")
        extracted_fields = [field.strip("-*• ") for field in extracted_fields if field.strip()]

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the extracted information fields to a text file
        with open(output_path, "w", encoding="utf-8") as f:
            for field in extracted_fields:
                f.write(f"{field}\n")

        print(f"Extracted information saved to {output_path}")

    except Exception as e:
        print(f"Error in extracting required fields: {e}")

def convert_text_to_pdf(text, pdf_path):
    """
    Convert a string of text to a PDF file and save it to the specified path.

    Parameters:
    - text (str): The text content to be converted into a PDF.
    - pdf_path (str): The output file path where the PDF will be saved.
    """
    try:
        # Ensure the directory for the PDF file exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # Create a PDF
        pdf = canvas.Canvas(pdf_path, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        width, height = letter
        x, y = 50, height - 50  # Starting coordinates

        for line in text.split("\n"):
            if y < 50:  # If the page bottom is reached, create a new page
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = height - 50
            pdf.drawString(x, y, line.strip())  # Write line to PDF
            y -= 15  # Move cursor down for the next line

        # Save the PDF
        pdf.save()
        print(f"PDF successfully created and saved to: {pdf_path}")

    except Exception as e:
        print(f"Error converting text to PDF: {e}")

# from markdown2 import markdown
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Paragraph

# def convert_text_to_pdf(markdown_text, pdf_path):
#     """
#     Convert Markdown text to a beautifully formatted PDF.

#     Parameters:
#     - markdown_text (str): The Markdown content to be converted into a PDF.
#     - pdf_path (str): The output file path where the PDF will be saved.
#     """
#     try:
#         # Ensure the directory for the PDF file exists
#         os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

#         # Convert Markdown to HTML
#         html_content = markdown(markdown_text)

#         # Create a ReportLab PDF
#         doc = SimpleDocTemplate(pdf_path, pagesize=letter)
#         styles = getSampleStyleSheet()
#         story = []

#         # Create a Paragraph from the HTML content
#         story.append(Paragraph(html_content, styles["Normal"]))

#         # Build the PDF
#         doc.build(story)
#         print(f"PDF successfully created and saved to: {pdf_path}")

#     except Exception as e:
#         print(f"Error converting Markdown to PDF: {e}")


def generate_ai_response(document, information):
    """Generate a filled document using Generative AI"""
    prompt = f'''
    You are an AI assistant tasked with helping users create legal documents.
    Your job is to take a template of a legal document (which contains placeholders for certain pieces of information) 
    and then fill in the placeholders with the information provided by the user.

    Inputs:
    1. Template document: {document}
    2. User Information: {information}

    Please fill in the placeholders and return a neatly formatted document.
    Also keep the indentation and formatting consistent with the original document.

    '''
    # Also return the response in markdown formate make appropriate headings etc.
    try:
        response = model.generate_content(prompt)
        print(document)
        print(response.text)
        return response.text
    except ValueError as e:
        print("Error generating AI response:", e)
        return "Error: Unable to process the document. Please ensure your inputs are valid and try again."


# Streamlit app interface
st.title("Legal Document Filling Service")

# Display document buttons
selected_doc = st.selectbox("Select a Document", documents)

# Check if the selected document has an info file
pdf_doc = get_pdf_file(selected_doc)
info_file = get_info_file(selected_doc)

# Open the file
with open(pdf_doc, "r", encoding="utf-8") as doc_template:
    document_template = doc_template.read()

extract_required_information(document_template, info_file)

if os.path.exists(info_file):

    # If info file exists, read its contents (questions to be filled)
    with open(info_file, 'r') as f:
        print("file is there")
        info_lines = f.readlines()

    st.write(f"Please fill the required information for the document: {selected_doc.replace('_', ' ').title()}")

    # Create a form to collect the user input
    with st.form(key="document_form"):
        user_inputs = {}
        for idx, line in enumerate(info_lines):  # Using enumerate() to create unique keys
            question = line.strip()
            user_input = st.text_input(question, key=f"{selected_doc}_{idx}")  # UNIQUE KEY ADDED
            user_inputs[question] = st.session_state.get(f"{selected_doc}_{idx}", "")  # Retrieve input value

        print("here...............")
        # Submit button to save the filled info
        submit_button = st.form_submit_button("Submit Information")

        if submit_button:
            # Save the filled information
            filled_info_file = get_filled_info_file(selected_doc)
            os.makedirs(os.path.dirname(filled_info_file), exist_ok=True)
            with open(filled_info_file, 'w') as f:
                for question, answer in user_inputs.items():
                    f.write(f"{question}: {answer}\n")

            # Generate the AI response
            information_str = "\n".join([f"{k}: {v}" for k, v in user_inputs.items()])
            
            ai_response = generate_ai_response(document_template, information_str)

            # Convert AI response to PDF
            pdf_path = get_filled_pdf_file(selected_doc)
            convert_text_to_pdf(ai_response, pdf_path)

            st.success(f"Information for {selected_doc.replace('_', ' ').title()} has been processed successfully!")
else:
    # If info file does not exist, display a message
    st.warning(f"The service for '{selected_doc.replace('_', ' ').title()}' is not available at the moment.")

