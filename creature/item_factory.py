from creature.item import *
from combat.ability_factory import get_ability_factory

abilities = get_ability_factory()

# pylint: disable=invalid-name
_item_factory = None
def get_item_factory():
    global _item_factory
    if not _item_factory:
        _item_factory = ItemFactory()
    return _item_factory

class ItemFactory:
    # WEAPONS
    def new_sword(self):
        i = Item("Sword", WEAPON, (0,0,12,12))
        i.set_equipped_sprite_rect((12,24,12,12))
        i.add_ability(abilities.basic_attack(1,3))
        i.add_ability(abilities.disarming_strike(1,3))
        return i

    def new_hammer(self):
        i = Item("Hammer", WEAPON, (0,12,12,12))
        i.set_equipped_sprite_rect((24,24,12,12))
        i.add_ability(abilities.basic_attack(1,3))
        i.add_ability(abilities.heavy_blow(1,3,80))
        return i

    def new_axe(self):
        i = Item("Axe", WEAPON, (0,24,12,12))
        i.set_equipped_sprite_rect((36,24,12,12))
        i.add_ability(abilities.basic_attack(1,3))
        i.add_ability(abilities.cleave(1,3,0))
        return i

    def new_staff(self):
        i = Item("Staff", WEAPON, (0,36,12,12))
        i.set_equipped_sprite_rect((48,24,12,12))
        i.add_ability(abilities.basic_attack(1,2))
        i.set_stats(intelligence=1)
        return i

    # ARMOR
    def new_leather_armor(self):
        i = Item("Leather Armor", ARMOR, (0,72,12,12))
        i.set_stats(defense=5, dodge=1)
        return i

    def new_robe(self):
        i = Item("Robe", ARMOR, (0,84,12,12))
        i.set_stats(defense=3, dodge=3, speed=1)
        return i

    # KEY ITEMS
    def new_vaelthorne_seal(self):
        i = Item("Vaelthorne Seal", TRINKET, (0,120,12,12))
        i.set_resistances(
            fire=20,
            cold=20,
            air=20,
            poison=20,
        )
        # Heal wearer at the end of each combat
        return i
