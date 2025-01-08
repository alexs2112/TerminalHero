from world.room import Room

class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rooms: list[list[Room]] = [[None for y in range(height)] for x in range(width)]
        self.room_list: list[Room] = []

        # Which room coords the player starts in
        self.start_player_pos = (0,0)

        # How many pixels the unscaled dungeon is to draw
        self.unscaled_width = 0
        self.unscaled_height = 0

    def add_room(self, pos, room: Room):
        self.rooms[pos[0]][pos[1]] = room
        self.room_list.append(room)

    def get_rooms(self):
        return self.room_list

    def set_unscaled_size(self, width, height):
        self.unscaled_width = width
        self.unscaled_height = height
