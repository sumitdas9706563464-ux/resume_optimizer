
import unittest
import os
import sys

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text_extraction import extract_text_from_pdf
from tests.create_dummy_pdf import create_dummy_pdf

class TestTextExtraction(unittest.TestCase):

    def setUp(self):
        """Set up a dummy PDF for testing."""
        self.pdf_path = "tests/dummy_resume.pdf"
        self.expected_text = "This is a dummy resume."
        create_dummy_pdf(self.pdf_path, self.expected_text)

    def test_extract_text_from_pdf(self):
        """Test that text is correctly extracted from a PDF."""
        extracted_text = extract_text_from_pdf(self.pdf_path)
        # We check for containment because the extraction might add some noise.
        self.assertIn(self.expected_text, extracted_text)

    def tearDown(self):
        """Remove the dummy PDF after the test."""
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)

if __name__ == '__main__':
    unittest.main()
