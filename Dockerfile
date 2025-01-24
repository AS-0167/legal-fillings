FROM python:3.10-slim

# Install poppler-utils for pdf2image
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy application files
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the port Streamlit uses
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py"]

