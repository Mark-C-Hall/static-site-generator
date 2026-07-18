import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://boot.dev"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev">Click me</a>',
        )

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Click me",
            {"href": "https://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" target="_blank">Click me</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_empty_value_renders(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_img_void_tag(self):
        node = LeafNode("img", "", {"src": "https://example.com", "alt": "a cat"})
        self.assertEqual(
            node.to_html(),
            '<img src="https://example.com" alt="a cat">',
        )

    def test_leaf_children_is_none(self):
        node = LeafNode("p", "Hello")
        self.assertIsNone(node.children)

    def test_leaf_props_default_none(self):
        node = LeafNode("p", "Hello")
        self.assertIsNone(node.props)


if __name__ == "__main__":
    unittest.main()
