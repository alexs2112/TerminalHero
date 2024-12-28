class DialogNode:
    def __init__(self, name: str, text: str, children):
        # Title of the dialogue box
        self.name: str = name

        # Text to display
        self.text: str = text

        # List of nodes and the choices that select them
        self.children: list[tuple[str, DialogNode]] = children
