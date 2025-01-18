class Ability:
    def __init__(self, name: str, cooldown: int, size: int = 1):
        self.name = name
        self.max_cooldown = cooldown
        self.cooldown = 0
        self.size = size
        self.description = ""

        # Function effect called when the ability is used
        self.effect = None

        # Function to be called to check if a creature can be targeted
        self.can_target_func = None

    def set_description(self, desc: str):
        self.description = desc

    def set_effect(self, effect_function):
        self.effect = effect_function

    def activate(self, creature, target, area):
        return self.effect(creature, target, area)

    def set_cooldown(self):
        self.cooldown = self.max_cooldown

    def is_usable(self):
        return self.cooldown == 0

    def get_short_desc(self):
        s = self.name
        if self.cooldown > 0:
            s += f" ({self.cooldown})"
        return s

    def can_target(self, creature):
        if self.can_target_func:
            return self.can_target_func(creature)
        return creature.is_alive()

    def set_can_target(self, func):
        self.can_target_func = func
