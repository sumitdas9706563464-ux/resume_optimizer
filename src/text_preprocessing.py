
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def _ensure_nltk_data():
    """Ensures necessary NLTK data is downloaded."""
    required = [
        ('corpora/stopwords', 'stopwords'),
        ('tokenizers/punkt', 'punkt'),
        ('corpora/wordnet', 'wordnet'),
        ('tokenizers/punkt_tab', 'punkt_tab')
    ]
    for resource, package in required:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(package)

def preprocess_text(text):
    """
    Cleans and preprocesses text for NLP analysis.

    Args:
        text (str): The input text.

    Returns:
        str: The preprocessed text.
    """
    _ensure_nltk_data()

    # 1. Lowercasing
    text = text.lower()

    # 2. Remove punctuation and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # 3. Tokenization
    tokens = word_tokenize(text)

    # 4. Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # 5. Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return " ".join(lemmatized_tokens)
