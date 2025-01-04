from random import choice
from creature.ai.ai import AI

class BasicAI(AI):
    def take_turn(self, player, encounter):
        if len(player.party) > 0:
            target = choice(player.party)
            abilities = self.list_usable_abilities()
            if abilities:
                ability = choice(abilities)
                self.creature.use_ability(ability, target)
