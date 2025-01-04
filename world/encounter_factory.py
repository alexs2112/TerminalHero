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
            self.creature_factory.new_rotfang_widow(),
            self.creature_factory.new_bonechewer_beetle(),
            self.creature_factory.new_deathburrower()
        ]
        e.valid_condition = 'accepted_sidequest_1'
        def complete(player, area):
            area.npcs.append(self.creature_factory.new_gorren())
            update_log('clear_cemetery_1', player)
        e.completed_function = complete
        return e
