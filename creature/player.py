from main.constants import *
from main.messenger import *
from creature.creature import Creature

messenger = get_messenger()

class Player(Creature):
    def __init__(self, name, sprite_rect):
        super().__init__(name, sprite_rect)
        self.party: list[Creature] = [self]

    def dies(self):
        messenger.add('You die.')
        messenger.add('Press [enter] to continue.')
