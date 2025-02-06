from creature.profession import Profession
from combat.ability_factory import get_ability_factory

abilities = get_ability_factory()

# pylint: disable=invalid-name
_profession_factory = None
def get_profession_factory():
    global _profession_factory
    if not _profession_factory:
        _profession_factory = ProfessionFactory()
    return _profession_factory

class ProfessionFactory:
    def enemy_profession(self, name):
        # We don't want enemy professions to add abilities and stats as those should be manually assigned
        return Profession(name)

    def new_test_warrior(self):
        p = Profession("Test Warrior")
        p.set_stats(strength=2, endurance=1)
        p.add_ability(abilities.multi_attack(1,3))
        p.add_ability(abilities.bolster(1,4))
        return p

    def soulwarden(self):
        p = Profession("Soulwarden")
        p.set_stats(intelligence=2, will=1, endurance=1)
        p.set_resistances(dark=10)
        p.add_ability(abilities.drain_life(90, 1, 2))
        p.add_ability(abilities.corpse_explosion(1, 3))
        p.add_ability(abilities.curse_of_decay())
        return p

    def ashen_stalker(self):
        p = Profession("Ashen Stalker")
        p.set_stats(dexterity=2, intelligence=1, speed=1, dodge=1)
        p.add_ability(abilities.blinding_smoke(80))
        p.add_ability(abilities.flickering_flames(80))
        # Another ability?
        return p
