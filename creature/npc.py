from creature.creature import Creature

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
