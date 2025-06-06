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
        'known_caravan_wreckage': False,
        'known_bandit_camp': False,

        'tavern_open': False,
        'tavern_room_unlocked': False,
        'tavern_store_unlocked': False,

        # Grave Concerns Questline
        'accepted_grave_concerns': False,
        'visit_cemetery': False,
        'finish_cemetery_stage_1': False,       # Finished when the player talks to Gorren for the first time
        'defeat_cemetery_church_ambush': False,
        'gorren_leaves_church': False,
        'finish_cemetery_stage_2': False,       # Finished when the player clears the Vaelthorne Crypt
        'visit_crypt': False,
        'visit_shrine': False,
        'shrine_opened': False,
        'runebound_stalker_defeated': False,    # Vaelthorne Seal Acquired
        'crypt_unlocked': False,
        'unhallowed_guardian_defeated': False,  # Obsidian Lantern Acquired
        'banishment_ritual_can_start': False,
        'gorren_ritual_interrupted': False,
        'soul_tethered_herald_defeated': False,
        'finish_cemetery_stage_3': False,       # Finished when the player completes the banishment ritual with Gorren

        # Scales and Spurs Questline
        'accepted_scales_spurs': False,
        'met_rangu': False,
        'visit_bandit_camp': False,
        'bandit_camp_sneak_attempted': False,
        'bandit_camp_sneak_failed': False,
        'bandit_camp_assassination': False,

        # Food Related Logs
        'food_mushroom': False,
        'food_carrot': False,
        'food_steak': False,
        'food_cheese': False,
    }

def update_log(field):
    # pylint: disable=import-outside-toplevel
    from quests.quest_handler import get_quest_handler
    player_log = get_player_log()
    quest_handler = get_quest_handler()
    player_log[field] = True
    for q in quest_handler.get():
        q.check_completion()
        if q.complete:
            quest_handler.mark_complete(q)
