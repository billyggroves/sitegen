import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        text = """
                    # Here is my Title

                    1. item one
                    2. item two
               """
        title = extract_title(text)
        self.assertEqual(title, "# Here is my Title")

if __name__ == "__main__":
    unittest.main()