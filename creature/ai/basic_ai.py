from random import choice
from creature.ai.ai import AI

class BasicAI(AI):
    def take_turn(self, player, area):
        if len(player.party) > 0:
            target = player.party[0]
            abilities = self.list_usable_abilities()
            if abilities:
                ability = choice(abilities)
                self.creature.use_ability(ability, target)
