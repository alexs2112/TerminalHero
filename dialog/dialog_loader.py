from dialog.dialog_parser import load_dialog
from main.player_log import get_player_log
player_log = get_player_log()

def test_dialog():
    return load_dialog('resources/dialog/test.json')['base_node']

def elder_varik_dialog():
    if player_log['met_elder_varik']:
        return load_dialog('resources/dialog/elder_varik.json')['start']
    return load_dialog('resources/dialog/elder_varik.json')['first_contact']

def gorren_dialogue():
    if not player_log['clear_cemetery_1']:
        return load_dialog('resources/dialog/gorren_questline.json')['start']
    elif player_log['met_gorren'] and not player_log['clear_cemetery_2']:
        return load_dialog('resources/dialog/gorren_questline.json')['pre_combat']
    elif player_log['clear_cemetery_2']:
        return load_dialog('resources/dialog/gorren_questline.json')['post_combat']

    # Add default dialogue once he is in your party
    return load_dialog('resources/dialog/gorren_questline.json')['start']

def vaelthorne_rune_pillar():
    return load_dialog('resources/dialog/vaelthorne_rune_pillar.json')['start']

def vaelthorne_crypt_entrance():
    return load_dialog('resources/dialog/vaelthorne_crypt_entrance.json')['start']

def doran_dialogue():
    return load_dialog('resources/dialog/doran_the_red.json')['start']
