from creature.creature import Creature
from creature.player import Player
from creature.npc import NPC
from creature.creature_sprite import CreatureSprite
from creature.profession_factory import get_profession_factory
from item.item_factory import get_item_factory
from creature.level_up_handler import get_level_up_handler
from creature.ai.basic_ai import BasicAI
from combat.ability_factory import get_ability_factory
from dialog.dialog_loader import *

abilities = get_ability_factory()
professions = get_profession_factory()
items = get_item_factory()
level_handler = get_level_up_handler()

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
        player = Player("Player")
        player.set_description("A fine specimen of an adventurer, if 'fine' means covered in dirt, blood, and questionable life choices.")
        player.set_sprite(CreatureSprite(-1, (0,0,12,12)))
        player.set_defensive_stats(base_hp=10, defense=0, dodge=2, will=2, endurance=2)
        player.set_offensive_stats(speed=5, strength=3, dexterity=2, intelligence=1)
        #player.equip_item(items.new_sword())
        player.equip_item(items.new_hammer())
        #player.equip_item(items.new_axe())
        player.equip_item(items.new_leather_armor())
        player.set_profession(professions.new_test_wizard())
        player.allied = True
        level_handler.add_creature(player)
        return player

    def new_companion_1(self):
        c = Creature("Companion", 1)
        c.set_sprite(CreatureSprite((0,36,12,12), (0,12,12,12)))
        c.set_defensive_stats(base_hp=6, defense=2, dodge=3, will=3, endurance=1)
        c.set_offensive_stats(speed=4, strength=1, dexterity=2, intelligence=3)
        c.add_ability(abilities.basic_attack(1, 2))
        c.add_ability(abilities.flickering_flames(85))
        c.allied = True
        level_handler.add_creature(c)
        return c

    def new_patchwork_dead_1(self):
        c = Creature("Patchwork Dead", 0)
        c.set_sprite(CreatureSprite((0,48,12,12), (12,0,12,12)))
        c.set_description("Sloppily assembled from discarded remains, this undead barely holds together. "
                          "A missing eye socket leaks dark fluid, and its left arm is attached at an unnatural angle. "
                          "It takes a step, and something wet and rotten falls from its torso, but it shuffles on undeterred.")
        c.set_defensive_stats(base_hp=4, defense=1, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=0, intelligence=0)
        c.set_profession(professions.enemy_profession("Shuffler"))
        c.add_ability(abilities.slow_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_patchwork_dead_2(self):
        c = Creature("Patchwork Dead", 0)
        c.set_sprite(CreatureSprite((12,48,12,12), (12,0,12,12)))
        c.set_description("This crude abomination is hastily sewn together, its seams splitting with every jerky movement. "
                          "Its face is an awful mismatch—one eye wide and unblinking, the other sunken and dead. "
                          "Its mouth stretches too far, pulled open by uneven stitches, revealing a grotesque attempt at a snarl.")
        c.set_defensive_stats(base_hp=4, defense=3, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=2, dexterity=0, intelligence=0)
        c.set_profession(professions.enemy_profession("Brute"))
        c.add_ability(abilities.slow_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_patchwork_dead_3(self):
        c = Creature("Patchwork Dead", 0)
        c.set_sprite(CreatureSprite((24,48,12,12), (12,0,12,12)))
        c.set_description("This undead creature lurches forward on uneven legs, its body stitched together from mismatched limbs. "
                          "One arm is bloated and bruised, the other little more than bone. "
                          "Its head is loosely attached, lolling to the side as it groans mindlessly.")
        c.set_defensive_stats(base_hp=4, defense=0, dodge=0, will=0, endurance=1)
        c.set_offensive_stats(speed=2, strength=1, dexterity=0, intelligence=0)
        c.set_profession(professions.enemy_profession("Shambler"))
        c.add_ability(abilities.slow_attack(1, 3))
        c.set_ai(BasicAI(c))
        return c

    def new_lanternbearer(self):
        c = Creature("Lanternbearer", 1)
        c.set_sprite(CreatureSprite((36,48,12,12), (60,0,12,12)))
        c.set_description("A skeletal figure clutching a rusted, glowing lantern that emits faint, necrotic light. "
                          "It appears to guide the undead forces.")
        c.set_defensive_stats(base_hp=5,defense=3,dodge=1,will=3,endurance=2)
        c.set_offensive_stats(speed=4, strength=1, dexterity=1, intelligence=3)
        c.set_profession(professions.enemy_profession("Guide of Lost Souls"))
        c.add_ability(abilities.basic_attack(1,3))
        c.add_ability(abilities.drain_life(85, 1, 2))
        c.add_ability(abilities.pale_light())
        c.set_ai(BasicAI(c))
        return c

    def new_rotten_stray(self):
        c = Creature("Rotten Stray", 1)
        c.set_sprite(CreatureSprite((48,48,12,12), (72,0,12,12)))
        c.set_description("Decayed canine corpse, animated to guard the cemetery from intruders.")
        c.set_defensive_stats(base_hp=4, defense=3, dodge=3, will=0, endurance=1)
        c.set_offensive_stats(speed=4, strength=2, dexterity=1, intelligence=1)
        c.set_profession(professions.enemy_profession("Hound"))
        c.add_ability(abilities.basic_attack(1,3))
        c.add_ability(abilities.rabid_bite(1,3))
        c.add_ability(abilities.chilling_howl('Rotten Stray'))
        c.set_ai(BasicAI(c))
        return c

    def new_runebound_stalker(self):
        c = Creature("Runebound Stalker", 3)
        c.set_sprite(CreatureSprite((0,96,12,12), (108,0,12,12)))
        c.set_description("A massive, four-armed feline-like predator, its body wrapped in broken runic chains that float around it. "
                          "Its face is hidden beneath an imperial mask, engraved with the Vaelthorne crest, but cracks in it's body reveal shifting eyes underneath.")
        c.set_defensive_stats(base_hp=25, defense=10, dodge=2, will=4, endurance=2)
        c.set_offensive_stats(speed=4, strength=3, dexterity=3, intelligence=4)
        c.set_profession(professions.enemy_profession("Astral Predator"))
        c.add_ability(abilities.basic_attack(2, 4))
        c.add_ability(abilities.astral_lightning())
        c.add_ability(abilities.runic_chains())
        c.set_ai(BasicAI(c))
        c.action_point_replenish = 3
        return c

    def new_bone_servitor(self):
        c = Creature("Bone Servitor", 3)
        c.set_sprite(CreatureSprite((60,48,12,12), (84,0,12,12)))
        c.set_description("A skeletal construct assembled with crude weapons and jagged bones.")
        c.set_defensive_stats(base_hp=16,defense=8,dodge=2,will=1,endurance=3)
        c.set_offensive_stats(speed=3, strength=3, dexterity=2, intelligence=2)
        c.set_profession(professions.enemy_profession("Servitor"))
        c.add_ability(abilities.basic_attack(2,4))
        c.add_ability(abilities.multi_attack(2,4))
        c.add_ability(abilities.bone_shield(5))
        c.set_ai(BasicAI(c))
        return c

    def new_gravebound_watcher(self):
        c = Creature("Gravebound Watcher", 3)
        c.set_sprite(CreatureSprite((72,48,12,12), (60,0,12,12)))
        c.set_description("A rotting figure with glowing eyes and remnants of priestly robes.")
        c.set_defensive_stats(base_hp=12,defense=12,dodge=2,will=4,endurance=2)
        c.set_offensive_stats(speed=4, strength=2, dexterity=3, intelligence=4)
        c.add_ability(abilities.elemental_attack(1, 3, 'dark', 'intelligence'))
        c.add_ability(abilities.hollow_gaze(1, 3, 30))
        c.add_ability(abilities.necrotic_chains(1, 3, 80))
        c.set_ai(BasicAI(c))
        return c

    def new_unhallowed_guardian(self):
        c = Creature("Unhallowed Guardian", 4)
        c.set_sprite(CreatureSprite((84,48,12,12), (96,0,12,12)))
        c.set_description("A massive undead knight, clad in ancient armor that bears the Vaelthorne Crest. Bound to the crypt to defend the Vaelthorne remains.")
        c.set_defensive_stats(base_hp=30, defense=14, dodge=2, will=5, endurance=4)
        c.set_offensive_stats(speed=3, strength=5, dexterity=3, intelligence=5)
        c.add_ability(abilities.basic_attack(2,4))
        c.add_ability(abilities.multi_attack(2,4))
        c.add_ability(abilities.greataxe_slash(2,4))
        c.add_ability(abilities.bone_shield(8))
        c.add_ability(abilities.soul_drain(1,2,2))
        c.action_point_replenish = 3
        c.set_ai(BasicAI(c))
        return c

    def new_bound_remnant_sword(self):
        c = Creature("Bound Remnant", 3)
        c.set_sprite(CreatureSprite((36,60,12,12), (12,0,12,12)))
        c.set_description("Cobbled together with sinew and mismatched bone, its torso wrapped in chains to hold it upright. "
                          "One arm ends in a jagged, rusted sword fused to the forearm, while the other clutches a battered shield of cracked iron. "
                          "Scraps of rotted leather dangle from its shoulders, as if mocking the memory of a warrior.")
        c.set_defensive_stats(base_hp=12, defense=12, dodge=2, will=1, endurance=2)
        c.set_offensive_stats(speed=3, strength=4, dexterity=2, intelligence=2)
        c.add_ability(abilities.basic_attack(1,3))
        c.add_ability(abilities.disarming_strike(1,3))
        c.add_ability(abilities.bone_shield(5))
        c.add_ability(abilities.multi_attack(1,3))
        c.set_ai(BasicAI(c))
        return c

    def new_bound_remnant_hammer(self):
        c = Creature("Bound Remnant", 3)
        c.set_sprite(CreatureSprite((48,60,12,12), (12,0,12,12)))
        c.set_description("Reinforced with iron rods piercing its limbs, giving it a hulking, unnatural stance. "
                          "It wields a crude warhammer, the head a block of rust-streaked stone lashed to a thick, splintering wooden shaft.")
        c.set_defensive_stats(base_hp=14, defense=12, dodge=2, will=1, endurance=2)
        c.set_offensive_stats(speed=3, strength=4, dexterity=2, intelligence=2)
        c.add_ability(abilities.basic_attack(1,3))
        c.add_ability(abilities.heavy_blow(1,3,70))
        c.add_ability(abilities.multi_attack(1,3))
        c.set_ai(BasicAI(c))
        return c

    def new_bound_remnant_axe(self):
        c = Creature("Bound Remnant", 3)
        c.set_sprite(CreatureSprite((60,60,12,12), (12,0,12,12)))
        c.set_description("a lopsided horror, its arms unevenly sized, with the larger one fused to a massive battle axe forged from jagged steel. "
                          "Its ribcage is exposed, with faintly glowing runes etched into the bone, pulsing with necrotic energy.")
        c.set_defensive_stats(base_hp=12, defense=14, dodge=2, will=1, endurance=2)
        c.set_offensive_stats(speed=3, strength=4, dexterity=2, intelligence=2)
        c.add_ability(abilities.basic_attack(1,3))
        c.add_ability(abilities.cleave(1,3,3))
        c.add_ability(abilities.multi_attack(1,3))
        c.set_ai(BasicAI(c))
        return c

    def new_soul_tethered_herald(self):
        c = Creature("Soul-Tethered Herald", 5)
        c.set_sprite(CreatureSprite((96,48,12,12), (60,12,12,12)))
        c.set_description("A twisted undead being that was once a priest or holy figure in life. "
                          "In death, it has become a conduit for the endless waves of necromantic energy that have corrupted the cemetery.")
        c.set_defensive_stats(base_hp=28, defense=24, dodge=3, will=4, endurance=6)
        c.set_offensive_stats(speed=4, strength=4, dexterity=2, intelligence=5)
        c.add_ability(abilities.elemental_attack(1, 3, 'dark', 'intelligence'))
        c.add_ability(abilities.dark_tether(1,3))
        c.add_ability(abilities.necrotic_wave(0,2,20))
        c.add_ability(abilities.unholy_summons())
        c.action_point_replenish = 4
        c.set_ai(BasicAI(c))
        return c

    def new_bandit_grunt_1(self):
        c = Creature("Bandit Grunt", 0)
        c.set_sprite(CreatureSprite((0,72,12,12),(72,12,12,12)))
        c.set_description("A burly brute with a chipped cudgel, his tunic still bearing the crest of a past employer.")
        c.set_defensive_stats(base_hp=6,defense=5,dodge=2,will=1,endurance=1)
        c.set_offensive_stats(speed=3,strength=3,dexterity=2,intelligence=1)
        c.add_ability(abilities.slow_attack(1,3))
        c.add_ability(abilities.basic_attack(-1,1))
        c.add_ability(abilities.bolster(1, 4))
        c.set_ai(BasicAI(c))
        return c

    def new_bandit_grunt_2(self):
        c = Creature("Bandit Grunt", 0)
        c.set_sprite(CreatureSprite((12,72,12,12),(72,12,12,12)))
        c.set_description("A ragged swordsman with mismatched armor, more used to shaking down travelers than actual combat.")
        c.set_defensive_stats(base_hp=6,defense=7,dodge=2,will=1,endurance=1)
        c.set_offensive_stats(speed=3,strength=3,dexterity=2,intelligence=1)
        c.add_ability(abilities.slow_attack(1,3))
        c.add_ability(abilities.basic_attack(-1,1))
        c.add_ability(abilities.bolster(1, 4))
        c.set_ai(BasicAI(c))
        return c

    def new_harold(self):
        harold = Creature("Harold", 1)
        harold.set_sprite(CreatureSprite((0,84,12,12), (48,0,12,12)))
        harold.set_defensive_stats(base_hp=5, defense=4, dodge=1, will=2, endurance=1)
        harold.set_resistances(physical=20)
        harold.set_offensive_stats(speed=1, strength=4, dexterity=1, intelligence=1)
        harold.add_ability(abilities.basic_attack(1, 3))
        harold.set_ai(BasicAI(harold))
        return harold

    def new_elder_varik(self):
        varik = NPC("Elder Varik", 0)
        varik.set_sprite(CreatureSprite((12,60,12,12), None))
        varik.dialog_function = elder_varik_dialog
        return varik

    def new_gorren(self):
        gorren = NPC("Gorren", 1)
        gorren.set_sprite(CreatureSprite(-1, (0,0,12,12)))
        gorren.set_description("A wiry, pale-skinned young man who looks as though he hasn't seen sunlight in years. "
                               "A faint aura of cold seems to cling to him, as if the magic he wields has leeched warmth from his very being.")
        gorren.set_defensive_stats(base_hp=7, defense=0, dodge=2, will=3, endurance=1)
        gorren.set_offensive_stats(speed=3, strength=2, dexterity=2, intelligence=2)
        gorren.equip_item(items.new_staff())
        gorren.equip_item(items.new_robe())
        gorren.set_profession(professions.soulwarden())
        gorren.hp = gorren.max_hp()
        gorren.allied = True
        level_handler.add_creature(gorren)
        return gorren

    def new_rangu(self):
        rangu = Creature("Rangu", 1)
        rangu.set_sprite(CreatureSprite(-1, (0,0,12,12)))
        rangu.set_description("Wrapped in a weathered cloak, Rangu's presence is both imposing and effortless. "
                              "His twin hunting knives rest at his hips, and a musky scent of charred wood clings to him—like a fire that never fully goes out.")
        rangu.set_defensive_stats(base_hp=8, defense=0, dodge=3, will=2, endurance=2)
        rangu.set_offensive_stats(speed=4, strength=2, dexterity=2, intelligence=2)
        rangu.equip_item(items.new_shortbow())
        rangu.equip_item(items.new_leather_armor())
        rangu.set_profession(professions.ashen_stalker())
        rangu.hp = rangu.max_hp()
        rangu.allied = True
        level_handler.add_creature(rangu)
        return rangu
