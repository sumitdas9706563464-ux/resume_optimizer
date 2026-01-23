
import re

def calculate_ats_score(resume_text, jd_keywords=None):
    """
    Calculates a comprehensive ATS score for a resume.
    """
    score = 0
    feedback = []

    # 1. Contact Information (20 points)
    contact_info_score, contact_feedback = check_contact_information(resume_text)
    score += contact_info_score
    feedback.extend(contact_feedback)

    # 2. Key Sections (20 points)
    sections_score, sections_feedback = check_key_sections(resume_text)
    score += sections_score
    feedback.extend(sections_feedback)

    # 3. Action Verbs (15 points)
    action_verbs_score, action_verbs_feedback = check_action_verbs(resume_text)
    score += action_verbs_score
    feedback.extend(action_verbs_feedback)

    # 4. Quantifiable Achievements (15 points)
    quantifiable_achievements_score, quantifiable_achievements_feedback = check_quantifiable_achievements(resume_text)
    score += quantifiable_achievements_score
    feedback.extend(quantifiable_achievements_feedback)

    # 5. Keyword Match (30 points) - if JD keywords are provided
    if jd_keywords:
        match_score, match_feedback = check_keyword_match(resume_text, jd_keywords)
        score += match_score
        feedback.extend(match_feedback)
    else:
        # Default match score if no JD provided yet
        score += 0
        feedback.append("Upload a job description to see your keyword match score.")

    # 6. Formatting & Length (Bonus/Penalty)
    length_score, length_feedback = check_resume_length(resume_text)
    score += length_score
    feedback.extend(length_feedback)

    return min(max(score, 0), 100), feedback

def check_contact_information(text):
    score = 0
    feedback = []

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    linkedin_pattern = r'linkedin\.com/in/[A-Za-z0-9_-]+'

    if re.search(email_pattern, text):
        score += 7
    else:
        feedback.append("Missing email address.")

    if re.search(phone_pattern, text):
        score += 7
    else:
        feedback.append("Missing phone number.")

    if re.search(linkedin_pattern, text, re.IGNORECASE):
        score += 6
    else:
        feedback.append("Missing LinkedIn profile link.")

    return score, feedback

def check_key_sections(text):
    score = 0
    feedback = []
    required_sections = {
        "experience": ["experience", "work history", "employment"],
        "education": ["education", "academic background"],
        "skills": ["skills", "technical skills", "proficiencies"],
        "summary": ["summary", "objective", "profile"]
    }

    for section, keywords in required_sections.items():
        found = False
        for keyword in keywords:
            if re.search(r'\b' + keyword + r'\b', text, re.IGNORECASE):
                found = True
                break
        if found:
            score += 5
        else:
            feedback.append(f"Missing '{section.capitalize()}' section.")

    return score, feedback

def check_action_verbs(text):
    score = 0
    feedback = []
    action_verbs = [
        "managed", "led", "developed", "created", "implemented", "achieved",
        "increased", "reduced", "spearheaded", "designed", "optimized"
    ]

    found_verbs = 0
    for verb in action_verbs:
        if re.search(r'\b' + verb + r'\b', text, re.IGNORECASE):
            found_verbs += 1

    if found_verbs >= 5:
        score += 15
    elif found_verbs >= 2:
        score += 10
    elif found_verbs >= 1:
        score += 5
    else:
        feedback.append("Use more strong action verbs (e.g., 'Spearheaded', 'Optimized').")

    return score, feedback

def check_quantifiable_achievements(text):
    score = 0
    feedback = []
    quantifiable_pattern = r'(\d+%|\$\d+|\d+\s?(million|billion|thousand)|\d{3,})'

    matches = re.findall(quantifiable_pattern, text)
    if len(matches) >= 3:
        score += 15
    elif len(matches) >= 1:
        score += 10
        feedback.append("Add more quantifiable results to showcase your impact.")
    else:
        feedback.append("Include numbers, percentages, or budgets to quantify your achievements.")

    return score, feedback

def check_keyword_match(text, jd_keywords):
    score = 0
    feedback = []

    text_lower = text.lower()
    found_count = 0
    for keyword in jd_keywords:
        if keyword.lower() in text_lower:
            found_count += 1

    if not jd_keywords:
        return 0, []

    match_percentage = (found_count / len(jd_keywords)) * 100

    # Scale 30 points based on match percentage
    score = (match_percentage / 100) * 30

    if match_percentage < 40:
        feedback.append(f"Low keyword match ({match_percentage:.1f}%). Add more relevant skills from the job description.")
    elif match_percentage < 70:
        feedback.append(f"Moderate keyword match ({match_percentage:.1f}%). Try to include missing key terms.")
    else:
        feedback.append("Excellent keyword match!")

    return int(score), feedback

def check_resume_length(text):
    score = 0
    feedback = []
    word_count = len(text.split())

    if word_count < 200:
        score -= 5
        feedback.append("Resume is too short. Expand on your experience and skills.")
    elif word_count > 1500:
        score -= 5
        feedback.append("Resume is quite long. Try to keep it concise and under 2 pages.")

    return score, feedback
