import unittest

from generatepage import extract_title, generate_page

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title"
        result = "Title"

        self.assertEqual(extract_title(markdown), result)

    def test_extract_title_error(self):
        markdown = "Some text"
        result = "Title"

        self.assertRaises(Exception, extract_title, markdown)

if __name__ == "__main__":
    unittest.main()

