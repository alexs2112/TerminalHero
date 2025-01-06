from world.encounter import Encounter
from creature.creature_factory import get_creature_factory
from main.player_log import get_player_log, update_log
player_log = get_player_log()
creature_factory = get_creature_factory()

# pylint: disable=invalid-name
_encounter_factory = None
def get_encounter_factory():
    global _encounter_factory
    if not _encounter_factory:
        _encounter_factory = EncounterFactory()
    return _encounter_factory

class EncounterFactory:
    def get_cemetery_encounter_1(self):
        e = Encounter("Attack Patchwork Dead")
        e.enemies = [
            creature_factory.new_patchwork_dead_1(),
            creature_factory.new_patchwork_dead_3()
        ]
        e.valid_condition = 'accepted_sidequest_1'
        def complete(player, area):
            area.npcs.append(creature_factory.new_gorren())
            update_log('clear_cemetery_1', player)
        e.completed_function = complete
        return e

    def get_cemetery_encounter_2(self):
        e = Encounter("Attack Patchwork Dead")
        e.enemies = [
            creature_factory.new_patchwork_dead_1(),
            creature_factory.new_patchwork_dead_2(),
            creature_factory.new_patchwork_dead_3()
        ]
        e.valid_condition = 'met_gorren'
        def complete(player, _):
            update_log('clear_cemetery_2', player)
        e.completed_function = complete
        e.block_exit = True
        return e
