from world.encounter import Encounter
from creature.creature_factory import get_creature_factory
from item.item_factory import get_item_factory
from main.messenger import get_messenger
from main.player_log import get_player_log, update_log
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
        e = Encounter("Attack Patchwork Dead")
        e.add_enemies(
            creature_factory.new_patchwork_dead_1(),
            creature_factory.new_patchwork_dead_2()
        )
        e.invalid_condition = 'finish_cemetery_stage_1'
        e.reward_xp = 200
        e.block_exit = True
        return e
    def cemetery_first_stage_2(self):
        e = Encounter("Attack Patchwork Dead")
        e.add_enemies(
            creature_factory.new_patchwork_dead_1(),
            creature_factory.new_patchwork_dead_2(),
            creature_factory.new_patchwork_dead_3()
        )
        e.invalid_condition = 'finish_cemetery_stage_1'
        e.reward_xp = 300
        e.block_exit = True
        return e

    # Cemetery - Second Stage
    def cemetery_second_stage_ambush(self):
        e = Encounter("Undead Ambush")
        e.add_enemies(
            creature_factory.new_patchwork_dead_2(),
            creature_factory.new_lanternbearer(),
            creature_factory.new_patchwork_dead_3()
        )
        e.valid_condition = 'finish_cemetery_stage_1'
        def complete(*_):
            update_log('defeat_cemetery_church_ambush')
        e.set_completed_function(complete)
        e.reward_xp = 350
        e.block_exit = True
        return e
    def cemetery_second_stage_1(self):
        e = Encounter("Attack Undead")
        e.add_enemies(
            creature_factory.new_patchwork_dead_1(),
            creature_factory.new_rotten_stray(),
            creature_factory.new_lanternbearer()
        )
        e.valid_condition = 'finish_cemetery_stage_1'
        e.invalid_condition = 'finish_cemetery_stage_2'
        e.reward_xp = 350
        e.block_exit = True
        return e
    def cemetery_second_stage_2(self):
        e = Encounter("Attack Rotten Strays")
        e.add_enemies(
            creature_factory.new_rotten_stray(),
            creature_factory.new_rotten_stray(),
            creature_factory.new_rotten_stray()
        )
        e.valid_condition = 'finish_cemetery_stage_1'
        e.invalid_condition = 'finish_cemetery_stage_2'
        e.reward_xp = 350
        e.block_exit = True
        return e

    # Vaelthorne Shrine
    def runebound_stalker(self):
        e = Encounter("Attack Runebound Stalker")
        e.add_enemies(
            creature_factory.new_runebound_stalker()
        )
        e.valid_condition = 'shrine_opened'
        e.block_exit = True
        def complete(player, _):
            update_log('runebound_stalker_defeated', player)
        e.set_completed_function(complete)
        e.reward_items = [ item_factory.new_vaelthorne_seal() ]
        e.reward_xp = 400
        return e

    # Vaelthorne Crypt
    def get_crypt_encounter_1(self):
        e = Encounter("Attack Bone Servitors")
        e.add_enemies(
            creature_factory.new_patchwork_dead_1(),
            creature_factory.new_bone_servitor(),
            creature_factory.new_bone_servitor()
        )
        e.block_exit = True
        e.reward_xp = 500
        return e
    def get_crypt_encounter_2(self):
        e = Encounter("Attack Gravebound Watchers")
        e.add_enemies(
            creature_factory.new_gravebound_watcher(),
            creature_factory.new_gravebound_watcher()
        )
        e.block_exit = True
        e.reward_xp = 500
        return e
    def get_crypt_encounter_3(self):
        e = Encounter("Attack Unhallowed Guardian")
        e.add_enemies(
            creature_factory.new_unhallowed_guardian(),
            creature_factory.new_gravebound_watcher()
        )
        def complete(player, _):
            update_log('unhallowed_guardian_defeated', player)
            messenger.add("The :BLUEVIOLET:Unhallowed Guardian:BLUEVIOLET: collapses into a pillar of :LIGHTGRAY:Salt:LIGHTGRAY:. "
                          "you feel another dark pulse of :BLUEVIOLET:Necromantic Energy:BLUEVIOLET: "
                          "rock the crypt around you.")
        e.set_completed_function(complete)
        e.reward_items = [ item_factory.new_obsidian_lantern() ]
        e.block_exit = True
        e.reward_xp = 800
        return e
