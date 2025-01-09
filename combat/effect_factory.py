from combat.effect_subclasses import *
from main.messenger import get_messenger
messenger = get_messenger()

# pylint: disable=invalid-name
_effect_factory = None
def get_effect_factory():
    global _effect_factory
    if not _effect_factory:
        _effect_factory = EffectFactory()
    return _effect_factory

class EffectFactory:
    def create_burning_effect(self, damage, duration):
        return BurningEffect(duration, damage)

    def create_disarmed_effect(self, duration, strength):
        return DisarmedEffect(duration, strength)

    def create_stun_effect(self, duration):
        return StunEffect(duration)

    def create_decaying_effect(self, duration, strength):
        return DecayingEffect(duration, strength)
