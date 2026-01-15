
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_dummy_pdf(filename, text):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.drawString(72, height - 72, text)
    c.save()

if __name__ == "__main__":
    create_dummy_pdf("tests/dummy_resume.pdf", "This is a dummy resume.")
