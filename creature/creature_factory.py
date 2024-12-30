from creature.creature import Creature
from creature.player import Player
from creature.npc import NPC
from creature.npc import *
from creature.ai.basic_ai import BasicAI

class CreatureFactory:
    def new_player(self):
        player = Player("Player", (1,1,12,12))
        player.set_combat_stats(10, 2, 5, 5)
        return player

    def new_goblin(self):
        goblin = Creature("Goblin", (1,27,12,12))
        goblin.set_combat_stats(5, 1, 2, 3)
        goblin.set_ai(BasicAI(goblin))
        return goblin

    def new_kobold(self):
        kobold = Creature("Kobold", (1,40,12,12))
        kobold.set_combat_stats(3, 1, 2, 3)
        kobold.set_ai(BasicAI(kobold))
        return kobold

    def new_harold(self):
        harold = Creature("Harold", (1,53,12,12))
        harold.set_combat_stats(4, 4, 2, 3)
        harold.set_ai(BasicAI(harold))
        return harold

    def new_elder_varik(self):
        varik = NPC("Elder Varik", (14,1,12,12))
        varik.dialog_function = elder_varik_dialog
        return varik
