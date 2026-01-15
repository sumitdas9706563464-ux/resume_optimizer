
import unittest
import streamlit

class TestEnvironment(unittest.TestCase):

    def test_streamlit_import(self):
        """Tests that Streamlit can be imported."""
        self.assertIsNotNone(streamlit)

if __name__ == '__main__':
    unittest.main()
