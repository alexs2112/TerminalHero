from creature.npc import NPC
from world.encounter import Encounter
from world.feature import *
from main.player_log import get_player_log, update_log
player_log = get_player_log()

class Area:
    def __init__(self, name, sprite_rect, description):
        self.type = 'Area'
        self.name: str = name
        self.sprite_rect: str = sprite_rect
        self.description: str = description
        self.npcs: list[NPC] = []
        self.encounters: list[Encounter] = []
        self.features: list[Feature] = []
        self.dungeon = None

        # If the player needs to meet a condition to know about this area
        self.condition: str = None

        # If this area is just filler to make the map look better
        # Find a better way to handle this eventually
        self.is_filler: bool = False

        # Entering this area will set this player_log field as true
        self.entry_log_update: str = None

    def condition_met(self):
        if self.condition in player_log:
            return player_log[self.condition]
        return True

    def enter_area(self, player):
        player.area = self
        update_log(self.entry_log_update, player)

    def finish_encounter(self, encounter: Encounter, player):
        encounter.complete(player, self)

    def enabled_encounters(self):
        return [ e for e in self.encounters if e.enabled() ]

    def get_encounter(self):
        return self.enabled_encounters()[0]

    def enabled_features(self):
        return [ f for f in self.features if f.enabled() ]

    def get_dialog_features(self):
        return [ f for f in self.features if f.enabled() and f.type == DIALOG ]
