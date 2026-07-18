import re
from textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 != 1:
            raise Exception(f"node does not contain closing delimter: {delimiter}")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(part, TextType.PLAIN))
            else:
                result.append(TextNode(part, text_type))

    return result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            result.append(node)
            continue
        for alt, url in images:
            before, node.text = node.text.split(f"![{alt}]({url})", 1)
            if before:
                result.append(TextNode(before, TextType.PLAIN))
            result.append(TextNode(alt, TextType.IMAGE, url))
        if node.text:
            result.append(TextNode(node.text, TextType.PLAIN))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    # Assumes split_nodes_image has already run on old_nodes. Image markdown
    # like ![alt](url) contains [alt](url) as a literal substring, so if raw
    # image syntax is still present here it can be mistaken for a link.
    result: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            result.append(node)
            continue
        for alt, url in links:
            before, node.text = node.text.split(f"[{alt}]({url})", 1)
            if before:
                result.append(TextNode(before, TextType.PLAIN))
            result.append(TextNode(alt, TextType.LINK, url))
        if node.text:
            result.append(TextNode(node.text, TextType.PLAIN))

    return result


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
