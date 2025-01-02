from combat.effect import *
from main.constants import *
from main.messenger import get_messenger
messenger = get_messenger()

class EffectFactory:
    def create_fire_effect(self, damage, duration):
        e = Effect('Burning', duration, ORANGE)
        def start(creature):
            messenger.add(f"{creature.name} catches fire!")
        e.set_effect_start(start)
        def turn(creature):
            messenger.add(f"{creature.name} takes {damage} fire damage.")
            creature.take_damage(damage, 'fire')
        e.set_effect_turn(turn)
        def end(creature):
            messenger.add(f"{creature.name} puts out the flames.")
        e.set_effect_end(end)
        return e

    def create_stun_effect(self, duration):
        e = Effect('Stunned', duration, CYAN)
        def f(creature):
            messenger.add(f"{creature.name} is stunned.")
            creature.skip_next_turn = True
        e.set_effect_start(f)
        e.set_effect_turn(f)
        def end(creature):
            messenger.add(f"{creature.name} recovers from the stun.")
        e.set_effect_end(end)
        return e
