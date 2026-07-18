from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType
from inline import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        lines = block.split("\n")
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
    if block.startswith("- "):
        lines = block.split("\n")
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        lines = block.split("\n")
        if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    parts = markdown.split("\n\n")
    stripped = [part.strip() for part in parts]
    return [b for b in stripped if b]


def markdown_to_html_node(markdown: str) -> HTMLNode:
    children: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                children.append(create_paragraph_html_node(block))
            case BlockType.HEADING:
                children.append(create_heading_html_node(block))
            case BlockType.CODE:
                children.append(create_code_html_node(block))
            case BlockType.QUOTE:
                children.append(create_quote_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(create_unordered_list_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(create_ordered_list_html_node(block))

    return ParentNode("div", children)


def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    return [node.to_html_node() for node in nodes]


def create_paragraph_html_node(block: str) -> HTMLNode:
    children_nodes = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children_nodes)


def create_heading_html_node(block: str) -> HTMLNode:
    heading_classifier, title = block.split(" ", 1)
    count = heading_classifier.count("#")
    heading = f"h{count}"
    children_nodes = text_to_children(title)
    return ParentNode(heading, children_nodes)


def create_code_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    code = "\n".join(lines[1:-1]) + "\n"
    text_node = TextNode(code, TextType.CODE)
    leaf_node = text_node.to_html_node()
    return ParentNode("pre", [leaf_node])


def strip_quote_marker(line: str) -> str:
    text = line[1:]
    return text[1:] if text.startswith(" ") else text


def create_quote_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    stripped_lines = [strip_quote_marker(line) for line in lines]
    content = " ".join(stripped_lines)
    children_nodes = text_to_children(content)
    return ParentNode("blockquote", children_nodes)


def create_unordered_list_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    stripped_lines = [line[2:] for line in lines]
    list_items: list[HTMLNode] = []
    for line in stripped_lines:
        children_nodes = text_to_children(line)
        list_items.append(ParentNode("li", children_nodes))
    return ParentNode("ul", list_items)


def create_ordered_list_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    list_items: list[HTMLNode] = []
    for i, line in enumerate(lines, start=1):
        text = line[len(f"{i}. ") :]
        children_nodes = text_to_children(text)
        list_items.append(ParentNode("li", children_nodes))
    return ParentNode("ol", list_items)
