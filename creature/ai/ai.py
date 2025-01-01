class AI:
    def __init__(self, creature):
        self.creature = creature

    def take_turn(self, player, area):
        pass

    def list_usable_abilities(self):
        return [ a for a in self.creature.abilities if a.is_usable() ]
