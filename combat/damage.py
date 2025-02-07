from random import randint

# pylint: disable=redefined-builtin
class Damage:
    def __init__(self, min, max, type):
        self.min = min
        self.max = max
        self.type = type

    def get(self):
        return self.min, self.max, self.type

    def roll_damage(self):
        return randint(self.min, self.max)

    def apply_multiplier(self, multiplier):
        self.min = int(self.min * multiplier)
        self.max = int(self.max * multiplier)

    def add_damage(self, bonus):
        self.min += bonus
        self.max += bonus

    def clone(self):
        return Damage(self.min, self.max, self.type)
