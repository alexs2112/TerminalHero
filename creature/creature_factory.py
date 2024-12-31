from creature.creature import Creature
from creature.player import Player
from creature.npc import NPC
from creature.npc import *
from creature.ai.basic_ai import BasicAI

#pylint: disable=line-too-long
# If names are currently longer than 8 characters we get some visual overlap, fix later
class CreatureFactory:
    def new_player(self):
        player = Player("Player", (1,1,12,12))
        player.set_combat_stats(10, 2, 5, 5, 0)
        return player

    def new_rotfang_widow(self):
        rotfang = Creature("Rotfang Widow", (1,66,12,12))
        rotfang.set_description("The Rotfang Widow is known for its grotesque feeding habits, often lingering over decomposing corpses for days. "
                                "Its venom causes rapid decomposition, softening flesh for easier consumption.")
        rotfang.set_combat_stats(5, 1, 2, 3, 2)
        rotfang.set_ai(BasicAI(rotfang))
        return rotfang

    def new_bonechewer_beetle(self):
        bonechewer = Creature("Bonechewer Beetle", (14,66,12,12))
        bonechewer.set_description("Feasting on marrow and sinew, the Bonechewer Beetle crushes bones with ease. "
                                   "Its tough exoskeleton is lined with jagged protrusions, remnants of a grotesque metamorphosis spurred by its gruesome diet.")
        bonechewer.set_combat_stats(5, 1, 2, 3, 2)
        bonechewer.set_ai(BasicAI(bonechewer))
        return bonechewer

    def new_deathburrower(self):
        deathburrower = Creature("Deathburrower", (27,66,12,12))
        deathburrower.set_description("This eerie insect tunnels through graveyards, disturbing the dead as it searches for sustenance. "
                                      "Its gnarled, extended abdomen acts as both a weapon and a tool for extracting nutrients from decomposed remains.")
        deathburrower.set_combat_stats(5,1,2,3, 2)
        deathburrower.set_ai(BasicAI(deathburrower))
        return deathburrower

    def new_goblin(self):
        goblin = Creature("Goblin", (1,27,12,12))
        goblin.set_combat_stats(5, 1, 2, 3, 1)
        goblin.set_ai(BasicAI(goblin))
        return goblin

    def new_kobold(self):
        kobold = Creature("Kobold", (1,40,12,12))
        kobold.set_combat_stats(3, 1, 2, 3, 2)
        kobold.set_ai(BasicAI(kobold))
        return kobold

    def new_harold(self):
        harold = Creature("Harold", (1,53,12,12))
        harold.set_combat_stats(4, 4, 2, 3, 3)
        harold.set_ai(BasicAI(harold))
        return harold

    def new_elder_varik(self):
        varik = NPC("Elder Varik", (14,1,12,12))
        varik.dialog_function = elder_varik_dialog
        return varik
