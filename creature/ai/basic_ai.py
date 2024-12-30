from creature.ai.ai import AI

class BasicAI(AI):
    def take_turn(self, allies, _):
        # Attack the first ally
        if len(allies) > 0:
            # This should never not be the case?
            self.creature.attack(allies[0])
