from combat.ability import Ability
from combat.ability_function_factory import AbilityFunctionFactory

class AbilityFactory():
    def __init__(self):
        self.function_factory = AbilityFunctionFactory()

    def basic_attack(self, min_damage, max_damage):
        a = Ability("Attack", cooldown=1)
        a.set_description("attack...")
        a.set_to_hit(self.function_factory.strength_melee_attack())
        a.set_effect(self.function_factory.strength_melee_effect(min_damage, max_damage))
        return a
