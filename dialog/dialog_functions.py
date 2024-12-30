from main.player_log import get_player_log
player_log = get_player_log()

def set_met_elder_varik():
    player_log['met_elder_varik'] = True

def set_known_corpse_pile():
    player_log['known_corpse_pile'] = True

def set_known_bloodstone_mine():
    player_log['known_bloodstone_mine'] = True

def set_known_starvation_pit():
    player_log['known_starvation_pit'] = True

def set_known_garrison():
    player_log['known_garrison'] = True
