from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

def generate_resume_pdf(data, filename="resume.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    name_style = ParagraphStyle(
        "NameStyle",
        fontSize=18,
        spaceAfter=10,
        leading=22,
        alignment=1  # center
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6,
        leading=14,
        fontName="Helvetica-Bold"
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        fontSize=10,
        leading=14
    )

    # ===== HEADER =====
    story.append(Paragraph(data["name"], name_style))
    story.append(Paragraph(data["contact"], normal_style))
    story.append(Spacer(1, 12))

    # ===== SUMMARY =====
    story.append(Paragraph("SUMMARY", heading_style))
    story.append(Paragraph(data["summary"], normal_style))

    # ===== SKILLS =====
    story.append(Paragraph("SKILLS", heading_style))
    story.append(
        ListFlowable(
            [ListItem(Paragraph(skill, normal_style)) for skill in data["skills"]],
            bulletType="bullet"
        )
    )

    # ===== EXPERIENCE =====
    story.append(Paragraph("PROJECTS / EXPERIENCE", heading_style))
    for exp in data["experience"]:
        story.append(Paragraph(exp, normal_style))

    # ===== EDUCATION =====
    story.append(Paragraph("EDUCATION", heading_style))
    story.append(Paragraph(data["education"], normal_style))

    doc.build(story)
