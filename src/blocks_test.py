import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType


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


class TestBlockToBlockType(unittest.TestCase):
    # --- heading ---

    def test_heading_level_1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_level_6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_no_space_after_hashes(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        self.assertEqual(
            block_to_block_type("####### Heading"), BlockType.PARAGRAPH
        )

    # --- code ---

    def test_code_block_single_line_of_content(self):
        self.assertEqual(
            block_to_block_type("```\ncode line\n```"), BlockType.CODE
        )

    def test_code_block_multiline_content(self):
        self.assertEqual(
            block_to_block_type("```\nline1\nline2\n```"), BlockType.CODE
        )

    def test_code_block_missing_newline_after_opening_fence(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_code_block_missing_closing_fence(self):
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)

    # --- quote ---

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> quote text"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(
            block_to_block_type("> line one\n> line two"), BlockType.QUOTE
        )

    def test_quote_no_space_after_gt(self):
        self.assertEqual(block_to_block_type(">no space"), BlockType.QUOTE)

    def test_quote_mixed_with_non_quote_line(self):
        self.assertEqual(
            block_to_block_type("> line one\nline two"), BlockType.PARAGRAPH
        )

    # --- unordered list ---

    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- item one"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        self.assertEqual(
            block_to_block_type("- item one\n- item two\n- item three"),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_unordered_list_mixed_with_non_list_line(self):
        self.assertEqual(
            block_to_block_type("- item one\nitem two"), BlockType.PARAGRAPH
        )

    # --- ordered list ---

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. item one"), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        self.assertEqual(
            block_to_block_type("1. item one\n2. item two\n3. item three"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_must_start_at_one(self):
        self.assertEqual(
            block_to_block_type("2. item one\n3. item two"), BlockType.PARAGRAPH
        )

    def test_ordered_list_must_increment_by_one(self):
        self.assertEqual(
            block_to_block_type("1. item one\n3. item two"), BlockType.PARAGRAPH
        )

    def test_ordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("1.item"), BlockType.PARAGRAPH)

    # --- paragraph ---

    def test_plain_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph of text."),
            BlockType.PARAGRAPH,
        )

    def test_paragraph_multiline(self):
        self.assertEqual(
            block_to_block_type(
                "This is a paragraph\nwith multiple lines\nof text"
            ),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
