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
        'met_gorren': False,
        'known_cemetery': False,
        'known_bloodstone_mine': False,
        'known_garrison': False,
        'known_tavern': False,
        'known_crypt': False,

        'tavern_open': False,       # Currently does nothing

        'accepted_grave_concerns': False,

        'visit_cemetery': False,
        'visit_crypt': False,

        'clear_cemetery_1': False,
        'clear_cemetery_2': False,
    }

def update_log(field, player=None):
    player_log = get_player_log()
    if field in player_log:
        player_log[field] = True
    if player:
        for q in player.get_quests():
            q.check_completion()
            if q.complete:
                if q in player.main_quests:
                    player.main_quests.remove(q)
                elif q in player.side_quests:
                    player.side_quests.remove(q)
                player.done_quests.append(q)
