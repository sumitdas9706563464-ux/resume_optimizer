
import pdfplumber
import re
import docx2txt
import os

def extract_text_from_pdf(pdf_path):
    """
    Extracts clean text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted and cleaned text.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text from the page
            page_text = page.extract_text()

            # A simple heuristic to remove headers/footers:
            # Assumes they are in the top/bottom 10% of the page
            lines = page_text.split('\n')
            # This can be adjusted based on resume format
            if len(lines) > 10: # Only filter if there are enough lines
                filtered_lines = lines[int(len(lines) * 0.05):int(len(lines) * 0.95)]
            else:
                filtered_lines = lines
            text += '\n'.join(filtered_lines)

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def extract_text_from_docx(docx_path):
    """
    Extracts text from a DOCX file.
    """
    text = docx2txt.process(docx_path)
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text(file_path):
    """
    Extracts text from a file, supporting PDF and DOCX formats.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file was not found at: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
