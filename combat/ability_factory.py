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

    def strong_attack(self, min_damage, max_damage):
        a = Ability("Strong Attack", cooldown=5)
        a.set_description("attack but better")
        a.set_to_hit(self.function_factory.strength_melee_attack())
        a.set_effect(self.function_factory.strength_melee_effect(min_damage + 5, max_damage + 5))
        return a
