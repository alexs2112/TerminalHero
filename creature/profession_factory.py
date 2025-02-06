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

    def champion(self):
        p = Profession("Champion")
        p.set_stats(strength=2, endurance=1)
        p.add_ability(abilities.multi_attack(1,3))
        p.add_ability(abilities.bolster(1,5))
        return p

    def dualist(self):
        p = Profession("Dualist")
        p.set_stats(strength=1, dexterity=1, dodge=1, speed=1)
        p.add_ability(abilities.defensive_strike(1,3))
        p.add_ability(abilities.challenge(2, 30))
        return p

    def elementalist(self):
        p = Profession("Elementalist")
        p.set_stats(intelligence=2, will=2, dodge=1)
        p.add_ability(abilities.rainstorm())
        p.add_ability(abilities.lightning_strike(0,2,90))
        return p

    def luminarch(self):
        p = Profession("Luminarch")
        p.set_stats(strength=1, wisdom=1, endurance=2)
        p.add_ability(abilities.rallying_cry())
        p.add_ability(abilities.enchant_weapon())
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
