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
        self.xp = 0

    def get_exp(self):
        return self.xp

    def get_remaining_exp(self):
        next_bp = 0
        for bp in LEVEL_UP_BREAKPOINTS:
            next_bp += bp
            if next_bp > self.xp:
                break
        return next_bp - self.xp

    def get_level(self):
        for i in range(len(LEVEL_UP_BREAKPOINTS)):
            if self.xp < LEVEL_UP_BREAKPOINTS[i]:
                return i

    def add_xp(self, amount: int):
        old = self.xp
        self.xp += amount

        next_bp = 0
        for bp in LEVEL_UP_BREAKPOINTS:
            next_bp += bp
            if next_bp > old:
                break

        if self.xp >= next_bp:
            new_level = self.get_level()
            msg = [':YELLOW:Level Up!:YELLOW:']
            msg += [ f'Level: {new_level - 1} -> :GREEN:{new_level}:GREEN:']
            msg += [ ':GREEN:Stat Point Gained!:GREEN:']
            msg += [ ':GREEN:Ability Point Gained!']
            add_notification(msg)
