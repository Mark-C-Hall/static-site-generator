import unittest
from delimeter import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestDelimeter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters_same_line(self):
        node = TextNode("This has `code one` and `code two` in it", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("code one", TextType.CODE),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code two", TextType.CODE),
            TextNode(" in it", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter_present(self):
        node = TextNode("This is plain text with no delimiters", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_plain_node_passed_through_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_mixed_plain_and_non_plain_nodes(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        plain_node = TextNode("some `code` here", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([bold_node, plain_node], "`", TextType.CODE)
        expected = [
            TextNode("already bold", TextType.BOLD),
            TextNode("some ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code` at both `ends`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at both ", TextType.PLAIN),
            TextNode("ends", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_adjacent_delimiters_no_gap(self):
        node = TextNode("`code1``code2`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_bold_same_line(self):
        node = TextNode("This has **bold one** and **bold two** in it", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("bold one", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("bold two", TextType.BOLD),
            TextNode(" in it", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_italic_same_line(self):
        node = TextNode("This has *italic one* and *italic two* in it", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("italic one", TextType.ITALIC),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic two", TextType.ITALIC),
            TextNode(" in it", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is ![one](https://example.com/1.png) and ![two](https://example.com/2.png)"
        )
        self.assertListEqual(
            [
                ("one", "https://example.com/1.png"),
                ("two", "https://example.com/2.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_none_present(self):
        matches = extract_markdown_images("This is just plain text")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_ignores_links(self):
        matches = extract_markdown_images(
            "This is a [link](https://example.com), not an image"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com) and another [link two](https://example.com/2)"
        )
        self.assertListEqual(
            [
                ("link", "https://example.com"),
                ("link two", "https://example.com/2"),
            ],
            matches,
        )

    def test_extract_markdown_links_none_present(self):
        matches = extract_markdown_links("This is just plain text")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "This is an ![image](https://example.com/img.png), not a link"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_and_images_together(self):
        text = "An ![image](https://example.com/img.png) next to a [link](https://example.com)"
        self.assertListEqual(
            [("link", "https://example.com")], extract_markdown_links(text)
        )
        self.assertListEqual(
            [("image", "https://example.com/img.png")], extract_markdown_images(text)
        )
