class CreatureSprite:
    def __init__(self, sprite_rect, dead_rect):
        self.sprite_rect = sprite_rect
        self.dead_rect = dead_rect

    def get(self, creature):
        if creature.is_alive():
            return self.sprite_rect
        return self.dead_rect
