# pylint: disable=invalid-name
_player_log = None
def get_player_log():
    global _player_log
    if not _player_log:
        _player_log = initialize_player_log()
    return _player_log

def initialize_player_log():
    return {
        'met_elder_varik': False,
        'known_cemetery': False,
        'known_bloodstone_mine': False,
        'known_starvation_pit': False,
        'known_garrison': False,
        'accepted_sidequest_1': False,
        'visit_cemetery': False,
        'clear_cemetery_1': False,
        'met_gorren': False
    }

def update_log(field, player=None):
    player_log = get_player_log()
    if field in player_log:
        player_log[field] = True
    if player:
        for q in player.get_quests():
            q.check_completion()
            q.debug_print()
