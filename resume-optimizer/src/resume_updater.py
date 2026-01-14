import re

def add_keywords_to_resume(resume_text, keywords_to_add):
    """
    Adds missing keywords to the Skills section in bullet format.
    """

    skills_header_pattern = r'(?i)(^skills.*?$)'
    match = re.search(skills_header_pattern, resume_text, re.MULTILINE)

    unique_keywords = sorted(set(keywords_to_add))
    existing_text = resume_text.lower()
    new_keywords = [k for k in unique_keywords if k.lower() not in existing_text]

    if not new_keywords:
        return resume_text

    bullet_skills = "\n- " + "\n- ".join(new_keywords)

    if match:
        insert_pos = match.end()
        updated_resume = (
            resume_text[:insert_pos]
            + bullet_skills
            + resume_text[insert_pos:]
        )
    else:
        updated_resume = (
            resume_text
            + "\n\nSKILLS"
            + bullet_skills
        )

    return updated_resume
20