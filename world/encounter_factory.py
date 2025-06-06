from random import shuffle
from world.encounter import Encounter
from creature.creature_factory import get_creature_factory
from item.item_factory import get_item_factory
from main.messenger import get_messenger
from main.player_log import get_player_log, update_log
from main.notification import add_notification
messenger = get_messenger()
player_log = get_player_log()
creature_factory = get_creature_factory()
item_factory = get_item_factory()

# pylint: disable=invalid-name
_encounter_factory = None
def get_encounter_factory():
    global _encounter_factory
    if not _encounter_factory:
        _encounter_factory = EncounterFactory()
    return _encounter_factory

class EncounterFactory:
    # Cemetery - First Stage
    def cemetery_first_stage_1(self):
        e = Encounter('cemetery_1_1', "Attack Patchwork Dead")
        e.set_enemy_functions(
            creature_factory.new_patchwork_dead_1,
            creature_factory.new_patchwork_dead_2
        )
        e.invalid_condition = 'finish_cemetery_stage_1'
        e.reward_xp = 200
        e.block_exit = True
        return e
    def cemetery_first_stage_2(self):
        e = Encounter('cemetery_1_2', "Attack Patchwork Dead")
        e.set_enemy_functions(
            creature_factory.new_patchwork_dead_1,
            creature_factory.new_patchwork_dead_2,
            creature_factory.new_patchwork_dead_3
        )
        e.invalid_condition = 'finish_cemetery_stage_1'
        e.reward_xp = 300
        e.block_exit = True
        return e

    # Cemetery - Second Stage
    def cemetery_second_stage_ambush(self):
        e = Encounter('cemetery_2_0', "Undead Ambush")
        e.set_enemy_functions(
            creature_factory.new_patchwork_dead_2,
            creature_factory.new_lanternbearer,
            creature_factory.new_patchwork_dead_3
        )
        e.valid_condition = 'finish_cemetery_stage_1'
        def complete(*_):
            update_log('defeat_cemetery_church_ambush')
        e.set_completed_function(complete)
        e.reward_xp = 350
        e.block_exit = True
        return e
    def cemetery_second_stage_1(self):
        e = Encounter('cemetery_2_1', "Attack Undead")
        e.set_enemy_functions(
            creature_factory.new_patchwork_dead_1,
            creature_factory.new_rotten_stray,
            creature_factory.new_lanternbearer
        )
        shuffle(e.enemies)
        e.valid_condition = 'finish_cemetery_stage_1'
        e.invalid_condition = 'finish_cemetery_stage_2'
        e.reward_xp = 350
        e.block_exit = True
        return e
    def cemetery_second_stage_2(self):
        e = Encounter('cemetery_2_2', "Attack Rotten Strays")
        e.set_enemy_functions(
            creature_factory.new_rotten_stray,
            creature_factory.new_rotten_stray,
            creature_factory.new_rotten_stray
        )
        e.valid_condition = 'finish_cemetery_stage_1'
        e.invalid_condition = 'finish_cemetery_stage_2'
        e.reward_xp = 350
        e.block_exit = True
        return e

    # Vaelthorne Shrine
    def runebound_stalker(self):
        e = Encounter('shrine_runebound_stalker', "Attack Runebound Stalker")
        e.set_enemy_functions(
            creature_factory.new_runebound_stalker
        )
        e.valid_condition = 'shrine_opened'
        e.block_exit = True
        def complete(*_):
            update_log('runebound_stalker_defeated')
        e.set_completed_function(complete)
        e.reward_items = [ item_factory.new_vaelthorne_seal() ]
        e.reward_xp = 400
        return e

    # Vaelthorne Crypt
    def get_crypt_encounter_1(self):
        e = Encounter('crypt_1', "Attack Bone Servitors")
        e.set_enemy_functions(
            creature_factory.new_patchwork_dead_1,
            creature_factory.new_bone_servitor,
            creature_factory.new_bone_servitor
        )
        shuffle(e.enemies)
        e.block_exit = True
        e.reward_xp = 500
        return e
    def get_crypt_encounter_2(self):
        e = Encounter('crypt_2', "Attack Gravebound Watchers")
        e.set_enemy_functions(
            creature_factory.new_gravebound_watcher,
            creature_factory.new_gravebound_watcher
        )
        e.block_exit = True
        e.reward_xp = 500
        return e
    def get_crypt_encounter_3(self):
        e = Encounter('crypt_3', "Attack Unhallowed Guardian")
        e.set_enemy_functions(
            creature_factory.new_unhallowed_guardian,
            creature_factory.new_gravebound_watcher
        )
        def complete(*_):
            update_log('unhallowed_guardian_defeated')
            update_log('finish_cemetery_stage_2')
            add_notification(
                ["The :BLUEVIOLET:Unhallowed Guardian:BLUEVIOLET: collapses into a pillar of :LIGHTGRAY:Salt:LIGHTGRAY:. "
                "you feel another dark pulse of :BLUEVIOLET:Necromantic Energy:BLUEVIOLET: "
                "rock the crypt around you.",
                "The :CYAN:Cemetery:CYAN: is now a dungeon instance!"]
            )
        e.set_completed_function(complete)
        e.reward_items = [ item_factory.new_obsidian_lantern() ]
        e.block_exit = True
        e.reward_xp = 800
        return e

    # Cemetery - Third Stage
    def cemetery_third_stage_1(self):
        e = Encounter('cemetery_3_1', "Attack Bound Remnants")
        e.set_enemy_functions(
            creature_factory.new_bound_remnant_sword,
            creature_factory.new_bound_remnant_hammer,
            creature_factory.new_bound_remnant_axe
        )
        shuffle(e.enemies)
        e.block_exit = True
        e.reward_xp = 450
        e.valid_condition = 'finish_cemetery_stage_2'
        e.invalid_condition = 'finish_cemetery_stage_3'
        return e

    def cemetery_third_stage_2(self):
        e = Encounter('cemetery_3_2', "Attack Rotten Strays")
        e.set_enemy_functions(
            creature_factory.new_rotten_stray,
            creature_factory.new_rotten_stray,
            creature_factory.new_rotten_stray,
            creature_factory.new_rotten_stray
        )
        e.block_exit = True
        e.reward_xp = 550
        e.valid_condition = 'finish_cemetery_stage_2'
        e.invalid_condition = 'finish_cemetery_stage_3'
        return e

    def cemetery_third_stage_3(self):
        e = Encounter('cemetery_3_3', "Attack Bound Remnants")
        e.set_enemy_functions(
            creature_factory.new_bound_remnant_sword,
            creature_factory.new_bound_remnant_sword,
            creature_factory.new_bound_remnant_hammer,
            creature_factory.new_bound_remnant_axe
        )
        shuffle(e.enemies)
        e.block_exit = True
        e.reward_xp = 450
        e.valid_condition = 'finish_cemetery_stage_2'
        e.invalid_condition = 'finish_cemetery_stage_3'
        def complete(*_):
            update_log('banishment_ritual_can_start')
        e.set_completed_function(complete)
        return e

    def soul_tethered_herald(self):
        e = Encounter('cemetery_soul_tethered_herald', "Soul-Tethered Herald")
        e.set_enemy_functions(
            creature_factory.new_soul_tethered_herald
        )
        e.block_exit = True
        e.reward_xp = 800
        e.valid_condition = 'gorren_ritual_interrupted'
        def complete(*_):
            update_log('soul_tethered_herald_defeated')
        e.set_completed_function(complete)
        return e

    # Caravan Wreckage
    def caravan_wreckage_1(self):
        e = Encounter('caravan_wreckage_1', "Attack Bandits")
        e.set_enemy_functions(
            creature_factory.new_bandit_grunt_1,
            creature_factory.new_bandit_grunt_2
        )
        e.block_exit = True
        e.reward_xp = 200
        return e

    def caravan_wreckage_2(self):
        e = Encounter('caravan_wreckage_2', "Attack Bandits")
        e.set_enemy_functions(
            creature_factory.new_bandit_grunt_1,
            creature_factory.new_bandit_grunt_2,
            creature_factory.new_bandit_grunt_1
        )
        e.block_exit = True
        e.reward_xp = 300
        return e

    # Bandit Camp
    def bandit_camp_failed_sneak(self):
        e = Encounter('bandit_camp_failed_sneak', "Attack Bandits")
        e.valid_condition = 'bandit_camp_sneak_failed' # Note this is different than the ID
        e.set_enemy_functions(
            creature_factory.new_bandit_grunt_1,
            creature_factory.new_bandit_cutthroat
        )
        e.block_exit = True
        e.reward_xp = 300
        return e

    def bandit_camp_watchtower_default(self):
        e = Encounter('bandit_camp_watchtower_default', "Attack Bandits")
        e.invalid_condition = 'bandit_camp_assassination'
        e.set_enemy_functions(
            creature_factory.new_bandit_grunt_1,
            creature_factory.new_bandit_grunt_2,
            creature_factory.new_bandit_raider
        )
        e.block_exit = True
        e.reward_xp = 450
        return e

    def bandit_camp_watchtower_small(self):
        e = Encounter('bandit_camp_watchtower_small', "Attack Bandits")
        e.valid_condition = 'bandit_camp_assassination'
        e.set_enemy_functions(
            creature_factory.new_bandit_grunt_2,
            creature_factory.new_bandit_raider
        )
        e.block_exit = True
        e.reward_xp = 450
        return e

    def bandit_camp_pool(self):
        e = Encounter('bandit_camp_pool', "Attack Bandits")
        e.set_enemy_functions(
            creature_factory.new_bandit_cutthroat,
            creature_factory.new_bandit_cutthroat
        )
        e.block_exit = True
        e.reward_xp = 400
        return e

    def bandit_camp_fire_default(self):
        e = Encounter('bandit_camp_fire_default', "Attack Bandits")
        e.invalid_condition = 'bandit_camp_assassination'
        e.set_enemy_functions(
            creature_factory.new_bandit_grunt_1,
            creature_factory.new_bandit_cutthroat,
            creature_factory.new_lesser_black_flame_elemental
        )
        e.block_exit = True
        e.reward_xp = 550
        return e

    def bandit_camp_fire_small(self):
        e = Encounter('bandit_camp_fire_small', "Attack Bandits")
        e.valid_condition = 'bandit_camp_assassination'
        e.set_enemy_functions(
            creature_factory.new_bandit_grunt_1,
            creature_factory.new_lesser_black_flame_elemental
        )
        e.block_exit = True
        e.reward_xp = 550
        return e

    def bandit_camp_boss(self):
        e = Encounter('bandit_camp_boss', "Attack Bandits")
        e.set_enemy_functions(
            creature_factory.new_bandit_cutthroat,
            creature_factory.new_bandit_grunt_2,
            creature_factory.new_bandit_raider_elite
        )
        e.block_exit = True
        e.reward_xp = 700
        return e
