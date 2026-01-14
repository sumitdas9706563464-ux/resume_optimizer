
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, top_n=20):
    """
    Extracts the top N keywords from a given text using TF-IDF.

    Args:
        text (str): The preprocessed text.
        top_n (int): The number of top keywords to return.

    Returns:
        list: A list of the top N keywords.
    """
    # Create a TF-IDF Vectorizer
    # We use a corpus of one document, so we only care about term frequency.
    # The IDF part is not really used here, but this is a convenient way to get scored words.
    # We will use n-grams to capture multi-word skills
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english')

    # We expect a list of documents, so we pass the text in a list
    tfidf_matrix = tfidf_vectorizer.fit_transform([text])

    # Get the feature names (the keywords)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Get the tf-idf scores for the single document
    scores = tfidf_matrix.toarray().flatten()

    # Get the indices of the top N scores
    top_indices = scores.argsort()[-top_n:][::-1]

    # Get the top N keywords
    top_keywords = [feature_names[i] for i in top_indices]

    return top_keywords
