import unittest
from blocks import (
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_block_type,
    BlockType,
)


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
        self.assertEqual(blocks, ["- item one\n  - nested item", "Second block"])


class TestBlockToBlockType(unittest.TestCase):
    # --- heading ---

    def test_heading_level_1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_level_6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_no_space_after_hashes(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    # --- code ---

    def test_code_block_single_line_of_content(self):
        self.assertEqual(block_to_block_type("```\ncode line\n```"), BlockType.CODE)

    def test_code_block_multiline_content(self):
        self.assertEqual(block_to_block_type("```\nline1\nline2\n```"), BlockType.CODE)

    def test_code_block_missing_newline_after_opening_fence(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_code_block_missing_closing_fence(self):
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)

    # --- quote ---

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> quote text"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type("> line one\n> line two"), BlockType.QUOTE)

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
            block_to_block_type("This is a paragraph\nwith multiple lines\nof text"),
            BlockType.PARAGRAPH,
        )


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    # --- heading ---

    def test_heading_only(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_heading_all_levels(self):
        for level in range(1, 7):
            md = f"{'#' * level} Heading text"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html, f"<div><h{level}>Heading text</h{level}></div>"
            )

    def test_multiple_headings_in_one_document(self):
        md = "# First heading\n\n## Second heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>First heading</h1><h2>Second heading</h2></div>",
        )

    def test_heading_with_inline_markdown(self):
        md = "# This is a **bolded** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h1>This is a <b>bolded</b> heading</h1></div>"
        )

    # --- unordered list ---

    def test_unordered_list_single_item(self):
        md = "- item one"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>item one</li></ul></div>")

    def test_unordered_list_multiple_items(self):
        md = "- item one\n- item two\n- item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        md = "- **bold** item\n- _italic_ item\n- `code` item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li>"
            "<li><code>code</code> item</li></ul></div>",
        )

    def test_unordered_list_item_text_starting_with_hyphen(self):
        # Regression guard: stripping the "- " marker must remove exactly
        # that literal prefix, not repeatedly eat any leading '-'/space
        # characters (which would also consume a hyphen that's part of the
        # item's actual text, e.g. a negative number).
        md = "- -1 is negative"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>-1 is negative</li></ul></div>")

    def test_unordered_list_followed_by_paragraph(self):
        md = "- item one\n- item two\n\nA paragraph after the list"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item two</li></ul>"
            "<p>A paragraph after the list</p></div>",
        )

    # --- ordered list ---

    def test_ordered_list_single_item(self):
        md = "1. item one"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>item one</li></ol></div>")

    def test_ordered_list_multiple_items(self):
        md = "1. item one\n2. item two\n3. item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item one</li><li>item two</li><li>item three</li></ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = "1. **first**\n2. _second_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>first</b></li><li><i>second</i></li></ol></div>",
        )

    def test_ordered_list_double_digit_items(self):
        # Guards against slicing a fixed number of characters off each line
        # (e.g. line[3:]) to drop the "N. " prefix, which breaks once the
        # item number reaches two digits.
        items = "\n".join(f"{i}. item {i}" for i in range(1, 11))
        node = markdown_to_html_node(items)
        html = node.to_html()
        expected_items = "".join(f"<li>item {i}</li>" for i in range(1, 11))
        self.assertEqual(html, f"<div><ol>{expected_items}</ol></div>")

    def test_ordered_list_triple_digit_items(self):
        # Regression guard: the "N. " marker must be stripped based on the
        # actual item number's width, not a fixed-length slice, which would
        # break once numbers reach 3+ digits.
        items = "\n".join(f"{i}. item {i}" for i in range(1, 101))
        node = markdown_to_html_node(items)
        html = node.to_html()
        expected_items = "".join(f"<li>item {i}</li>" for i in range(1, 101))
        self.assertEqual(html, f"<div><ol>{expected_items}</ol></div>")

    def test_ordered_list_followed_by_paragraph(self):
        md = "1. item one\n2. item two\n\nA paragraph after the list"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item one</li><li>item two</li></ol>"
            "<p>A paragraph after the list</p></div>",
        )

    # --- quote ---

    def test_quote_single_line(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_quote_multiline(self):
        md = "> Line one\n> Line two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>Line one Line two</blockquote></div>"
        )

    def test_quote_no_space_after_gt(self):
        md = ">no space"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>no space</blockquote></div>")

    def test_quote_with_inline_markdown(self):
        md = "> This is **bold** and _italic_ and `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bold</b> and <i>italic</i> and "
            "<code>code</code></blockquote></div>",
        )

    def test_quote_multiline_with_inline_markdown(self):
        md = "> Line one **bold**\n> Line two _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Line one <b>bold</b> Line two "
            "<i>italic</i></blockquote></div>",
        )

    def test_quote_content_starting_with_gt(self):
        # Regression guard: only the single ">" marker (and at most one
        # following space) should be stripped, not every leading '>' —
        # otherwise quote content that itself starts with '>' gets mangled.
        md = ">>test"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>>test</blockquote></div>")

    def test_quote_followed_by_paragraph(self):
        md = "> A quote\n\nA paragraph after the quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>A quote</blockquote>"
            "<p>A paragraph after the quote</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
