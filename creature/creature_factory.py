from creature.creature import Creature
from creature.player import Player
from creature.npc import NPC
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

    def new_rotfang_widow(self):
        c = Creature("Rotfang Widow", (1,66,12,12))
        c.set_description("The Rotfang Widow is known for its grotesque feeding habits, often lingering over decomposing corpses for days. "
                                "Its venom causes rapid decomposition, softening flesh for easier consumption.")
        c.set_defensive_stats(max_hp=5, armor=2, dodge=1, will=2, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=1, intelligence=1)
        c.add_ability(self.abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_bonechewer_beetle(self):
        c = Creature("Bonechewer Beetle", (14,66,12,12))
        c.set_description("Feasting on marrow and sinew, the Bonechewer Beetle crushes bones with ease. "
                                   "Its tough exoskeleton is lined with jagged protrusions, remnants of a grotesque metamorphosis spurred by its gruesome diet.")
        c.set_defensive_stats(max_hp=5, armor=2, dodge=1, will=2, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=1, intelligence=1)
        c.add_ability(self.abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_deathburrower(self):
        c = Creature("Deathburrower", (27,66,12,12))
        c.set_description("This eerie insect tunnels through graveyards, disturbing the dead as it searches for sustenance. "
                                      "Its gnarled, extended abdomen acts as both a weapon and a tool for extracting nutrients from decomposed remains.")
        c.set_defensive_stats(max_hp=5, armor=2, dodge=1, will=2, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=1, intelligence=1)
        c.add_ability(self.abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_goblin(self):
        goblin = Creature("Goblin", (1,27,12,12))
        goblin.set_defensive_stats(max_hp=5, armor=2, dodge=2, will=2, endurance=1)
        goblin.set_offensive_stats(speed=2, strength=2, dexterity=1, intelligence=1)
        goblin.add_ability(self.abilities.basic_attack(1, 3))
        goblin.set_ai(BasicAI(goblin))
        return goblin

    def new_kobold(self):
        kobold = Creature("Kobold", (1,40,12,12))
        kobold.set_defensive_stats(max_hp=4, armor=1, dodge=5, will=2, endurance=1)
        kobold.set_offensive_stats(speed=3, strength=1, dexterity=2, intelligence=1)
        kobold.add_ability(self.abilities.basic_attack(1, 3))
        kobold.set_ai(BasicAI(kobold))
        return kobold

    def new_harold(self):
        harold = Creature("Harold", (1,53,12,12))
        harold.set_defensive_stats(max_hp=5, armor=4, dodge=1, will=2, endurance=1)
        harold.set_resistances(physical=20)
        harold.set_offensive_stats(speed=1, strength=4, dexterity=1, intelligence=1)
        harold.add_ability(self.abilities.basic_attack(1, 3))
        harold.set_ai(BasicAI(harold))
        return harold

    def new_elder_varik(self):
        varik = NPC("Elder Varik", (14,1,12,12))
        varik.dialog_function = elder_varik_dialog
        return varik
