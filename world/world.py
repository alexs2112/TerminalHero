from world.area import Area
from creature.player import Player

class World:
    def __init__(self):
        self.player: Player = None
        self.areas: list[Area] = []
        self.positions: dict[Area, (int, int)] = {}

    def add_area(self, position, area):
        self.areas.append(area)
        self.positions[area] = position

    def get_areas(self):
        return self.areas

    def get_known_areas(self):
        return [ a for a in self.areas if a.condition_met() and not a.is_filler ]
