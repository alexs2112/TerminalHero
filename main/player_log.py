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
        'known_corpse_pile': False,
        'known_bloodstone_mine': False,
        'known_starvation_pit': False,
        'known_garrison': False
    }
