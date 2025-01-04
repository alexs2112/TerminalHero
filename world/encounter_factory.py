from world.encounter import Encounter
from creature.creature_factory import CreatureFactory
from main.player_log import get_player_log, update_log
player_log = get_player_log()

class EncounterFactory:
    def __init__(self):
        self.creature_factory = CreatureFactory()

    def get_cemetery_encounter_1(self):
        e = Encounter("Attack Patchwork Dead")
        e.enemies = [
            self.creature_factory.new_patchwork_dead_1(),
            self.creature_factory.new_patchwork_dead_3()
        ]
        e.valid_condition = 'accepted_sidequest_1'
        def complete(player, area):
            area.npcs.append(self.creature_factory.new_gorren())
            update_log('clear_cemetery_1', player)
        e.completed_function = complete
        return e

    def get_cemetery_encounter_2(self):
        e = Encounter("Attack Patchwork Dead")
        e.enemies = [
            self.creature_factory.new_patchwork_dead_1(),
            self.creature_factory.new_patchwork_dead_2(),
            self.creature_factory.new_patchwork_dead_3()
        ]
        e.valid_condition = 'met_gorren'
        def complete(player, _):
            update_log('clear_cemetery_2', player)
        e.completed_function = complete
        e.block_exit = True
        return e
