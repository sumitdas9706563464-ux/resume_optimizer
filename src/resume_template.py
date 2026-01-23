
import re

def generate_professional_template(resume_text):
    """
    Parses resume text and formats it into a professional, ATS-friendly template.
    Returns a structured dictionary instead of just a string to allow better PDF generation.
    """

    sections = {
        "name": "Professional Candidate",
        "contact": "",
        "summary": "",
        "skills": [],
        "experience": [],
        "education": []
    }

    # Define regex patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    linkedin_pattern = r'linkedin\.com/in/[A-Za-z0-9_-]+'

    # Try to extract Name (usually the first line or first few words)
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    if lines:
        if len(lines[0].split()) <= 4: # Likely a name
            sections["name"] = lines[0]

    # Extract Contact Info
    email = re.search(email_pattern, resume_text)
    phone = re.search(phone_pattern, resume_text)
    linkedin = re.search(linkedin_pattern, resume_text, re.IGNORECASE)

    contact_parts = []
    if email: contact_parts.append(email.group(0))
    if phone: contact_parts.append(phone.group(0))
    if linkedin: contact_parts.append(linkedin.group(0))
    sections["contact"] = " | ".join(contact_parts)

    # Extract Sections
    summary_match = re.search(r'(?is)(summary|objective|profile)(.*?)(\n[A-Z][a-z]+|\n\n|$)', resume_text)
    if summary_match:
        sections["summary"] = summary_match.group(2).strip()

    skills_match = re.search(r'(?is)(skills|technical skills|proficiencies)(.*?)(\n[A-Z][a-z]+|\n\n|$)', resume_text)
    if skills_match:
        skill_items = [s.strip('- •*') for s in skills_match.group(2).strip().split('\n') if s.strip()]
        # Handle comma-separated skills
        final_skills = []
        for item in skill_items:
            if ',' in item:
                final_skills.extend([s.strip() for s in item.split(',') if s.strip()])
            else:
                final_skills.append(item)
        sections["skills"] = final_skills

    exp_match = re.search(r'(?is)(experience|work history|employment)(.*?)(\n(education|skills|academic)|\n\n[A-Z]|$)', resume_text)
    if exp_match:
        # Split by what looks like new job entries (e.g., Year or common patterns)
        # For now, just split by double newlines or lines starting with dates
        exp_items = [item.strip() for item in exp_match.group(2).strip().split('\n\n') if item.strip()]
        sections["experience"] = exp_items

    edu_match = re.search(r'(?is)(education|academic background)(.*)', resume_text)
    if edu_match:
        sections["education"] = [item.strip() for item in edu_match.group(2).strip().split('\n\n') if item.strip()]

    return sections

def get_html_template(sections):
    """
    Optional: Converts structured sections to HTML for display or alternative uses.
    """
    html = f"<h1>{sections['name']}</h1>"
    html += f"<p>{sections['contact']}</p>"

    if sections['summary']:
        html += "<h2>Summary</h2>"
        html += f"<p>{sections['summary']}</p>"

    if sections['skills']:
        html += "<h2>Skills</h2><ul>"
        for skill in sections['skills']:
            html += f"<li>{skill}</li>"
        html += "</ul>"

    if sections['experience']:
        html += "<h2>Experience</h2>"
        for item in sections['experience']:
            html += f"<p>{item.replace('\n', '<br>')}</p>"

    if sections['education']:
        html += "<h2>Education</h2>"
        for item in sections['education']:
            html += f"<p>{item.replace('\n', '<br>')}</p>"

    return html
