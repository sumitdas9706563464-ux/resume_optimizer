
import pytest
from src.keyword_extraction import extract_keywords, categorize_keywords
from src.ats_scoring import calculate_ats_score
from src.resume_updater import add_keywords_to_resume

def test_categorize_keywords():
    keywords = ["Python", "managed", "leadership", "AWS", "developed", "communication"]
    categories = categorize_keywords(keywords)

    assert "Technical Skills" in categories
    assert "Action Verbs" in categories
    assert "Soft Skills" in categories
    assert "Tools & Technologies" in categories

    # "managed" should be an Action Verb
    assert any(w.lower() == "managed" for w in categories["Action Verbs"])
    # "Python" should be a Tool/Tech or Technical Skill
    assert any(w.lower() == "python" for w in categories["Tools & Technologies"] + categories["Technical Skills"])

def test_ats_scoring_with_jd():
    resume_text = "John Doe. Email: john@example.com. Experience: Managed a team of 5. Skills: Python, Java."
    jd_keywords = ["Python", "leadership", "AWS"]

    score, feedback = calculate_ats_score(resume_text, jd_keywords)

    assert score > 0
    assert any("keyword match" in f.lower() for f in feedback)

def test_resume_updater_blending():
    resume_text = "Summary: Experienced developer.\nSkills: Python.\nExperience: Worked at Google."
    keywords_to_add = ["React", "managed", "leadership"]

    updated_text = add_keywords_to_resume(resume_text, keywords_to_add)

    assert "React" in updated_text
    assert "expertise includes" in updated_text.lower() or "skills" in updated_text.lower()
    # Check if experience was updated
    assert "utilized" in updated_text.lower() or "managed" in updated_text.lower()
