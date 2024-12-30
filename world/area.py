from creature.creature import Creature
from creature.npc import NPC
from creature.player import Player
from main.player_log import get_player_log
player_log = get_player_log()

class Area:
    def __init__(self, name, sprite_rect, description):
        self.name: str = name
        self.sprite_rect: str = sprite_rect
        self.description: str = description
        self.player: Player = None
        self.allies: list[Creature] = []
        self.enemies: list[Creature] = []
        self.npcs: list[NPC] = []

        # If the player needs to meet a condition to know about this area
        self.condition: str = None

        # If this area is just filler to make the map look better
        # Find a better way to handle this eventually
        self.is_filler: bool = False

    def condition_met(self):
        if self.condition:
            if self.condition in player_log:
                return player_log[self.condition]
        return True
