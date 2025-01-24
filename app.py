import streamlit as st
import os
import google.generativeai as genais
import subprocess
import shutil

# Configure the generative AI
with open("api.key", "r") as file:
    API_KEY = file.read().strip()
genais.configure(api_key=API_KEY)
base_model = "models/gemini-1.5-flash-001-tuning"
model = genais.GenerativeModel(model_name=base_model)

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

def get_filled_laetx_file(doc_name):
    """Get the path to save the latex"""
    return f"documents_latex_filled/{doc_name}.tex"


def get_txt_file(doc_name):
    """Get the path to the txt file"""
    return f"documents_txt/{doc_name}.txt"

def get_latex_file(doc_name):
    """Get the path to the latex file"""
    return f"documents_latex/{doc_name}.tex"

def save_the_latex_file(latex_path, latex_code) :
    with open(latex_path, "w", encoding="utf-8") as tex_file:
        tex_file.write(latex_code)
    print("LaTeX code generated and saved as output.tex")

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

# def convert_text_to_pdf(text, pdf_path):
#     """
#     Convert a string of text to a PDF file and save it to the specified path.

#     Parameters:
#     - text (str): The text content to be converted into a PDF.
#     - pdf_path (str): The output file path where the PDF will be saved.
#     """
#     try:
#         # Ensure the directory for the PDF file exists
#         os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

#         # Create a PDF
#         pdf = canvas.Canvas(pdf_path, pagesize=letter)
#         pdf.setFont("Helvetica", 12)
#         width, height = letter
#         x, y = 50, height - 50  # Starting coordinates

#         for line in text.split("\n"):
#             if y < 50:  # If the page bottom is reached, create a new page
#                 pdf.showPage()
#                 pdf.setFont("Helvetica", 12)
#                 y = height - 50
#             pdf.drawString(x, y, line.strip())  # Write line to PDF
#             y -= 15  # Move cursor down for the next line

#         # Save the PDF
#         pdf.save()
#         print(f"PDF successfully created and saved to: {pdf_path}")

#     except Exception as e:
#         print(f"Error converting text to PDF: {e}")




def latex_to_pdf(tex_path, output_dir="documents_filled"):
    """
    Converts a LaTeX (.tex) file to PDF using Tectonic and stores it in a separate output directory.

    Parameters:
        tex_path (str): Path to the .tex file.
        output_dir (str): Directory where the generated PDF should be saved.

    Returns:
        str: Path to the generated PDF if successful, else None.
    """
    if not os.path.exists(tex_path):
        print(f"❌ Error: File '{tex_path}' not found.")
        return None

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Get directory and filename separately
        tex_dir = os.path.dirname(os.path.abspath(tex_path))
        tex_filename = os.path.basename(tex_path)

        # Run tectonic in the same directory as the .tex file
        subprocess.run(
            ["tectonic", tex_filename],  # Pass only the filename
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=tex_dir  # Change working directory to where .tex file is located
        )

        # Get the generated PDF path (same as .tex file but with .pdf extension)
        pdf_filename = os.path.splitext(tex_filename)[0] + ".pdf"
        generated_pdf_path = os.path.join(tex_dir, pdf_filename)

        # Define the final destination path in the output directory
        output_pdf_path = os.path.join(output_dir, pdf_filename)

        # Move the generated PDF to the output directory
        if os.path.exists(generated_pdf_path):
            shutil.move(generated_pdf_path, output_pdf_path)
            print(f"✅ PDF successfully generated and moved to: {output_pdf_path}")
            return output_pdf_path
        else:
            print("❌ Error: PDF not generated.")
            return None

    except subprocess.CalledProcessError as e:
        print("❌ Tectonic failed:", e.stderr.decode())
        return None

def generate_ai_response(document, information, latex_code):
    """Generate a filled document using Generative AI"""
    prompt = f'''
        You are an AI that specializes in processing LaTeX documents. 
        Your task is to take a document template written in text form, a set of filled information fields, and a LaTeX document structure. 
        Using these inputs, you must replace the placeholders in the LaTeX code with the provided information and generate a final, correctly formatted LaTeX document.

    Inputs:
        Document Template (Text Form): {document}
        Filled Information Fields: {information}
        LaTeX Code: {latex_code}        
    Instructions:
        Identify all placeholders in the LaTeX code that need to be filled with the provided information.
        Replace each placeholder with the corresponding value from the filled information fields.
        Preserve the LaTeX syntax and structure while ensuring correct formatting.
        Ensure that special LaTeX characters (like _, %, $) are properly escaped.
        Return only the final LaTeX document without any extra text.

    Output Format:
        A valid, fully formatted LaTeX document with the placeholders replaced by the provided values.

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
pdf_doc = get_txt_file(selected_doc)
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

            # load the latex file
            latex_file = get_latex_file(selected_doc)
            with open(latex_file, "r") as f:
                latex_code = f.read()

            # Generate the AI response
            information_str = "\n".join([f"{k}: {v}" for k, v in user_inputs.items()])
            
            ai_response = generate_ai_response(document_template, information_str, latex_code)

            # Convert AI response to PDF
            pdf_path = get_filled_pdf_file(selected_doc)
            latex_path = get_filled_laetx_file(selected_doc)
            save_the_latex_file(latex_path, ai_response)

            with open(latex_path, "r") as lx:
                latex_filled = lx.read()
            latex_to_pdf(latex_path) 

            # convert_text_to_pdf(ai_response, pdf_path)

            st.success(f"Information for {selected_doc.replace('_', ' ').title()} has been processed successfully!")
else:
    # If info file does not exist, display a message
    st.warning(f"The service for '{selected_doc.replace('_', ' ').title()}' is not available at the moment.")


