from main.constants import WHITE

class Effect:
    def __init__(self, name: str, duration: int, colour = WHITE):
        self.name = name
        self.duration = duration
        self.colour = colour

    # Triggered when the effect is started on a creature
    def effect_start(self, creature):
        pass

    # Triggered at the beginning of that creature's turn
    def effect_turn(self, creature):
        pass

    # Triggered when the effect ends
    def effect_end(self, creature):
        pass

    # If the player is affected by another effect while this is active, trigger this
    # If return True, the other effect is not applied
    def combine(self, other_effect):
        pass
