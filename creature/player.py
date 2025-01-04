from main.constants import *
from main.messenger import *
from creature.creature import Creature
from quests.quest import Quest

messenger = get_messenger()

class Player(Creature):
    def __init__(self, name, sprite_rect):
        super().__init__(name, sprite_rect)
        self.party: list[Creature] = [self]

        self.main_quests: list[Quest] = []
        self.side_quests: list[Quest] = []

    def dies(self):
        messenger.add('You die.')

    def get_quests(self):
        return self.main_quests + self.side_quests
