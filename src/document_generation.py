
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from docx import Document
from .resume_template import generate_professional_template

def generate_pdf(resume_text, file_path):
    """
    Generates a PDF resume from the given text using a professional template.
    """
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Use the professional template to structure the resume
    template = generate_professional_template(resume_text)

    # Simple HTML-like parsing to create the PDF
    for line in template.split('\n'):
        if line.startswith('<h1>'):
            story.append(Paragraph(line.replace('<h1>', '').replace('</h1>', ''), styles['h1']))
        elif line.startswith('<h2>'):
            story.append(Paragraph(line.replace('<h2>', '').replace('</h2>', ''), styles['h2']))
        elif line.startswith('<ul>'):
            pass  # Handled by list items
        elif line.startswith('  <li>'):
            story.append(Paragraph(f"• {line.replace('<li>', '').replace('</li>', '').strip()}", styles['Normal']))
        elif line.startswith('<p>'):
            story.append(Paragraph(line.replace('<p>', '').replace('</p>', ''), styles['Normal']))
        else:
            story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

    doc.build(story)

def generate_docx(resume_text, file_path):
    """
    Generates a DOCX resume from the given text using a professional template.
    """
    document = Document()
    template = generate_professional_template(resume_text)

    # Simple HTML-like parsing to create the DOCX
    for line in template.split('\n'):
        if line.startswith('<h1>'):
            document.add_heading(line.replace('<h1>', '').replace('</h1>', ''), level=1)
        elif line.startswith('<h2>'):
            document.add_heading(line.replace('<h2>', '').replace('</h2>', ''), level=2)
        elif line.startswith('<ul>'):
            pass  # Handled by list items
        elif line.startswith('  <li>'):
            document.add_paragraph(line.replace('<li>', '').replace('</li>', '').strip(), style='List Bullet')
        elif line.startswith('<p>'):
            document.add_paragraph(line.replace('<p>', '').replace('</p>', ''))
        else:
            document.add_paragraph(line)

    document.save(file_path)
