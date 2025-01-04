from creature.creature import Creature
from creature.player import Player
from creature.npc import *
from creature.ai.basic_ai import BasicAI
from combat.ability_factory import AbilityFactory

#pylint: disable=line-too-long
# If names are currently longer than 8 characters we get some visual overlap, fix later
class CreatureFactory:
    def __init__(self):
        self.abilities = AbilityFactory()

    def new_player(self):
        player = Player("Player", (1,1,12,12))
        player.set_defensive_stats(max_hp=10, armor=5, dodge=2, will=2, endurance=2)
        player.set_offensive_stats(speed=5, strength=3, dexterity=2, intelligence=1)
        player.add_ability(self.abilities.basic_attack(1, 4))
        player.add_ability(self.abilities.heavy_blow(0, 2))
        return player

    def new_companion_1(self):
        c = Creature("Companion", (1,14,12,12))
        c.set_defensive_stats(max_hp=6, armor=2, dodge=3, will=3, endurance=1)
        c.set_offensive_stats(speed=4, strength=1, dexterity=2, intelligence=3)
        c.add_ability(self.abilities.basic_attack(1, 2))
        c.add_ability(self.abilities.flickering_flames(85))
        return c

    def new_patchwork_dead_1(self):
        c = Creature("Patchwork Dead", (1,27,12,12))
        c.set_defensive_stats(max_hp=4, armor=1, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=0, intelligence=0)
        c.add_ability(self.abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_patchwork_dead_2(self):
        c = Creature("Patchwork Dead", (14,27,12,12))
        c.set_defensive_stats(max_hp=4, armor=3, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=2, dexterity=0, intelligence=0)
        c.add_ability(self.abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_patchwork_dead_3(self):
        c = Creature("Patchwork Dead", (27,27,12,12))
        c.set_defensive_stats(max_hp=4, armor=0, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=0, intelligence=0)
        c.add_ability(self.abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_harold(self):
        harold = Creature("Harold", (1,66,12,12))
        harold.set_defensive_stats(max_hp=5, armor=4, dodge=1, will=2, endurance=1)
        harold.set_resistances(physical=20)
        harold.set_offensive_stats(speed=1, strength=4, dexterity=1, intelligence=1)
        harold.add_ability(self.abilities.basic_attack(1, 3))
        harold.set_ai(BasicAI(harold))
        return harold

    def new_elder_varik(self):
        varik = NPC("Elder Varik", (14,40,12,12))
        varik.dialog_function = elder_varik_dialog
        return varik

    def new_gorren(self):
        gorren = NPC("Gorren", (14,1,12,12))
        gorren.set_defensive_stats(max_hp=6, armor=2, dodge=3, will=3, endurance=1)
        gorren.set_offensive_stats(speed=4, strength=1, dexterity=2, intelligence=3)
        gorren.add_ability(self.abilities.basic_attack(1, 2))
        gorren.add_ability(self.abilities.flickering_flames(85))
        gorren.dialog_function = gorren_dialogue
        return gorren
