
def generate_explanations(gap_analysis_result):
    """
    Generates human-readable explanations for the gap analysis.

    Args:
        gap_analysis_result (dict): The result from the analyze_gaps function.

    Returns:
        dict: A dictionary with explanations for missing and matched keywords.
    """
    explanations = {
        'missing': [],
        'matches': []
    }

    # Explanations for missing keywords
    for keyword in gap_analysis_result.get('missing_keywords', []):
        explanation = (
            f"The job description mentions '{keyword}', which is not prominently featured in your resume. "
            "If you have this skill, consider adding it to your skills or experience sections."
        )
        explanations['missing'].append(explanation)

    # Explanations for strong matches
    for keyword in gap_analysis_result.get('strong_matches', []):
        explanation = (
            f"Your resume shows experience with '{keyword}', which is a great match for this role."
        )
        explanations['matches'].append(explanation)

    return explanations
