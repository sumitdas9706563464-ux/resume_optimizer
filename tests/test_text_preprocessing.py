
import unittest
import os
import sys

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text_preprocessing import preprocess_text

class TestTextPreprocessing(unittest.TestCase):

    def test_preprocess_text(self):
        """Test the full text preprocessing pipeline."""
        input_text = "This is a Test sentence with punctuation! And numbers 123."
        expected_output = "test sentence punctuation number"
        self.assertEqual(preprocess_text(input_text), expected_output)

    def test_preprocess_text_with_stopwords(self):
        """Test that stopwords are correctly removed."""
        input_text = "a the is an"
        expected_output = ""
        self.assertEqual(preprocess_text(input_text), expected_output)

    def test_preprocess_text_with_lemmatization(self):
        """Test that words are correctly lemmatized."""
        input_text = "running runs ran"
        expected_output = "running run ran"
        self.assertEqual(preprocess_text(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()
