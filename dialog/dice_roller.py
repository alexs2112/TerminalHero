from random import randint

class DiceRoller:
    def __init__(self):
        self.first = 0
        self.second = 0

    def roll(self):
        self.first = randint(1,6)
        self.second = randint(1,6)

    def get_roll(self):
        return self.first, self.second

    def total(self):
        return self.first + self.second
