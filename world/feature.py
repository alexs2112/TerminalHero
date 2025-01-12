from main.colour import *

# Feature Types
FEATURE = 'Feature'
CHEST = 'Chest'
DIALOG = 'Dialog'

class Feature:
    def __init__(self, name):
        self.name = name
        self.type = FEATURE
        self.enabled_function = None

    def set_enabled_function(self, function):
        self.enabled_function = function

    # Potentially useful later
    def enabled(self):
        if self.enabled_function:
            return self.enabled_function()
        return True

# Currently not implemented
class ChestFeature(Feature):
    def __init__(self, name):
        super().__init__(name)
        self.type = CHEST
        self.inventory = []
        # Set this chest as locked until requirement is met?

    def set_inventory(self, inventory):
        self.inventory = inventory

class DialogFeature(Feature):
    def __init__(self, name):
        super().__init__(name)
        self.type = DIALOG
        self.dialog_function = None

    def set_dialog_function(self, dialog_function):
        self.dialog_function = dialog_function

    def get_dialog_node(self):
        return self.dialog_function()
