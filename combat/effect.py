from main.constants import WHITE

class Effect:
    def __init__(self, name: str, duration: int, colour = WHITE):
        self.name = name
        self.duration = duration
        self.colour = colour

        # Functions that are triggered by this status effect
        self.effect_start_function = None
        self.effect_turn_function = None
        self.effect_end_function = None

    def set_effect_start(self, func):
        self.effect_start_function = func
    def set_effect_turn(self, func):
        self.effect_turn_function = func
    def set_effect_end(self, func):
        self.effect_end_function = func

    def effect_start(self, creature):
        if self.effect_start_function:
            self.effect_start_function(creature)

    def effect_turn(self, creature):
        if self.effect_turn_function:
            self.effect_turn_function(creature)
        self.duration -= 1

    def effect_end(self, creature):
        if self.effect_end_function:
            self.effect_end_function(creature)
