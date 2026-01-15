
import re

def calculate_ats_score(resume_text):
    """
    Calculates an ATS score for a resume based on predefined criteria.
    """
    score = 0
    feedback = []

    # Criterion 1: Contact Information
    contact_info_score, contact_feedback = check_contact_information(resume_text)
    score += contact_info_score
    feedback.extend(contact_feedback)

    # Criterion 2: Key Sections
    sections_score, sections_feedback = check_key_sections(resume_text)
    score += sections_score
    feedback.extend(sections_feedback)

    # Criterion 3: Action Verbs
    action_verbs_score, action_verbs_feedback = check_action_verbs(resume_text)
    score += action_verbs_score
    feedback.extend(action_verbs_feedback)

    # Criterion 4: Quantifiable Achievements
    quantifiable_achievements_score, quantifiable_achievements_feedback = check_quantifiable_achievements(resume_text)
    score += quantifiable_achievements_score
    feedback.extend(quantifiable_achievements_feedback)

    return min(score, 100), feedback

def check_contact_information(text):
    """
    Checks for the presence of contact information like email and phone number.
    """
    score = 0
    feedback = []

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

    if re.search(email_pattern, text):
        score += 10
    else:
        feedback.append("Missing email address.")

    if re.search(phone_pattern, text):
        score += 10
    else:
        feedback.append("Missing phone number.")

    return score, feedback

def check_key_sections(text):
    """
    Checks for the presence of key resume sections.
    """
    score = 0
    feedback = []

    required_sections = ["experience", "education", "skills"]

    for section in required_sections:
        if re.search(r'\b' + section + r'\b', text, re.IGNORECASE):
            score += 10
        else:
            feedback.append(f"Missing '{section.capitalize()}' section.")

    return score, feedback

def check_action_verbs(text):
    """
    Checks for the use of action verbs.
    """
    score = 0
    feedback = []

    action_verbs = ["managed", "led", "developed", "created", "implemented", "achieved", "increased", "reduced"]

    found_verbs = 0
    for verb in action_verbs:
        if re.search(r'\b' + verb + r'\b', text, re.IGNORECASE):
            found_verbs += 1

    if found_verbs >= 3:
        score += 20
    elif found_verbs >= 1:
        score += 10
    else:
        feedback.append("Include more action verbs to describe your accomplishments.")

    return score, feedback

def check_quantifiable_achievements(text):
    """
    Checks for quantifiable achievements (e.g., numbers, percentages).
    """
    score = 0
    feedback = []

    # Looks for numbers, percentages, and currency symbols
    quantifiable_pattern = r'(\d+%|\$\d+|\d+\s?(million|billion|thousand)|\d{3,})'

    if re.search(quantifiable_pattern, text):
        score += 20
    else:
        feedback.append("Add quantifiable achievements to demonstrate your impact (e.g., 'Increased sales by 20%').")

    return score, feedback
