from random import random, randint
from creature.creature import Creature
from main.messenger import get_messenger

messenger = get_messenger()

class AbilityFunctionFactory:
    def strength_melee_attack(self):
        def out(creature: Creature, target: Creature):
            roll = random() * 100
            success = roll > target.dodge * 5
            if not success:
                messenger.add(f"{creature.name} misses {target.name}.")
            return success
        return out

    def strength_melee_effect(self, dam_min, dam_max):
        def out(c: Creature, t: Creature):
            dam = randint(dam_min + c.strength, dam_max + c.strength)
            messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
            t.take_damage(dam, 'physical')
        return out
