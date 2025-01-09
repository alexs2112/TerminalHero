# Defining constants as the item slots
WEAPON = 'Weapon'
ARMOR = 'Armor'
TRINKET = 'Trinket'
ITEM_SLOTS = [ WEAPON, ARMOR, TRINKET ]

class Item:
    def __init__(self, name, slot, sprite_rect):
        self.name = name
        self.slot = slot
        self.sprite_rect = sprite_rect
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
