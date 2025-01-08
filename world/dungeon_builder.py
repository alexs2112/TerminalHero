from world.dungeon import Dungeon
from world.room import *

class DungeonBuilder:
    def new_crypt(self):
        d = Dungeon(2,3)
        d.set_unscaled_size(53, 95)
        d.start_player_pos = (0,1)

        entrance = Room("Entrance Hall", (1,40,29,31), "Placeholder Text")
        entrance.set_unscaled_position(0,32)
        entrance.set_player_position(15,15)
        entrance.features = [ 'Locked Door' ]
        entrance.exits = [ EXIT_RIGHT ]
        d.add_room((0,1), entrance)

        main_hall = Room("Main Hall", (31,31,21,47), "Placeholder Text")
        main_hall.set_unscaled_position(24,23)
        main_hall.set_player_position(11,23)
        main_hall.exits = [ EXIT_UP, EXIT_DOWN, EXIT_LEFT ]
        d.add_room((1,1), main_hall)

        sacred_crypt = Room("Sacred Crypt", (7,2,45,29), "Placeholder Text")
        sacred_crypt.set_unscaled_position(0,0)
        sacred_crypt.set_player_position(34,12)
        sacred_crypt.exits = [ EXIT_DOWN ]
        d.add_room((1,0), sacred_crypt)

        pool_room = Room("Pool Room", (23,79,37,31), "Placeholder Text")
        pool_room.set_unscaled_position(16,63)
        pool_room.set_player_position(19,14)
        pool_room.features = [ 'Treasure Chest' ]
        pool_room.exits = [ EXIT_UP ]
        d.add_room((1,2), pool_room)

        return d
