from world.dungeon import Dungeon
from world.room import *
from world.encounter_factory import get_encounter_factory
from world.feature_factory import get_feature_factory

encounter_factory = get_encounter_factory()
feature_factory = get_feature_factory()

# pylint: disable=invalid-name
_dungeon_builder = None
def get_dungeon_builder():
    global _dungeon_builder
    if not _dungeon_builder:
        _dungeon_builder = DungeonBuilder()
    return _dungeon_builder

class DungeonBuilder:
    #pylint: disable=line-too-long
    def new_arad_cemetery(self, area):
        d = Dungeon('Arad Cemetery',
                    "placeholder text",
                    area, 2, 2)
        d.set_unscaled_size(63, 65)
        d.start_player_pos = (0,1)

        start = Room("Cemetery Entrance", (54, 35, 32, 32))
        start.add_description("placeholder text")
        start.set_unscaled_position(0, 33)
        start.set_player_position(16,15)
        start.exits = [ EXIT_UP, EXIT_RIGHT ]
        start.exit_dungeon_direction = EXIT_LEFT
        d.add_room((0,1), start)

        tree = Room("Deathly Tree", (54, 1, 32, 33))
        tree.add_description("placeholder text")
        tree.set_unscaled_position(0,0)
        tree.set_player_position(16,16)
        tree.exits = [ EXIT_RIGHT, EXIT_DOWN ]
        d.add_room((0,0), tree)

        pool = Room("Shattered Mausoleums", (87,35,31,32))
        pool.add_description("placeholder text")
        pool.set_unscaled_position(32,33)
        pool.set_player_position(14,15)
        pool.exits = [ EXIT_LEFT, EXIT_UP ]
        d.add_room((1,1), pool)

        church = Room("Abandoned Church", (87,1,31,33))
        church.add_description("placeholder text")
        church.set_unscaled_position(32,0)
        church.set_player_position(14,16)
        church.exits = [ EXIT_LEFT, EXIT_DOWN ]
        church.features = [ feature_factory.cemetery_church() ]
        d.add_room((1,0), church)

        return d

    def new_vaelthorne_crypt(self, area):
        d = Dungeon('Vaelthorne Crypt',
                    "A heavy, suffocating chill fills the air, thick with the scent of damp stone and decayed linen. "
                    "Flickering sconces cast long, shifting shadows across ancient sarcophagi, their lids slightly ajar as if disturbed. "
                    "A faint, unnatural whisper echoes through the chamber. The dead do not rest easily here.",
                    area, 2,3)
        d.set_unscaled_size(53, 95)
        d.start_player_pos = (0,1)

        entrance = Room("Entrance Hall", (1,40,29,31))
        entrance.add_description(
            "A heavy, suffocating chill fills the air, thick with the scent of damp stone and decayed linen. "
            "Flickering sconces cast long, shifting shadows across ancient sarcophagi, their lids slightly ajar as if disturbed. "
            "A faint, unnatural whisper echoes through the chamber. The dead do not rest easily here."
        )
        entrance.set_unscaled_position(0,32)
        entrance.set_player_position(15,15)
        entrance.features = [ feature_factory.vaelthorne_crypt_entrance() ]
        entrance.exits = [ EXIT_RIGHT ]
        entrance.locked = [ EXIT_RIGHT ]
        entrance.exit_dungeon_direction = EXIT_LEFT
        d.add_room((0,1), entrance)

        main_hall = Room("Main Hall", (31,31,21,47))
        main_hall.add_description(
            "A vast chamber stretches before you, its once-grand architecture now in ruin. "
            "Rubble litters the floor, and shattered statues of long-forgotten figures stand in eerie silence, their faces broken and lost to time. "
            "The flickering torchlight casts deep shadows, giving the illusion that something stirs just beyond sight."
        )
        main_hall.set_unscaled_position(24,23)
        main_hall.set_player_position(11,23)
        main_hall.exits = [ EXIT_UP, EXIT_DOWN, EXIT_LEFT ]
        main_hall.encounters = [ encounter_factory.get_crypt_encounter_1() ]
        d.add_room((1,1), main_hall)

        burial_chamber = Room("Burial Chamber", (7,2,45,29))
        burial_chamber.add_description(
            "The scent of decay is overwhelming in this sacred space, now defiled and disturbed. "
            "Rows of small, desecrated graves line the chamber, their contents stolen or scattered, while a massive sarcophagus at the far end sits with its lid pushed aside. "
            "Whatever once rested here is long gone, leaving only an unsettling void where the dead should have remained."
        )
        burial_chamber.set_unscaled_position(0,0)
        burial_chamber.set_player_position(34,12)
        burial_chamber.exits = [ EXIT_DOWN ]
        burial_chamber.encounters = [ encounter_factory.get_crypt_encounter_2() ]
        d.add_room((1,0), burial_chamber)

        pool_room = Room("Ritual Room", (23,79,37,31))
        pool_room.add_description(
            "Two large pools of still, murky water dominate the room, their surfaces reflecting the dim glow of shattered Bloodstones lying inert within them. "
            "The air is damp, heavy with an unnatural energy, and the faint scent of iron lingers. "
            "At the far end, an :YELLOW:Ancient Chest:YELLOW: rests in the gloom, its ornate design hinting at something long forgotten."
        )
        pool_room.set_unscaled_position(16,63)
        pool_room.set_player_position(19,14)
        pool_room.features = [ ] # Treasure Chest
        pool_room.exits = [ EXIT_UP ]
        d.add_room((1,2), pool_room)

        return d
