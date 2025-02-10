from main.messenger import *
from creature.creature import Creature

messenger = get_messenger()

class Player(Creature):
    def __init__(self, name):
        super().__init__(name, 1)
        self.area = None
        self.room = None
        self.type = 'player'
        self.party: list[Creature] = [self]

    def dies(self):
        messenger.add('You die.')

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
            for e in c.effects:
                e.effect_end(c)
            c.effects.clear()
            c.action_points = 0

    def party_stat(self, stat):
        s = 0
        for c in self.party:
            s2 = c.stat(stat)
            if s2 > s:
                s = s2
        return s
