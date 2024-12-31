from creature.ai.ai import AI

class BasicAI(AI):
    def take_turn(self, player, area):
        if len(player.party) > 0:
            self.creature.attack(player.party[0])
