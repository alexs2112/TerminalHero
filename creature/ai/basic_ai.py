from random import choice
from creature.ai.ai import AI

class BasicAI(AI):
    def take_turn(self, player, area):
        target = choice(self.list_alive_creatures(player.party))
        abilities = self.list_usable_abilities()
        if abilities and target:
            ability = choice(abilities)
            self.creature.use_ability(ability, target, area)
