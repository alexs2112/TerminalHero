from creature.npc import NPC
from world.encounter import Encounter
from world.feature import *
from main.player_log import get_player_log, update_log
player_log = get_player_log()

class Area:
    def __init__(self, name, sprite_rect):
        self.type = 'Area'
        self.name: str = name
        self.sprite_rect: str = sprite_rect
        self.player = None
        self.npcs: list[NPC] = []
        self.encounters: list[Encounter] = []
        self.features: list[Feature] = []
        self.dungeon = None

        # A list of descriptions and player_log entries
        # Show the latest description that has all entries as true
        # The first entrance should ideally have no player_log entries
        self.descriptions: list[tuple[str, list[str]]] = []

        # If the player needs to meet a condition to know about this area
        self.condition: str = None

        # If this area is just filler to make the map look better
        # Find a better way to handle this eventually
        self.is_filler: bool = False

        # Entering this area will set this player_log field as true
        self.entry_log_update: str = None

    def get_description(self):
        # Do this backwards to return the latest description that meets requirements
        i = len(self.descriptions) - 1
        while i >= 0:
            select = True
            desc, reqs = self.descriptions[i]
            if reqs:
                for r in reqs:
                    if not player_log[r]:
                        select = False
                        break
            if select:
                return desc
            i -= 1
        return ""

    def add_description(self, description, *requirements):
        self.descriptions.append((description, requirements))

    def condition_met(self):
        if self.condition in player_log:
            return player_log[self.condition]
        return True

    def enter_area(self, player):
        player.area = self
        self.player = player
        update_log(self.entry_log_update)

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

    def get_function_features(self):
        return [ f for f in self.features if f.enabled() and f.type == FUNCTION ]

    def get_store_features(self):
        return [ f for f in self.features if f.enabled() and f.type == FOOD_STORE ]

    def get_area_features(self):
        return [ f for f in self.features if f.enabled() and f.type == AREA ]
