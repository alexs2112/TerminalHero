from world.area import Area
from creature.player import Player

class World:
    def __init__(self, width, height):
        self.player: Player = None
        self.player_position = (0,0)
        self.width: int = width
        self.height: int = height
        self.areas: list[list[Area]] = []
        self.initialize_areas()

    def initialize_areas(self):
        for _ in range(self.width):
            column = []
            for _ in range(self.height):
                column.append(None)
            self.areas.append(column)

    def get_area_sprite_rect(self, x, y):
        return self.areas[x][y].sprite_rect
