class Ability:
    def __init__(self, name: str, cooldown: int, cost: int = 2):
        self.name = name
        self.max_cooldown = cooldown
        self.cooldown = 0
        self.description = ""
        self.action_points = cost

        # Function effect called when the ability is used
        self.effect = None

        # Function to be called to check if a creature can be targeted
        self.can_target_func = None

        # Function to be called to determine target priorities
        self.target_priority_func = None

        # How the ability scales damage off of the stats of the user (as a decimal)
        self.scaling = None

    def set_description(self, desc: str):
        self.description = desc

    def set_effect(self, effect_function):
        self.effect = effect_function

    def activate(self, creature, target, area):
        creature.action_points -= self.action_points
        return self.effect(creature, target, area)

    def set_cooldown(self):
        self.cooldown = self.max_cooldown

    def is_usable(self, creature):
        return self.cooldown == 0 and creature.action_points >= self.action_points

    def get_short_desc(self):
        s = self.name
        s += f" (cost={self.action_points})"
        if self.cooldown > 0:
            s += f" ({self.cooldown})"
        return s

    def can_target(self, creature, other):
        if self.can_target_func:
            return self.can_target_func(creature, other)
        return other.is_alive()

    def set_can_target(self, func):
        self.can_target_func = func

    def set_target_priority(self, func):
        self.target_priority_func = func

    def get_target_priorities(self, creature, player, encounter):
        if not self.target_priority_func:
            return []
        return self.target_priority_func(self, creature, player, encounter)

    def set_scaling(self, scaling):
        self.scaling = scaling

    def scale_damage(self, damage, creature):
        for s, v in self.scaling.items():
            damage.add_damage(int(creature.stat(s) * v * 7))
        return damage
