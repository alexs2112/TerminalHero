from random import random, randint
from creature.creature import Creature
from combat.effect_factory import get_effect_factory
from world.area import Area
from main.messenger import get_messenger

messenger = get_messenger()
effects = get_effect_factory()

# pylint: disable=invalid-name
_ability_function_factory = None
def get_ability_function_factory():
    global _ability_function_factory
    if not _ability_function_factory:
        _ability_function_factory = AbilityFunctionFactory()
    return _ability_function_factory

# pylint: disable=unused-argument
class AbilityFunctionFactory:
    def strength_melee_attack(self):
        def out(c: Creature, t: Creature, a: Area):
            roll = random() * 100
            success = roll > t.stat('dodge') * 5
            if not success:
                messenger.add(f"{c.name} misses {t.name} with an attack.")
            return success
        return out

    def strength_melee_effect(self, dam_min, dam_max):
        def out(c: Creature, t: Creature, a: Area):
            dam = randint(dam_min + c.stat('strength'), dam_max + c.stat('strength'))
            messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
            t.take_damage(dam, 'physical')
        return out

    def heavy_blow_attack(self):
        # This is pretty much exactly the same as strength_melee_attack
        def out(c: Creature, t: Creature, a: Area):
            roll = random() * 100
            success = roll > t.stat('dodge') * 5
            if not success:
                messenger.add(f"{c.name} misses {t.name} with a heavy blow.")
            return success
        return out

    def heavy_blow_effect(self, dam_min, dam_max, base_stun_chance):
        def out(c: Creature, t: Creature, a: Area):
            dam = randint(dam_min + c.stat('strength'), dam_max + c.stat('strength'))
            messenger.add(f"{c.name} heavy attacks {t.name} for {dam} damage!")
            t.take_damage(dam, 'physical')
            if t.is_alive():
                roll = random() * 100
                if roll < base_stun_chance - t.stat('endurance') * 5 + c.stat('strength') * 5:
                    t.add_effect(effects.create_stun_effect(1))
                else:
                    messenger.add(f"{t.name} shrugs off the stun.")
        return out

    def flickering_flames_attack(self, base_hit_chance):
        def out(c: Creature, t: Creature, a: Area):
            roll = random() * 100
            success = roll < base_hit_chance - t.stat('dodge') * 5 + c.stat('intelligence') * 5
            if not success:
                messenger.add(f"{c.name} throws flame at {t.name} but misses.")
            return success
        return out

    def flickering_flames_effect(self):
        def out(c: Creature, t: Creature, a: Area):
            messenger.add(f"{c.name} casts Flickering Flames.")
            t.add_effect(effects.create_burning_effect(c.stat('intelligence'), 2 + c.stat('intelligence')))
        return out
