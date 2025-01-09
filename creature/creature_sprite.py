from creature.item import WEAPON

class CreatureSprite:
    def __init__(self, sprite_rect, dead_rect):
        self.sprite_rect = sprite_rect
        self.dead_rect = dead_rect

    def get(self, creature):
        if creature.is_alive():
            # If this is a dynamic sprite for party members
            if self.sprite_rect == -1:
                if creature.equipment[WEAPON] and creature.equipment[WEAPON].equipped_sprite_rect:
                    return creature.equipment[WEAPON].equipped_sprite_rect
                else:
                    # Not sure where else to put this, this should be refactored
                    return (0,24,12,12)
            return self.sprite_rect
        return self.dead_rect
