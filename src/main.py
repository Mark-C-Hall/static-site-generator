from textnode import *


def main():
    plain_text_node = TextNode("Hello!", TextType.PLAIN)
    bold_text_node = TextNode("**HEY!!!**", TextType.BOLD)
    link_text_node = TextNode(
        "[Repo](https://github.com/Mark-C-Hall/static-site-generator)",
        TextType.LINK,
        "https://github.com/Mark-C-Hall/static-site-generator",
    )

    print(plain_text_node)
    print(bold_text_node)
    print(link_text_node)


if __name__ == "__main__":
    main()
