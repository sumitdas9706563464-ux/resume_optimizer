import re

def add_keywords_to_resume(resume_text, keywords_to_add):
    """
    Adds keywords as bullet points under the Skills section.
    If Skills section does not exist, it creates one.
    """

    keywords_to_add = sorted(set(keywords_to_add))

    # Regex to capture full Skills section
    skills_pattern = re.compile(
        r'(?is)(skills|technical skills|proficiencies)\s*\n(.*?)(\n\n|$)'
    )

    match = skills_pattern.search(resume_text)

    if match:
        skills_title = match.group(1)
        existing_skills_block = match.group(2)

        # Extract existing skills (bullets or commas)
        existing_skills = re.findall(r'[\w\+\#\.]+', existing_skills_block.lower())

        # Filter new keywords
        new_skills = [
            skill for skill in keywords_to_add
            if skill.lower() not in existing_skills
        ]

        if not new_skills:
            return resume_text  # nothing to add

        # Convert to bullet format
        new_skills_text = "\n" + "\n".join(f"- {skill}" for skill in new_skills)

        updated_skills_block = existing_skills_block.rstrip() + new_skills_text

        updated_resume = (
            resume_text[:match.start(2)] +
            updated_skills_block +
            resume_text[match.end(2):]
        )

        return updated_resume

    else:
        # Create a new Skills section
        skills_section = "\n\nSkills\n" + "\n".join(f"- {k}" for k in keywords_to_add)
        return resume_text + skills_section
