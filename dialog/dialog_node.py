from main.player_log import get_player_log
from main.messenger import get_messenger
player_log = get_player_log()
messenger = get_messenger()

class DialogNode:
    def __init__(self, name: str, text: str, children):
        # Title of the dialogue box
        self.name: str = name

        # Text to display
        self.text: str = text

        # List of nodes and the choices that select them
        self.children: list[tuple[str, DialogNode]] = children

        # Condition requirement to show this child node
        self.condition = None

        # Condition that does not show this child node
        self.unless = None

        # Function called when this option is selected
        self.function_name = None

        # For root nodes, what option the player chooses from the area screen
        self.area_option = None

    def set_condition(self, condition: str):
        self.condition = condition

    def set_unless(self, unless: str):
        self.unless = unless

    def set_function_name(self, function_name: str):
        self.function_name = function_name

    def set_area_option(self, area_option: str):
        self.area_option = area_option

    def condition_met(self):
        if self.unless:
            if player_log[self.unless]:
                return False
        if self.condition:
            if self.condition in player_log:
                return player_log[self.condition]
            messenger.warning(f"Can't find {self.condition} in player_log. Setting as True.")
        return True

    def call_function(self, player):
        # This causes a circular import
        # pylint: disable=import-outside-toplevel
        from dialog import dialog_functions
        if self.function_name:
            f = getattr(dialog_functions, self.function_name)
            f(player)
