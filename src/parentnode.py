from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None
    ):
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("tag not included in parent node")
        if not self.children:
            raise ValueError("children not included in parent node")

        result: list[str] = []
        result.append(f"<{self.tag}{super().props_to_html()}>")
        for child in self.children:
            result.append(child.to_html())
        result.append(f"</{self.tag}>")

        return "".join(result)
