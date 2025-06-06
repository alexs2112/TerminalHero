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
    def create_disarmed_effect(self, duration, strength):
        return DisarmedEffect(duration, strength)

    def create_stun_effect(self, duration):
        return StunEffect(duration)

    def create_decaying_effect(self, duration, strength):
        return DecayingEffect(duration, strength)

    def create_bolstered_effect(self, duration, str_buff, armor_buff):
        return BolsteredEffect(duration, str_buff, armor_buff)

    def create_bleed_effect(self, duration, strength):
        return BleedEffect(duration, strength)

    def create_armor_effect(self, duration, strength):
        return ArmorEffect(duration, strength)

    def create_drained_effect(self, duration, strength):
        return DrainedEffect(duration, strength)

    def create_blinded_effect(self, duration, strength):
        return BlindedEffect(duration, strength)
