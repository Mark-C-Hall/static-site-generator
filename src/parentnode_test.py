import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("a", "Click me", {"href": "https://boot.dev"})
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><a href="https://boot.dev">Click me</a></div>',
        )

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "child")])  # type: ignore
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)  # type: ignore
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_multiple_parent_children(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode(None, "first")]),
                ParentNode("p", [LeafNode(None, "second")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>first</p><p>second</p></div>",
        )

    def test_children_default_props_none(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsNone(node.props)

    def test_value_is_none(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsNone(node.value)


if __name__ == "__main__":
    unittest.main()
