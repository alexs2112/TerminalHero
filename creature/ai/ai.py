class AI:
    def __init__(self, creature):
        self.creature = creature

    def take_turn(self, player, encounter):
        pass

    def list_usable_abilities(self):
        return [ a for a in self.creature.abilities if a.is_usable() ]

    def list_alive_creatures(self, creatures):
        return [ c for c in creatures if c.is_alive() ]
