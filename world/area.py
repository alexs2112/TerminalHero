from creature.creature import Creature
from creature.npc import NPC
from creature.player import Player

class Area:
    def __init__(self, name, sprite_rect, description):
        self.name: str = name
        self.sprite_rect: str = sprite_rect
        self.description: str = description
        self.player: Player = None
        self.allies: list[Creature] = []
        self.enemies: list[Creature] = []
        self.npcs: list[NPC] = []
