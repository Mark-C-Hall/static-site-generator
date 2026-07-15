from enum import Enum
from leafnode import *


class TextType(Enum):
    PLAIN = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.PLAIN:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                assert self.url is not None
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                assert self.url is not None
                start = self.text.find("[") + 1
                end = self.text.find("]")
                return LeafNode(
                    "img", "", {"src": self.url, "alt": self.text[start:end]}
                )
