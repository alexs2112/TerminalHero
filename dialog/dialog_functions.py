from main.player_log import get_player_log
from creature.player import Player
from quests.quest_factory import *
player_log = get_player_log()

def set_met_elder_varik(_):
    player_log['met_elder_varik'] = True

def set_known_cemetery(_):
    player_log['known_cemetery'] = True

def set_known_bloodstone_mine(_):
    player_log['known_bloodstone_mine'] = True

def set_known_starvation_pit(_):
    player_log['known_starvation_pit'] = True

def set_known_garrison(_):
    player_log['known_garrison'] = True

def add_quest_visit_corpse_pile(player: Player):
    player_log['accepted_sidequest_1'] = True
    player.side_quests.append(investigate_corpse_pile())
