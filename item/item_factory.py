from item.item import *
from combat.ability_factory import get_ability_factory

abilities = get_ability_factory()

# pylint: disable=invalid-name
_item_factory = None
def get_item_factory():
    global _item_factory
    if not _item_factory:
        _item_factory = ItemFactory()
    return _item_factory

#pylint: disable=line-too-long
class ItemFactory:
    # WEAPONS
    def new_sword(self):
        i = Item("Sword", WEAPON, (0,0,12,12))
        i.set_equipped_sprite_rect((0,0,12,12))
        i.add_ability(abilities.basic_attack(1,3))
        i.add_ability(abilities.disarming_strike(1,3))
        return i

    def new_hammer(self):
        i = Item("Hammer", WEAPON, (0,12,12,12))
        i.set_equipped_sprite_rect((0,12,12,12))
        i.add_ability(abilities.basic_attack(1,3))
        i.add_ability(abilities.heavy_blow(1,3,80))
        return i

    def new_axe(self):
        i = Item("Axe", WEAPON, (0,24,12,12))
        i.set_equipped_sprite_rect((0,24,12,12))
        i.add_ability(abilities.basic_attack(1,3))
        i.add_ability(abilities.cleave(1,3,0))
        return i

    def new_staff(self):
        i = Item("Staff", WEAPON, (0,36,12,12))
        i.set_equipped_sprite_rect((0,36,12,12))
        i.add_ability(abilities.basic_attack(1,2))
        i.set_stats(intelligence=1)
        return i

    def new_shortbow(self):
        i = Item("Shortbow", WEAPON, (0,48,12,12))
        i.set_equipped_sprite_rect((0,48,12,12))
        i.add_ability(abilities.dexterity_attack(1,3))
        i.add_ability(abilities.power_shot(2,5))
        return i

    # ARMOR
    def new_leather_armor(self):
        i = Item("Leather Armor", ARMOR, (0,72,12,12))
        i.set_stats(defense=5, dodge=1)
        return i

    def new_robe(self):
        i = Item("Robe", ARMOR, (0,84,12,12))
        i.set_equipped_sprite_rect((0,84,12,12))
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

    def new_obsidian_lantern(self):
        i = Item("Obsidian Lantern", TRINKET, (12,120,12,12))
        i.set_stats(defense=5)
        i.set_resistances(dark=15)
        return i

    # FOOD
    def new_mushroom(self):
        f = Food("Plump Helmet", 10, (0,132,12,12), 'food_mushroom')
        f.set_description("Stubby, dome-capped fungi found in damp caves and shadowed groves. "
                          "Commonly used in stews, though some varieties induce vivid hallucinations or, in unfortunate cases, brief conversations with the recently deceased.")
        f.set_stats(intelligence=1)
        return f

    def new_carrot(self):
        f = Food("Buried Torch", 10, (12,132,12,12), 'food_carrot')
        f.set_description("Bright orange root vegetable, often unearthed with a satisfying pop. "
                          "Sweet, crisp, and rumored to improve night vision, though this may be a fabrication by desperate parents and dubious alchemists.")
        f.set_stats(dexterity=1)
        return f

    def new_steak(self):
        f = Food("Firecut", 10, (24,132,12,12), 'food_steak')
        f.set_description("A thick slab of meat, seared over an open flame or hot stone. "
                          "A staple of hearty meals, best served with a flagon of something strong and a moment of silence for the beast it came from.")
        f.set_stats(strength=1)
        return f

    def new_cheese(self):
        f = Food("Stonecurd", 10, (36,132,12,12), 'food_cheese')
        f.set_description("A hardened block of aged curd, ranging from smooth to crumbly in texture. "
                          "A common travel ration, as it keeps well and pairs with nearly anything, if one can handle its sometimes overpowering tang.")
        f.set_stats(endurance=2)
        return f
