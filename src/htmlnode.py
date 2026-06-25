class HTMLNode:
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        children: list["HTMLNode"] | None,
        props: dict[str, str] | None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        result: list[str] = []
        for key, value in self.props.items():
            result.append(f' {key}="{value}"')
        return "".join(result)
