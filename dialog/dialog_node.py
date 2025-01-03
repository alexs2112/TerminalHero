from dialog import dialog_functions
from main.player_log import get_player_log
from main.messenger import get_messenger
player_log = get_player_log()
messenger = get_messenger()

class DialogNode:
    def __init__(self, name: str, text: str, children, condition: str = None, function_name: str = None):
        # Title of the dialogue box
        self.name: str = name

        # Text to display
        self.text: str = text

        # List of nodes and the choices that select them
        self.children: list[tuple[str, DialogNode]] = children

        # Condition requirement to show this child node
        self.condition: str = condition

        # Function called when this option is selected
        self.function_name = function_name

    def condition_met(self):
        if self.condition:
            if self.condition in player_log:
                return player_log[self.condition]
            messenger.warning(f"Can't find {self.condition} in player_log. Setting as True.")
        return True

    def call_function(self):
        if self.function_name:
            f = getattr(dialog_functions, self.function_name)
            f()
