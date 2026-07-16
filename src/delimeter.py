import re
from textnode import *


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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
