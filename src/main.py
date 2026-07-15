from textnode import *
from parentnode import *
from leafnode import *


def main():
    plain_text_node = TextNode("Hello!", TextType.PLAIN)
    bold_text_node = TextNode("**HEY!!!**", TextType.BOLD)
    link_text_node = TextNode(
        "[Repo](https://github.com/Mark-C-Hall/static-site-generator)",
        TextType.LINK,
        "https://github.com/Mark-C-Hall/static-site-generator",
    )
    image_text_node = TextNode(
        "![A black kitten sleeping on a white blanket](https://example.com)",
        TextType.IMAGE,
        "https://example.com",
    )

    parent = ParentNode(
        "main",
        [
            LeafNode("b", "Bold text"),
            ParentNode(
                "p",
                [
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                    LeafNode(None, "Normal text"),
                ],
            ),
        ],
    )

    print(plain_text_node)
    print(bold_text_node)
    print(link_text_node)

    print(plain_text_node.to_html_node().to_html())
    print(bold_text_node.to_html_node().to_html())
    print(link_text_node.to_html_node().to_html())
    print(image_text_node.to_html_node().to_html())

    print(parent.to_html())


if __name__ == "__main__":
    main()
