from dialog.dialog_parser import load_dialog
from main.player_log import get_player_log
player_log = get_player_log()

def test_dialog():
    return load_dialog('resources/dialog/test.json')['base_node']

def elder_varik_dialog():
    if player_log['met_elder_varik']:
        return load_dialog('resources/dialog/elder_varik.json')['start']
    return load_dialog('resources/dialog/elder_varik.json')['first_contact']

def gorren_initial_meeting():
    if player_log['defeat_cemetery_church_ambush']:
        return load_dialog('resources/dialog/gorren_initial_meeting.json')['defeated_ambush']
    return load_dialog('resources/dialog/gorren_initial_meeting.json')['start']

def vaelthorne_rune_pillar():
    return load_dialog('resources/dialog/vaelthorne_rune_pillar.json')['start']

def vaelthorne_crypt_entrance():
    return load_dialog('resources/dialog/vaelthorne_crypt_entrance.json')['start']

def doran_dialogue():
    return load_dialog('resources/dialog/doran_the_red.json')['start']
