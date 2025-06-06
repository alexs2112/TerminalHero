from dialog.dialog_parser import load_dialog
from main.player_log import get_player_log
player_log = get_player_log()

def test_dialog():
    return load_dialog('resources/dialog/test.json')['base_node']

def elder_varik_dialog():
    if player_log['met_elder_varik']:
        return load_dialog('resources/dialog/elder_varik.json')['start']
    return load_dialog('resources/dialog/elder_varik.json')['first_contact']

def doran_dialogue():
    return load_dialog('resources/dialog/doran_the_red.json')['start']

def gorren_initial_meeting():
    if player_log['defeat_cemetery_church_ambush']:
        return load_dialog('resources/dialog/gorren_initial_meeting.json')['defeated_ambush']
    return load_dialog('resources/dialog/gorren_initial_meeting.json')['start']

def vaelthorne_rune_pillar():
    return load_dialog('resources/dialog/vaelthorne_rune_pillar.json')['start']

def vaelthorne_crypt_entrance():
    return load_dialog('resources/dialog/vaelthorne_crypt_entrance.json')['start']

def gorren_banishment_ritual():
    if player_log['soul_tethered_herald_defeated']:
        return load_dialog('resources/dialog/gorren_banishment_ritual.json')['victory_start']
    return load_dialog('resources/dialog/gorren_banishment_ritual.json')['start']

def rangu_initial_meeting():
    return load_dialog('resources/dialog/rangu_initial_meeting.json')['start']

def rangu_tavern():
    return load_dialog('resources/dialog/rangu_tavern.json')['start']

def bandit_camp_sneak_check():
    return load_dialog('resources/dialog/bandit_camp_sneak_check.json')['start']
