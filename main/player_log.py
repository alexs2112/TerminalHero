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
        'known_shrine': False,

        'tavern_open': False,
        'tavern_room_unlocked': False,
        'tavern_store_unlocked': False,

        # Grave Concerns Questline
        'accepted_grave_concerns': False,
        'visit_cemetery': False,
        'finish_cemetery_stage_1': False,       # Finished when the player talks to Gorren for the first time
        'defeat_cemetery_church_ambush': False,
        'gorren_leaves_church': False,
        'finish_cemetery_stage_2': False,       # Finished then the player clears the Vaelthorne Crypt
        'visit_crypt': False,
        'visit_shrine': False,
        'shrine_opened': False,
        'runebound_stalker_defeated': False,    # Vaelthorne Seal Acquired
        'crypt_unlocked': False,
        'unhallowed_guardian_defeated': False,  # Obsidian Lantern Acquired

        # Food Related Logs
        'food_mushroom': False,
        'food_carrot': False,
        'food_steak': False,
        'food_cheese': False,
    }

def update_log(field, player=None):
    player_log = get_player_log()
    if field in player_log:
        player_log[field] = True
    if player:
        for q in player.get_quests():
            q.check_completion()
            if q.complete:
                player.quests.remove(q)
                player.done_quests.append(q)
