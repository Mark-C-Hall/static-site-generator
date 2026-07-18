import unittest
from blocks import markdown_to_blocks


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "Just a single paragraph with no blank lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with no blank lines"])

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_whitespace_only_string(self):
        self.assertEqual(markdown_to_blocks("   \n\n   \n"), [])

    def test_strips_leading_and_trailing_whitespace_per_block(self):
        md = "   First block   \n\n   Second block   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_excessive_blank_lines_between_blocks(self):
        md = "First block\n\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_leading_and_trailing_blank_lines_in_document(self):
        md = "\n\n\nFirst block\n\nSecond block\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_heading_block(self):
        md = "# This is a heading\n\nThis is a paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# This is a heading", "This is a paragraph"])

    def test_three_distinct_blocks(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n"
                "- This is a list item\n"
                "- This is another list item",
            ],
        )

    def test_block_with_internal_leading_whitespace_on_lines_is_preserved(self):
        # .strip() only trims the outer edges of a block, not indentation
        # that's meaningful within the block itself (e.g. nested list items).
        md = "- item one\n  - nested item\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["- item one\n  - nested item", "Second block"]
        )


if __name__ == "__main__":
    unittest.main()
