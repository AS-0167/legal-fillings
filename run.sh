#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run scripts in sequence
python load_pdfs_as_txt.py
python load_pdfs_as_latex.py
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
