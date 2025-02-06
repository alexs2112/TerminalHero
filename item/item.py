from main.player_log import get_player_log

player_log = get_player_log()

# Defining constants as the item slots
WEAPON = 'Weapon'
ARMOR = 'Armor'
TRINKET = 'Trinket'
ITEM_SLOTS = [ WEAPON, ARMOR, TRINKET ]
EQUIPMENT = 'Equipment'
FOOD = 'Food'

class Item:
    def __init__(self, name, item_type, sprite_rect):
        self.name = name
        self.type = item_type
        self.sprite_rect = sprite_rect
        self.description = ""

    def set_description(self, desc):
        self.description = desc

class Equipment(Item):
    def __init__(self, name, sprite_rect, slot):
        super().__init__(name, EQUIPMENT, sprite_rect)
        self.slot = slot
        self.equipped_sprite_rect = None
        self.abilities = []
        self.stats = {}
        self.resistances = {}

    def set_equipped_sprite_rect(self, rect):
        self.equipped_sprite_rect = rect

    def add_ability(self, ability):
        self.abilities.append(ability)

    def set_stats(self, **kwargs):
        self.stats = kwargs

    def set_resistances(self, **kwargs):
        self.resistances = kwargs

class Food(Item):
    def __init__(self, name, cost, sprite_rect, log_entry):
        super().__init__(name, FOOD, sprite_rect)
        self.name = name
        self.cost = cost
        self.sprite_rect = sprite_rect
        self.stats = {}
        self.resistances = {}

        # If the player has eaten this before or not
        self.log_entry = log_entry

    def set_stats(self, **kwargs):
        self.stats = kwargs

    def set_resistances(self, **kwargs):
        self.resistances = kwargs

    def is_known(self):
        return player_log[self.log_entry]

    def get_stat_strings(self):
        out = []
        for stat, value in self.stats.items():
            out.append(f"{stat} {'+' if value > 0 else ''} {value}")
        for resist, value in self.resistances:
            out.append(f"{resist} {'+' if value > 0 else ''} {value}%")
        return out
