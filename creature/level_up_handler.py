from main.notification import add_notification

# All companions should have the same level
MAX_LEVEL = 9
LEVEL_UP_BREAKPOINTS = [
    0,      # Level 1
    1000,   # Level 2

    # Temporary breakpoints
    2000,   # Level 3
    3000,   # Level 4
    4000,   # Level 5
    5000,   # Level 6
    6000,   # Level 7
    7000,   # Level 8
    8000,   # Level 9
]

# pylint: disable=invalid-name
_level_up_handler = None
def get_level_up_handler():
    global _level_up_handler
    if not _level_up_handler:
        _level_up_handler = LevelUpHandler()
    return _level_up_handler

class LevelUpHandler:
    def __init__(self):
        self.creatures = []
        self.xp = 0

    def add_creature(self, creature):
        self.creatures.append(creature)

    def get_exp(self):
        return self.xp

    def add_xp(self, amount: int):
        self.xp += amount
        next_bp = LEVEL_UP_BREAKPOINTS[self.creatures[0].level]
        if self.xp >= next_bp:
            self.xp -= next_bp
            new_level = self.creatures[0].level + 1

            for c in self.creatures:
                if c.level < new_level:
                    c.level += 1
                    c.stat_points += 1
                    if (c.level) % 2:
                        c.ability_points += 1

            msg = [':YELLOW:Level Up!:YELLOW:']
            msg += [ f'Level: {new_level - 1} -> :GREEN:{new_level}:GREEN:']
            msg += [ ':GREEN:Stat Point Gained!:GREEN:']
            if (new_level) % 2:
                msg += [ ':GREEN:Ability Point Gained!']
            add_notification(msg)
