from creature.ai.ai import AI

class BasicAI(AI):
    def take_turn(self, area):
        if area.player.is_alive():
            self.creature.attack(area.player)
        elif len(area.allies) > 0:
            self.creature.attack(area.allies[0])
