from main.messenger import *
from creature.creature import Creature
from creature.item import Item
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

        self.key_items: list[Item] = []
        self.inventory: list[Item] = []

    def dies(self):
        messenger.add('You die.')

    def get_quests(self):
        return self.main_quests + self.side_quests

    def start_combat(self):
        for c in self.party:
            c.armor = c.max_armor()
            for a in c.get_abilities():
                a.cooldown = 0

    def end_combat(self):
        for c in self.party:
            if not c.is_alive():
                pass
            c.effects.clear()
