from main.colour import WHITE

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
    def combine(self, creature, other_effect):
        pass

    # Triggered when the attacker calculates weapon damage while this effect is active
    def modify_base_damage(self, target, damage):
        # Modify damage in place
        pass

    # Triggered when the target calculates total damage while this effect is active
    def modify_total_damage(self, attacker, damage):
        # Modify damage in place
        pass
