from creature.creature import Creature
from creature.player import Player
from creature.npc import *
from creature.profession_factory import get_profession_factory
from creature.ai.basic_ai import BasicAI
from combat.ability_factory import get_ability_factory

abilities = get_ability_factory()
professions = get_profession_factory()

# pylint: disable=invalid-name
_creature_factory = None
def get_creature_factory():
    global _creature_factory
    if not _creature_factory:
        _creature_factory = CreatureFactory()
    return _creature_factory

#pylint: disable=line-too-long
# If names are currently longer than 8 characters we get some visual overlap, fix later
class CreatureFactory:
    def new_player(self):
        player = Player("Player", (1,1,12,12))
        player.set_description("A fine specimen of an adventurer, if 'fine' means covered in dirt, blood, and questionable life choices.")
        player.set_defensive_stats(base_hp=10, defense=5, dodge=2, will=2, endurance=2)
        player.set_offensive_stats(speed=5, strength=3, dexterity=2, intelligence=1)
        player.add_ability(abilities.basic_attack(1, 4))
        player.add_ability(abilities.heavy_blow(0, 2))
        player.set_profession(professions.new_test_wizard(), 1)
        return player

    def new_companion_1(self):
        c = Creature("Companion", (1,14,12,12))
        c.set_defensive_stats(base_hp=6, defense=2, dodge=3, will=3, endurance=1)
        c.set_offensive_stats(speed=4, strength=1, dexterity=2, intelligence=3)
        c.add_ability(abilities.basic_attack(1, 2))
        c.add_ability(abilities.flickering_flames(85))
        return c

    def new_patchwork_dead_1(self):
        c = Creature("Patchwork Dead", (1,27,12,12))
        c.set_description("Sloppily assembled from discarded remains, this undead barely holds together. "
                          "A missing eye socket leaks dark fluid, and its left arm is attached at an unnatural angle. "
                          "It takes a step, and something wet and rotten falls from its torso, but it shuffles on undeterred.")
        c.set_defensive_stats(base_hp=4, defense=1, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=0, intelligence=0)
        c.set_profession(professions.new_enemy_profession("Shuffler"), 0)
        c.add_ability(abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_patchwork_dead_2(self):
        c = Creature("Patchwork Dead", (14,27,12,12))
        c.set_description("This crude abomination is hastily sewn together, its seams splitting with every jerky movement. "
                          "Its face is an awful mismatch—one eye wide and unblinking, the other sunken and dead. "
                          "Its mouth stretches too far, pulled open by uneven stitches, revealing a grotesque attempt at a snarl.")
        c.set_defensive_stats(base_hp=4, defense=3, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=2, dexterity=0, intelligence=0)
        c.set_profession(professions.new_enemy_profession("Brute"), 0)
        c.add_ability(abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_patchwork_dead_3(self):
        c = Creature("Patchwork Dead", (27,27,12,12))
        c.set_description("This undead creature lurches forward on uneven legs, its body stitched together from mismatched limbs. "
                          "One arm is bloated and bruised, the other little more than bone. "
                          "Its head is loosely attached, lolling to the side as it groans mindlessly.")
        c.set_defensive_stats(base_hp=4, defense=0, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=0, intelligence=0)
        c.set_profession(professions.new_enemy_profession("Shambler"), 0)
        c.add_ability(abilities.basic_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_harold(self):
        harold = Creature("Harold", (1,66,12,12))
        harold.set_defensive_stats(base_hp=5, defense=4, dodge=1, will=2, endurance=1)
        harold.set_resistances(physical=20)
        harold.set_offensive_stats(speed=1, strength=4, dexterity=1, intelligence=1)
        harold.add_ability(abilities.basic_attack(1, 3))
        harold.set_ai(BasicAI(harold))
        return harold

    def new_elder_varik(self):
        varik = NPC("Elder Varik", (14,40,12,12))
        varik.dialog_function = elder_varik_dialog
        return varik

    def new_gorren(self):
        gorren = NPC("Gorren", (14,1,12,12))
        gorren.set_description("A scrawny young man with hollow cheeks, wide eyes, and the scent of damp earth clinging to his tattered robes. "
                               "Gorren was once a gravedigger, but after too many lonely nights among the dead, he became obsessed with mastering necromancy.")
        gorren.set_defensive_stats(base_hp=6, defense=2, dodge=3, will=3, endurance=1)
        gorren.set_offensive_stats(speed=4, strength=1, dexterity=2, intelligence=3)
        gorren.set_profession(professions.new_test_wizard(), 1)
        gorren.add_ability(abilities.basic_attack(1, 2))
        gorren.dialog_function = gorren_dialogue
        return gorren
