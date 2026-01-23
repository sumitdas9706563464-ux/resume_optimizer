
import re
from .keyword_extraction import categorize_keywords

def add_keywords_to_resume(resume_text, keywords_to_add):
    """
    Naturally blends keywords into the Summary, Skills, and Experience sections.
    """
    if not keywords_to_add:
        return resume_text

    categories = categorize_keywords(keywords_to_add)

    technical_and_tools = list(set(categories.get("Technical Skills", []) + categories.get("Tools & Technologies", [])))
    soft_skills = categories.get("Soft Skills", [])
    action_verbs = categories.get("Action Verbs", [])

    updated_text = resume_text

    # 1. Update Summary Section
    # Use lookahead for the boundary to avoid consuming it
    summary_match = re.search(r'(?is)(summary|objective|profile)(.*?)(?=\n\n|\n[A-Z]|$)', updated_text)
    if summary_match:
        summary_title = summary_match.group(1)
        summary_content = summary_match.group(2).strip()

        # Add a few top technical skills to the summary
        summary_keywords = technical_and_tools[:min(5, len(technical_and_tools))]
        if summary_keywords:
            new_summary_sentence = f" Expertise includes {', '.join(summary_keywords)}."
            if new_summary_sentence.lower() not in summary_content.lower():
                updated_content = summary_content + new_summary_sentence
                # Replace only the content part if possible, or reconstruct carefully
                updated_text = updated_text[:summary_match.start(2)] + " " + updated_content + updated_text[summary_match.end(2):]

    # 2. Update Skills Section
    skills_match = re.search(r'(?is)(skills|technical skills|proficiencies)(.*?)(?=\n\n|\n[A-Z]|$)', updated_text)
    all_skills_to_add = technical_and_tools + soft_skills

    if skills_match:
        skills_title = skills_match.group(1)
        existing_skills_block = skills_match.group(2)

        # Filter out already existing skills
        new_skills = [s for s in all_skills_to_add if s.lower() not in existing_skills_block.lower()]

        if new_skills:
            # Add as bullet points
            new_skills_text = "\n" + "\n".join(f"- {s}" for s in new_skills)
            updated_skills_block = existing_skills_block.rstrip() + new_skills_text
            updated_text = updated_text[:skills_match.start(2)] + updated_skills_block + updated_text[skills_match.end(2):]
    else:
        # Create Skills section if missing
        skills_text = f"\n\nSkills\n" + "\n".join(f"- {s}" for s in all_skills_to_add)
        updated_text += skills_text

    # 3. Update Experience Section
    experience_match = re.search(r'(?is)(experience|work history|employment)(.*?)(?=\n\n|\n[A-Z]|$)', updated_text)
    if experience_match:
        exp_content = experience_match.group(2)

        # Use whatever keywords we have left
        relevant_verbs = action_verbs
        relevant_tech = technical_and_tools

        if relevant_tech or relevant_verbs:
            new_bullet = "\n- "
            if relevant_verbs:
                new_bullet += f"{relevant_verbs[0].capitalize()} projects using "
            else:
                new_bullet += "Utilized "

            if relevant_tech:
                new_bullet += f"{', '.join(relevant_tech[:10])} "

            new_bullet += "to achieve key business objectives."

            # Find the first block of experience
            blocks = exp_content.split('\n\n')
            if blocks:
                first_block = blocks[0]
                updated_first_block = first_block.rstrip() + new_bullet
                # Be careful with replace to avoid multiple replacements if the text is generic
                updated_text = updated_text[:experience_match.start(2)] + exp_content.replace(first_block, updated_first_block, 1) + updated_text[experience_match.end(2):]

    return updated_text
