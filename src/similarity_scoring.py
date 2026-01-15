
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, job_description_text):
    """
    Calculates the cosine similarity between a resume and a job description.

    Args:
        resume_text (str): The preprocessed resume text.
        job_description_text (str): The preprocessed job description text.

    Returns:
        float: A similarity score between 0 and 100.
    """
    documents = [resume_text, job_description_text]

    # Create a TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Calculate the cosine similarity between the two vectors (documents)
    # The result is a matrix, and the value at [0, 1] is the similarity between the first and second document.
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # The similarity is in the range [0, 1]. We scale it to [0, 100].
    similarity_score = similarity_matrix[0][0] * 100

    return similarity_score
