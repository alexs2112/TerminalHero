from creature.creature import Creature
from main.player_log import get_player_log

player_log = get_player_log()

class Encounter:
    def __init__(self, name):
        self.name: str = name
        self.enemies: list[Creature] = []
        self.completed: bool = False

        # Condition in player_log that makes this encounter appear in an area
        self.valid_condition: str = None

        # Function that is called when the encounter is completed
        self.completed_function = None

    def enabled(self):
        if self.completed:
            return False
        if self.valid_condition in player_log:
            return player_log[self.valid_condition]
        return True

    def set_completed_function(self, func):
        self.completed_function = func

    def complete(self, player, area):
        self.completed = True
        if self.completed_function:
            self.completed_function(player, area)
