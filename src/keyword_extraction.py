
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def _ensure_nltk_tagger():
    """Ensures necessary NLTK tagger data is downloaded."""
    required = [
        ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
        ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng')
    ]
    for resource, package in required:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(package)

def extract_keywords(text, top_n=50):
    """
    Extracts and categorizes keywords from a given text.
    """
    # Use TF-IDF to get important terms (including n-grams for multi-word skills)
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform([text])
    feature_names = tfidf_vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray().flatten()

    # Get more keywords than top_n to allow for filtering and categorization
    top_indices = scores.argsort()[-(top_n*2):][::-1]
    raw_keywords = [feature_names[i] for i in top_indices]

    return raw_keywords

def categorize_keywords(keywords):
    """
    Categorizes a list of keywords into Technical, Soft Skills, Tools, and Action Verbs.
    """
    _ensure_nltk_tagger()

    categories = {
        "Technical Skills": [],
        "Soft Skills": [],
        "Tools & Technologies": [],
        "Action Verbs": []
    }

    # Predefined lists for better accuracy
    soft_skills_list = {
        'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
        'adaptability', 'time management', 'collaboration', 'creativity', 'work ethic',
        'attention to detail', 'interpersonal', 'emotional intelligence', 'negotiation',
        'conflict resolution', 'presentation', 'public speaking', 'mentoring', 'coaching'
    }

    action_verbs_list = {
        'managed', 'led', 'developed', 'created', 'implemented', 'achieved', 'increased',
        'reduced', 'spearheaded', 'orchestrated', 'designed', 'optimized', 'facilitated',
        'collaborated', 'coordinated', 'mentored', 'trained', 'presented', 'analyzed',
        'automated', 'built', 'deployed', 'engineered', 'formulated', 'generated',
        'improved', 'initiated', 'launched', 'produced', 'resolved', 'streamlined'
    }

    tools_technologies_list = {
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'aws', 'azure', 'gcp',
        'docker', 'kubernetes', 'git', 'react', 'angular', 'vue', 'node', 'express',
        'django', 'flask', 'tensorflow', 'pytorch', 'sklearn', 'pandas', 'numpy',
        'excel', 'tableau', 'powerbi', 'jira', 'slack', 'confluence', 'linux', 'unix',
        'mongodb', 'postgresql', 'mysql', 'redis', 'kafka', 'jenkins', 'terraform'
    }

    # POS tagging for better categorization
    tagged = nltk.pos_tag(keywords)

    for word, tag in tagged:
        word_lower = word.lower()

        if word_lower in action_verbs_list or tag.startswith('VB'):
            categories["Action Verbs"].append(word)
        elif word_lower in soft_skills_list:
            categories["Soft Skills"].append(word)
        elif word_lower in tools_technologies_list:
            categories["Tools & Technologies"].append(word)
        elif tag.startswith('NN'):
            # Further check if it might be a tool or tech
            if any(tool in word_lower for tool in tools_technologies_list):
                 categories["Tools & Technologies"].append(word)
            else:
                categories["Technical Skills"].append(word)
        else:
            categories["Technical Skills"].append(word)

    # Limit results and remove duplicates within categories
    for cat in categories:
        categories[cat] = sorted(list(set(categories[cat])))[:15]

    return categories
