import unittest
from inline import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInline(unittest.TestCase):
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_without_lead(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single_no_surrounding_text(self):
        node = TextNode("![only image](https://example.com/only.png)", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("only image", TextType.IMAGE, "https://example.com/only.png")],
            new_nodes,
        )

    def test_split_images_trailing_text_after_last_image(self):
        node = TextNode(
            "An ![image](https://example.com/img.png) then trailing text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("An ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" then trailing text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_images_no_images_passthrough(self):
        node = TextNode("Just plain text, no images here", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_non_plain_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_mixed_nodes(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        image_node = TextNode(
            "here is ![a cat](https://example.com/cat.png)", TextType.PLAIN
        )
        new_nodes = split_nodes_image([bold_node, image_node])
        self.assertListEqual(
            [
                bold_node,
                TextNode("here is ", TextType.PLAIN),
                TextNode("a cat", TextType.IMAGE, "https://example.com/cat.png"),
            ],
            new_nodes,
        )

    def test_split_images_adjacent_no_gap(self):
        node = TextNode(
            "![one](https://example.com/1.png)![two](https://example.com/2.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
            ],
            new_nodes,
        )

    def test_split_images_duplicate_identical_images(self):
        node = TextNode(
            "![logo](https://example.com/logo.png) and again ![logo](https://example.com/logo.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
                TextNode(" and again ", TextType.PLAIN),
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_list(self):
        self.assertListEqual([], split_nodes_image([]))

    # --- split_nodes_link (TDD: split_nodes_link is currently a stub) ---

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://www.boot.dev/courses)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev/courses"
                ),
            ],
            new_nodes,
        )

    def test_split_links_without_lead(self):
        node = TextNode(
            "[link](https://boot.dev) and another [second link](https://www.boot.dev/courses)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev/courses"
                ),
            ],
            new_nodes,
        )

    def test_split_links_single_no_surrounding_text(self):
        node = TextNode("[only link](https://example.com)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("only link", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_links_trailing_text_after_last_link(self):
        node = TextNode(
            "Check out [this link](https://example.com) then trailing text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.PLAIN),
                TextNode("this link", TextType.LINK, "https://example.com"),
                TextNode(" then trailing text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_links_no_links_passthrough(self):
        node = TextNode("Just plain text, no links here", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_non_plain_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_mixed_nodes(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        link_node = TextNode("here is [a link](https://example.com)", TextType.PLAIN)
        new_nodes = split_nodes_link([bold_node, link_node])
        self.assertListEqual(
            [
                bold_node,
                TextNode("here is ", TextType.PLAIN),
                TextNode("a link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_adjacent_no_gap(self):
        node = TextNode(
            "[one](https://example.com/1)[two](https://example.com/2)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "https://example.com/1"),
                TextNode("two", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )

    def test_split_links_duplicate_identical_links(self):
        node = TextNode(
            "[docs](https://example.com/docs) and again [docs](https://example.com/docs)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("docs", TextType.LINK, "https://example.com/docs"),
                TextNode(" and again ", TextType.PLAIN),
                TextNode("docs", TextType.LINK, "https://example.com/docs"),
            ],
            new_nodes,
        )

    def test_split_links_empty_list(self):
        self.assertListEqual([], split_nodes_link([]))

    def test_split_links_ignores_images_with_shared_text_and_url(self):
        # split_nodes_link assumes split_nodes_image already ran (see the
        # comment on split_nodes_link) - an image's raw markdown contains the
        # link's token as a literal substring, so this only resolves
        # correctly once the image has already been stripped out first.
        node = TextNode(
            "![shared](https://example.com/shared) and "
            "[shared](https://example.com/shared)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("shared", TextType.IMAGE, "https://example.com/shared"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("shared", TextType.LINK, "https://example.com/shared"),
            ],
            new_nodes,
        )

    # --- text_to_textnodes (TDD: text_to_textnodes is currently a stub) ---

    def test_text_to_textnodes_full_example(self):
        text = (
            "This is **text** with an *italic* word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_plain_only(self):
        new_nodes = text_to_textnodes("Just plain text, nothing special")
        self.assertListEqual(
            [TextNode("Just plain text, nothing special", TextType.PLAIN)],
            new_nodes,
        )

    def test_text_to_textnodes_bold_only(self):
        new_nodes = text_to_textnodes("This has **bold** text")
        self.assertListEqual(
            [
                TextNode("This has ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_italic_only(self):
        new_nodes = text_to_textnodes("This has *italic* text")
        self.assertListEqual(
            [
                TextNode("This has ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_italic_underscore(self):
        new_nodes = text_to_textnodes("This has _italic_ text")
        self.assertListEqual(
            [
                TextNode("This has ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_italic_both_styles_together(self):
        new_nodes = text_to_textnodes("This has _italic_ and *also italic* text")
        self.assertListEqual(
            [
                TextNode("This has ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.PLAIN),
                TextNode("also italic", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_code_only(self):
        new_nodes = text_to_textnodes("This has `code` text")
        self.assertListEqual(
            [
                TextNode("This has ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_image_only(self):
        new_nodes = text_to_textnodes(
            "An image ![alt text](https://example.com/img.png) here"
        )
        self.assertListEqual(
            [
                TextNode("An image ", TextType.PLAIN),
                TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" here", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_link_only(self):
        new_nodes = text_to_textnodes("A link [to boot.dev](https://boot.dev) here")
        self.assertListEqual(
            [
                TextNode("A link ", TextType.PLAIN),
                TextNode("to boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" here", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_bold_and_italic_together(self):
        # Regression guard for ordering: bold ("**") must be split before
        # italic ("*"), otherwise the italic pass would shred "**bold**"
        # into pieces on its lone "*" characters before bold ever sees it.
        new_nodes = text_to_textnodes("**bold** and *italic* together")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" together", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_image_and_link_together(self):
        new_nodes = text_to_textnodes(
            "![alt](https://example.com/img.png) and [text](https://example.com)"
        )
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("text", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_multiple_bold(self):
        new_nodes = text_to_textnodes("**one** and **two**")
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("two", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_empty_string(self):
        self.assertListEqual([], text_to_textnodes(""))
