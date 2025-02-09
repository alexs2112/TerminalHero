from world.area import Area
from main.player_log import get_player_log, update_log

player_log = get_player_log()

EXIT_UP = (0,-1)
EXIT_RIGHT = (1,0)
EXIT_DOWN = (0,1)
EXIT_LEFT = (-1,0)

class Room(Area):
    def __init__(self, name, sprite_rect):
        super().__init__(name, sprite_rect)
        self.type = 'Room'

        # Where this room should be drawn
        # (0,0) is the top left of the whole dungeon sprite which will be centered in the dungeon screen
        # This is before the sprite is scaled
        self.unscaled_position = (0,0)

        # The center of where the player should be drawn in the room
        # This is relative to its own unscaled_position
        self.player_position = (0,0)

        # If the player has explored this room yet or not
        self.log_condition: str = f'room_{self.id}'

        # A list of exits available to this room
        self.exits = []

        # Which of the exits are currently locked
        self.locked = []

        # The direction in which to leave the dungeon
        self.exit_dungeon_direction = None

        # A list of features that the player can interact with (chests, locked doors, etc)
        # For now, just a list of strings, to be expanded upon
        self.features = []

    def set_revealed(self):
        update_log(self.log_condition)

    def is_revealed(self):
        if self.log_condition in player_log:
            return True
        return False

    def set_unscaled_position(self, x, y):
        self.unscaled_position = (x,y)

    def set_player_position(self, x, y):
        self.player_position = (x,y)
