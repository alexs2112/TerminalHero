from main.player_log import get_player_log
from main.messenger import get_messenger
player_log = get_player_log()
messenger = get_messenger()

class DialogNode:
    def __init__(self, node_id: str, name: str, text: str, children):
        self.type = "Dialog"

        self.id = node_id

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

        # Only allow this dialog node to be selected once
        self.only_once = False

        # Function called when this option is selected
        self.function_name = None

        # For root nodes, what option the player chooses from the area screen
        self.area_option = None

        # Stat requirement to show this node, else just greyed out requirement
        # A dict of { stat: value }
        self.stat_requirement = None

    def set_condition(self, condition: str):
        self.condition = condition

    def set_unless(self, unless: str):
        self.unless = unless

    def set_function_name(self, function_name: str):
        self.function_name = function_name

    def set_area_option(self, area_option: str):
        self.area_option = area_option

    def set_only_once(self, only_once: bool):
        self.only_once = only_once

    def set_stat_requirement(self, stat_requirement):
        self.stat_requirement = stat_requirement

    def meet_stat_requirement(self, player):
        if self.stat_requirement:
            for stat, value in self.stat_requirement.items():
                if player.party_stat(stat) < value:
                    return False
        return True

    def stat_requirement_string(self):
        s = '[ requires'
        for stat, value in self.stat_requirement.items():
            s += f" {stat}={value} "
        s += ']'
        return s

    def condition_met(self):
        if self.unless:
            if player_log[self.unless]:
                return False
        if self.only_once:
            if self.id in player_log:
                return not player_log[self.id]
        if self.condition:
            if self.condition in player_log:
                return player_log[self.condition]
            return False
        return True

    def call_function(self, player):
        # This causes a circular import
        # pylint: disable=import-outside-toplevel
        from dialog import dialog_functions
        if self.function_name:
            f = getattr(dialog_functions, self.function_name)
            f(player)
