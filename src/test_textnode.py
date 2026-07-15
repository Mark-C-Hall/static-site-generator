import unittest
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ne_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_eq_with_url(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_ne_url(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_ne_url_none(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_equal_to_other_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a text node")

    def test_repr(self):
        node = TextNode("Hello", TextType.LINK, "https://boot.dev")
        self.assertEqual(repr(node), "TextNode(Hello, TextType.LINK, https://boot.dev)")

    def test_to_html_node_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = node.to_html_node()
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_to_html_node_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_to_html_node_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_to_html_node_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")
        self.assertEqual(html_node.to_html(), "<code>code text</code>")

    def test_to_html_node_link(self):
        node = TextNode(
            "[Boot.dev](https://boot.dev)", TextType.LINK, "https://boot.dev"
        )
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "[Boot.dev](https://boot.dev)")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://boot.dev">[Boot.dev](https://boot.dev)</a>',
        )

    def test_to_html_node_link_no_url_raises(self):
        node = TextNode("[Boot.dev](https://boot.dev)", TextType.LINK)
        with self.assertRaises(AssertionError):
            node.to_html_node()

    def test_to_html_node_image(self):
        node = TextNode(
            "![alt text](https://example.com/image.png)",
            TextType.IMAGE,
            "https://example.com/image.png",
        )
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "alt text"},
        )

    def test_to_html_node_image_renders(self):
        node = TextNode(
            "![alt text](https://example.com/image.png)",
            TextType.IMAGE,
            "https://example.com/image.png",
        )
        html_node = node.to_html_node()
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/image.png" alt="alt text">',
        )

    def test_to_html_node_image_no_url_raises(self):
        node = TextNode("![alt text](https://example.com/image.png)", TextType.IMAGE)
        with self.assertRaises(AssertionError):
            node.to_html_node()


if __name__ == "__main__":
    unittest.main()
