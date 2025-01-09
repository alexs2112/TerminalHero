from main.messenger import *
from creature.creature import Creature
from quests.quest import Quest

messenger = get_messenger()

class Player(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.area = None
        self.party: list[Creature] = [self]

        self.main_quests: list[Quest] = []
        self.side_quests: list[Quest] = []
        self.done_quests: list[Quest] = []

    def dies(self):
        messenger.add('You die.')

    def get_quests(self):
        return self.main_quests + self.side_quests

    def end_combat(self):
        for c in self.party:
            if not c.is_alive():
                pass
            c.effects.clear()
            c.armor = c.max_armor()
            for a in c.get_abilities():
                a.cooldown = 0
