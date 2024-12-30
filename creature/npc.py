from creature.creature import Creature
from dialog.dialog_parser import load_dialog

def elder_varik_dialog():
    return load_dialog('resources/dialog/elder_varik.json')['root_node']

class NPC(Creature):
    def set_dialog_func(self, dialog_function):
        self.dialog_function = dialog_function

    def has_dialog(self):
        return self.dialog_function is not None

    def get_dialog_node(self):
        return self.dialog_function()
