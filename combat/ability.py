class Ability:
    def __init__(self, name: str, cooldown: int, size: int = 1):
        self.name = name
        self.max_cooldown = cooldown
        self.cooldown = 0
        self.size = size
        self.description = ""

        # Bool function that is called to see if the ability hits a target
        self.to_hit = None

        # Function effect called when the ability is used
        self.effect = None

    def set_description(self, desc: str):
        self.description = desc

    def set_to_hit(self, bool_function):
        self.to_hit = bool_function

    def set_effect(self, effect_function):
        self.effect = effect_function

    def success(self, creature, target, area):
        return self.to_hit(creature, target, area)

    def apply(self, creature, target, area):
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
