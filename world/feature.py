from main.colour import *

# Feature Types
FEATURE = 'Feature'
FUNCTION = 'Function'
CHEST = 'Chest'
DIALOG = 'Dialog'
AREA = 'Area'
FOOD_STORE = 'Food Store'

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

class FunctionFeature(Feature):
    def __init__(self, name):
        super().__init__(name)
        self.type = FUNCTION
        self.function_call = None

    def set_function(self, function):
        self.function_call = function

    def call_function(self, player, area):
        self.function_call(player, area)

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

class AreaFeature(Feature):
    def __init__(self, name, area):
        super().__init__(name)
        self.type = AREA
        self.area = area

class FoodStoreFeature(Feature):
    def __init__(self, name):
        super().__init__(name)
        self.type = FOOD_STORE
        self.store = None

    def set_store(self, store):
        self.store = store
