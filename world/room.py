from world.area import Area

EXIT_UP = 0
EXIT_RIGHT = 1
EXIT_DOWN = 2
EXIT_LEFT = 3

class Room(Area):
    def __init__(self, name, sprite_rect, description):
        super().__init__(name, sprite_rect, description)
        self.type = 'Room'

        # Where this room should be drawn
        # (0,0) is the top left of the whole dungeon sprite which will be centered in the dungeon screen
        # This is before the sprite is scaled
        self.unscaled_position = (0,0)

        # The center of where the player should be drawn in the room
        # This is relative to its own unscaled_position
        self.player_position = (0,0)

        # If the player has explored this room yet or not
        self.revealed: bool = False

        # A list of exits available to this room
        self.exits = []

        # The direction in which to leave the dungeon
        self.exit_dungeon_direction = None

        # A list of features that the player can interact with (chests, locked doors, etc)
        # For now, just a list of strings, to be expanded upon
        self.features = []

    def set_unscaled_position(self, x, y):
        self.unscaled_position = (x,y)

    def set_player_position(self, x, y):
        self.player_position = (x,y)