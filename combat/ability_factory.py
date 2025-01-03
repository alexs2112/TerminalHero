from combat.ability import Ability
from combat.ability_function_factory import AbilityFunctionFactory

class AbilityFactory():
    def __init__(self):
        self.function_factory = AbilityFunctionFactory()

    def basic_attack(self, min_damage, max_damage):
        a = Ability("Attack", cooldown=1)
        a.set_description("Melee attack an enemy.")
        a.set_to_hit(self.function_factory.strength_melee_attack())
        a.set_effect(self.function_factory.strength_melee_effect(min_damage, max_damage))
        return a

    def heavy_blow(self, min_damage, max_damage):
        a = Ability("Heavy Blow", cooldown=3)
        a.set_description("Swing a heavy blow to stun your target.")
        a.set_to_hit(self.function_factory.heavy_blow_attack())
        a.set_effect(self.function_factory.heavy_blow_effect(min_damage, max_damage, 90))
        return a

    def flickering_flames(self, base_hit_chance):
        a = Ability("Flickering Flames", cooldown=3)
        a.set_description("Attempt to light an enemy on fire.")
        a.set_to_hit(self.function_factory.flickering_flames_attack(base_hit_chance))
        a.set_effect(self.function_factory.flickering_flames_effect())
        return a
