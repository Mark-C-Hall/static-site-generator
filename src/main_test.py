import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_leading_and_trailing_whitespace(self):
        self.assertEqual(extract_title("#    Hello World   "), "Hello World")

    def test_title_among_other_lines(self):
        md = """
This is a paragraph

# Title Here

Another paragraph
"""
        self.assertEqual(extract_title(md), "Title Here")

    def test_ignores_h2_and_other_headers(self):
        md = """
## Not the title

# The Real Title

### Also not the title
"""
        self.assertEqual(extract_title(md), "The Real Title")

    def test_returns_first_h1_when_multiple(self):
        md = """
# First Title

# Second Title
"""
        self.assertEqual(extract_title(md), "First Title")

    def test_raises_when_no_h1(self):
        md = """
This is just a paragraph.

## This is an h2, not an h1
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_raises_on_empty_string(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_does_not_match_hash_without_space(self):
        md = "#NoSpaceHeader\n# Actual Title"
        self.assertEqual(extract_title(md), "Actual Title")


if __name__ == "__main__":
    unittest.main()