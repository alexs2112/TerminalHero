from creature.profession import Profession
from combat.damage import Damage
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
        p.set_description(
            "A hardened warrior forged by battle and hardship. "
            "You wield your axe with brutal efficiency, cutting down all who stand in your path."
            "Steel in your hands, fire in your heart. "
            "You are the wall that will not break, the force that will not falter."
        )
        p.set_stats(strength=2, endurance=1)
        p.add_ability(abilities.multi_attack(strength=1))
        p.add_ability(abilities.bolster(1, 5))
        return p

    def duelist(self):
        p = Profession("Duelist")
        p.set_description(
            "A master of the blade, swift and calculating. "
            "Every fight is a duel in your eyes, and you never strike without intent."
            "Honour, skill, and cunning define you. "
            "To face you in combat is to accept an unwinnable wager."
        )
        p.set_stats(strength=1, dexterity=1, dodge=1, speed=1)
        p.add_ability(abilities.defensive_strike(strength=0.67, dexterity=0.67))
        p.add_ability(abilities.challenge(2, 300))
        return p

    def elementalist(self):
        p = Profession("Elementalist")
        p.set_description(
            "The elements answer your call, shaping fire, ice, and storm at your fingertips. "
            "Magic is not a tool to you - it is an extension of your will. "
            "With each spell, you unravel the secrets of creation itself."
        )
        p.set_stats(intelligence=2, will=2, dodge=1)
        p.add_ability(abilities.rainstorm())
        p.add_ability(abilities.lightning_strike(Damage(1,3,'air'), 90, intelligence=1))
        return p

    def luminarch(self):
        p = Profession("Luminarch")
        p.set_description(
            "A beacon in the darkness, clad in shining steel. "
            "You wield your faith like a weapon, striking down those who would defy the light. "
            "Your presence alone is enough to rally the weary. "
            "In battle, you are both shield and hammer, standing unshaken against the tide."
        )
        p.set_stats(strength=1, wisdom=1, endurance=2)
        p.add_ability(abilities.rallying_cry())
        p.add_ability(abilities.enchant_weapon())
        return p

    def soulwarden(self):
        p = Profession("Soulwarden")
        p.set_stats(intelligence=2, will=1, endurance=1)
        p.set_resistances(dark=10)
        p.add_ability(abilities.drain_life(90, Damage(0, 2, 'dark'), intelligence=1))
        p.add_ability(abilities.corpse_explosion(Damage(1,3,'dark'), intelligence=1.25))
        p.add_ability(abilities.curse_of_decay(Damage(0, 2, 'dark'), intelligence=1))
        return p

    def ashen_stalker(self):
        p = Profession("Ashen Stalker")
        p.set_stats(dexterity=2, intelligence=1, speed=1, dodge=1)
        p.add_ability(abilities.blinding_smoke(80))
        p.add_ability(abilities.flickering_flames(80))
        return p
