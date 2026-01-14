
import pdfplumber
import re

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
