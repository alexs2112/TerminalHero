from random import shuffle
from creature.ai.ai import AI

class BasicAI(AI):
    def take_turn(self, player, area):
        abilities = self.list_usable_abilities()
        priorities = []
        for a in abilities:
            priorities += a.get_target_priorities(self.creature, player, area.get_encounter())

        if not priorities:
            return

        # Shuffle the priorities, then sort them by priority to get a random of the highest priority abilities
        shuffle(priorities)
        priorities.sort(key=lambda p: p.priority)

        p = priorities.pop()
        self.creature.use_ability(p.ability, p.target, area)
