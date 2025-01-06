from combat.effect import Effect
from main.colour import *
from main.messenger import get_messenger
messenger = get_messenger()

class BurningEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Burning", duration, ORANGE)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} catches fire!")
        creature.take_damage(self.strength, 'fire')

    def effect_turn(self, creature):
        creature.take_damage(self.strength, 'fire')
        self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} puts out the flames.")

    def combine(self, other_effect):
        if other_effect.name == self.name:
            self.duration = max(other_effect.duration, self.duration)
            self.strength = max(other_effect.strength, self.strength)
            messenger.add("The flames burn brighter!")
            return True
        return False

class StunEffect(Effect):
    def __init__(self, duration):
        super().__init__("Stunned", duration, CYAN)

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is stunned.")
        creature.skip_next_turn = True

    def effect_turn(self, creature):
        messenger.add(f"{creature.name} is stunned.")
        self.duration -= 1
        if self.duration > 0:
            creature.skip_next_turn = True

    def effect_end(self, creature):
        messenger.add(f"{creature.name} recovers from the stun.")

    def combine(self, other_effect):
        if other_effect.name == self.name:
            self.duration += other_effect.duration
            return True
        return False