
import re

def generate_professional_template(resume_text):
    """
    Parses resume text and formats it into a professional, ATS-friendly template.
    """

    # Define regex patterns for different sections
    name_pattern = r'([A-Z][a-z]+)\s+([A-Z][a-z]+)'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    summary_pattern = re.compile(r'(summary|objective)(.*?)(\n\n|skills|experience|education)', re.IGNORECASE | re.DOTALL)
    skills_pattern = re.compile(r'(skills|technical skills|proficiencies)(.*?)(\n\n|experience|education|projects)', re.IGNORECASE | re.DOTALL)
    experience_pattern = re.compile(r'(experience|work history|employment)(.*?)(\n\n|education|skills|projects)', re.IGNORECASE | re.DOTALL)
    education_pattern = re.compile(r'(education|academic background)(.*)', re.IGNORECASE | re.DOTALL)

    # Extract information using regex
    name_match = re.search(name_pattern, resume_text)
    email_match = re.search(email_pattern, resume_text)
    phone_match = re.search(phone_pattern, resume_text)
    summary_match = re.search(summary_pattern, resume_text)
    skills_match = re.search(skills_pattern, resume_text)
    experience_match = re.search(experience_pattern, resume_text)
    education_match = re.search(education_pattern, resume_text)

    # Build the template
    template = ""

    # Header
    if name_match:
        template += f"<h1>{name_match.group(0)}</h1>\n"
    if email_match or phone_match:
        template += f"<p>{email_match.group(0) if email_match else ''} | {phone_match.group(0) if phone_match else ''}</p>\n\n"

    # Summary
    if summary_match:
        template += "<h2>Summary</h2>\n"
        template += f"<p>{summary_match.group(2).strip()}</p>\n\n"

    # Skills
    if skills_match:
        template += "<h2>Skills</h2>\n"
        skills = [skill.strip() for skill in skills_match.group(2).strip().split('\n') if skill.strip()]
        template += "<ul>\n"
        for skill in skills:
            template += f"  <li>{skill}</li>\n"
        template += "</ul>\n\n"

    # Experience
    if experience_match:
        template += "<h2>Experience</h2>\n"
        experience_items = [item.strip() for item in experience_match.group(2).strip().split('\n\n') if item.strip()]
        for item in experience_items:
            template += f"<p>{item}</p>\n"
        template += "\n"

    # Education
    if education_match:
        template += "<h2>Education</h2>\n"
        template += f"<p>{education_match.group(2).strip()}</p>\n\n"

    return template
