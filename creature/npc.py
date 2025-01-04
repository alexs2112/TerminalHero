from creature.creature import Creature
from dialog.dialog_parser import load_dialog
from main.player_log import get_player_log
player_log = get_player_log()

def elder_varik_dialog():
    if player_log['met_elder_varik']:
        return load_dialog('resources/dialog/elder_varik.json')['root_node']
    return load_dialog('resources/dialog/elder_varik.json')['initial_node']

def gorren_dialogue():
    if not player_log['clear_cemetery_1']:
        return load_dialog('resources/dialog/gorren_questline.json')['start']

    # TODO: Add more dialogue here lol
    return load_dialog('resources/dialog/gorren_questline.json')['start']

class NPC(Creature):
    def set_dialog_func(self, dialog_function):
        self.dialog_function = dialog_function

    def has_dialog(self):
        return self.dialog_function is not None

    def get_dialog_node(self):
        # The results of this should be stored somewhere for cases where this
        # gets called multiple times
        # Could be tricky with branching dialogue functions
        return self.dialog_function()
