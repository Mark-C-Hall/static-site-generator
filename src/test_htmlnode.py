import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://boot.dev" target="_blank"',
        )

    def test_props_to_html_single(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Hello", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_values(self):
        node = HTMLNode("p", "Hello", None, None)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_children(self):
        child = HTMLNode("span", "child", None, None)
        node = HTMLNode("div", None, [child], None)
        self.assertEqual(node.children, [child])

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "greeting"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, Hello, None, {'class': 'greeting'})",
        )


if __name__ == "__main__":
    unittest.main()
