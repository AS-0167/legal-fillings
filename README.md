# 📝 Legal Fillings

## 📌 Overview
**Legal-Fillings** is an AI-powered web application designed to simplify the process of filling out legal documents and application forms. This project aims to assist users in quickly and accurately completing various legal forms without the hassle of manual data entry. With built-in AI assistance, users only need to provide their basic details, and the system will automatically generate a well-structured, professional document.

## 🚀 Features
- **Preloaded Legal Documents**: The application includes several commonly used legal documents and forms by default.
- **AI-Powered Form Filling**: Utilizes **Google AI Studio** to intelligently populate documents based on user input.
- **Custom Document Addition**: Users can add new legal documents as needed.
- **PDF Generation**: Automatically generates a filled PDF version of the document.
- **Secure API Key Management**: Uses an API key stored in a local file for secure AI access.

## 📜 Default Legal Documents
Form-Filler comes with the following default legal documents:

✔️ **Affidavit (Rawalpindi)**

✔️ **Application for Certificate of Domicile**

✔️ **Application for Copy of Domicile Certificate**

✔️ **Application for Permission to Build**

✔️ **Application for Wood Transit Permit**

✔️ **Assets Form**

✔️ **Certificate of Domicile**

✔️ **Police Character Certificate**

✔️ **Undertaking for Construction**

All these documents are stored in the **documents/** folder.

## 🛠 Installation Guide

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/AS-0167/legal-fillings.git
cd legal-fillings
```

### **2️⃣ Install Docker (if not installed)**  
Make sure Docker is installed on your machine. Follow the installation guide for your operating system from the official Docker website:  
[Install Docker](https://docs.docker.com/get-docker/)

### **3️⃣ Build and Run the Docker Container**
To quickly set up and run the application in a Docker container, use the following commands:

1. Build the Docker image:
   ```bash
   docker build -t form-filling-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 8501:8501 form-filling-app
   ```
3. Run the app :
   
  This will start the **Form-Filler** app in a Docker container, and you can access it by going to the follwing link in your web browser.
  ```
  http://localhost:8501
  ```

### **4️⃣ Install Dependencies (for local setup without Docker)**
If you prefer to run the app without Docker, ensure that you have Python installed. Then, install the required packages using:
```bash
pip install -r requirements.txt
```

### **5️⃣ Set Up Your API Key**
Form-Filler uses **Google AI Studio** for AI-driven form filling. To set up:
1. Go to [Google AI Studio](https://aistudio.google.com/apikey) and generate an API key.
2. Save the API key in a file named **`api.key`** in the project root directory.

## 📂 Adding New Documents
If you want to add a new document to the system:
1. Place the PDF file inside the `documents/` folder.
2. Run the following script to convert and integrate the new document:
```bash
python load_pdfs_as_txt.py
```
This will convert the newly added PDFs into text format so that the AI can process them.

## 🎯 Running the Application
- **Using Docker**: If you are using Docker, simply run the container as described above, and the app will be accessible at `http://localhost:8501`.
- **Without Docker**: If you're not using Docker, run the following command:
```bash
streamlit run app.py
```
This will launch the **Form-Filler** web interface in your default browser.

## 📌 How It Works
1. **Select a Legal Document**: Choose a document from the provided list.
2. **Enter Required Information**: The app will prompt you for the necessary details.
3. **AI-Powered Form Completion**: Google AI Studio fills in the document based on your input.
4. **Download the Completed PDF**: The generated document is downloaded in the folder `documents_filled/`.

## 🤝 Contributing
We welcome contributions! Feel free to fork this repository, submit issues, or create pull requests to improve the project.

---
### **🔹 Form-Filler: Making Legal Documentation Effortless! 🔹**
