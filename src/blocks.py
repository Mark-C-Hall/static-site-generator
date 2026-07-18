def markdown_to_blocks(markdown: str) -> list[str]:
    parts = markdown.split("\n\n")
    stripped = [part.strip() for part in parts]
    return [b for b in stripped if b]
