from htmlnode import HTMLNode


VOID_TAGS = {"img", "br", "hr", "input", "meta", "link"}


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError
        if not self.tag:
            return self.value
        if self.tag in VOID_TAGS:
            return f"<{self.tag}{super().props_to_html()}>"
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
