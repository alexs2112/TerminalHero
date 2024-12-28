from creature.creature import Creature
from creature.player import Player
from creature.ai.basic_ai import BasicAI

class CreatureFactory:
    def new_player(self):
        return Player("Player", (1,1,12,12), 10, 2, 5, 5)

    def new_goblin(self):
        goblin = Creature("Goblin", (1,27,12,12), 5, 1, 2, 3)
        goblin.ai = BasicAI(goblin)
        return goblin

    def new_kobold(self):
        kobold = Creature("Kobold", (1,40,12,12), 3, 1, 2, 3)
        kobold.ai = BasicAI(kobold)
        return kobold

    def new_harold(self):
        harold = Creature("Harold", (1,53,12,12), 4, 4, 2, 3)
        harold.ai = BasicAI(harold)
        return harold
