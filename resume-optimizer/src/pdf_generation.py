from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from xml.sax.saxutils import escape

def generate_pdf(text_content, output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    normal = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )

    heading = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        spaceBefore=12,
        spaceAfter=6
    )

    story = []

    for line in text_content.split("\n"):
        line = line.strip()

        if not line:
            story.append(Spacer(1, 0.15 * inch))
            continue

        # Headings (SKILLS, EXPERIENCE, etc.)
        if line.isupper() and len(line) < 40:
            story.append(Paragraph(escape(line), heading))
            continue

        # Bullet points
        if line.startswith("- "):
            bullet = escape(line[2:])
            story.append(Paragraph(f"• {bullet}", normal))
            continue

        # Normal text
        story.append(Paragraph(escape(line), normal))

    doc.build(story)
