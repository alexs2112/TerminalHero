from main.messenger import *
from creature.creature import Creature
from creature.item import Item
from quests.quest import Quest

messenger = get_messenger()

class Player(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.area = None
        self.type = 'player'
        self.party: list[Creature] = [self]

        self.main_quests: list[Quest] = []
        self.side_quests: list[Quest] = []
        self.done_quests: list[Quest] = []

        # Inventory also defined in Creature
        # Might want to get rid of key_items and just mark the item differently if its key?
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
            c.has_corpse = True

    def end_combat(self):
        for c in self.party:
            if not c.is_alive():
                pass
            c.effects.clear()

    def party_stat(self, stat):
        s = 0
        for c in self.party:
            s2 = c.stat(stat)
            if s2 > s:
                s = s2
        return s
