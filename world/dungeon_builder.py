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
                    "A forsaken patch of land overrun with decay and neglect. "
                    "Crumbling headstones jut from the earth like forgotten memories, while overgrown weeds claim the graves in a suffocating embrace. "
                    "A faint, acrid smell of rot lingers in the air, and a deathly stillness hangs heavy over the area.",
                    area, 2, 2)
        d.set_unscaled_size(63, 65)
        d.start_player_pos = (0,1)

        start = Room("Cemetery Entrance", (54, 35, 32, 32))
        start.add_description(
            "The dirt path leading into the cemetery is lined with shattered headstones and dry, withered grass. "
            "The overgrowth reaches across the path, clawing at the legs of any who pass. "
            "The scent of decay thickens as you walk, and the distant sound of rustling leaves adds to the eerie atmosphere."
        )
        start.set_unscaled_position(0, 33)
        start.set_player_position(16,15)
        start.exits = [ EXIT_UP, EXIT_RIGHT ]
        start.exit_dungeon_direction = EXIT_LEFT
        d.add_room((0,1), start)

        tree = Room("Deathly Tree", (54, 1, 32, 33))
        tree.add_description(
            "The centerpiece of this area is a massive, decaying tree with brittle, gnarled branches that claw at the sky. "
            "Its blackened bark is cracked, and a faint ooze leaks from its hollow trunk. "
            "Scattered bones and remnants of graves circle its base, as though the tree itself feeds on the cemetery's corruption."
        )
        tree.set_unscaled_position(0,0)
        tree.set_player_position(16,16)
        tree.exits = [ EXIT_RIGHT, EXIT_DOWN ]
        tree.encounters = [
            encounter_factory.cemetery_first_stage_1(),
            encounter_factory.cemetery_second_stage_1(),
            encounter_factory.cemetery_third_stage_1()
        ]
        d.add_room((0,0), tree)

        mauses = Room("Shattered Mausoleums", (87,35,31,32))
        mauses.add_description(
            "This section is dominated by three mausoleums, all in various stages of ruin. "
            "One has caved in completely, its crypt exposed to the elements. "
            "Another's stone walls are cracked, with faint engravings barely visible. "
            "The last leans precariously, its door hanging loose on rusted hinges. "
        )
        mauses.set_unscaled_position(32,33)
        mauses.set_player_position(14,15)
        mauses.exits = [ EXIT_LEFT, EXIT_UP ]
        mauses.encounters = [
            encounter_factory.cemetery_first_stage_2(),
            encounter_factory.cemetery_second_stage_2(),
            encounter_factory.cemetery_third_stage_2()
        ]
        d.add_room((1,1), mauses)

        church = Room("Abandoned Church", (87,1,31,33))
        church.add_description(
            "This decrepit structure stands at the far end of the cemetery, its roof partially collapsed and its wooden doors splintered. "
            "Broken stained-glass windows depict barely recognizable scenes of mourning and prayer. "
            "Inside the church, rubble and shattered pews litter the floor, and the smell of damp earth is overwhelming."
        )
        church.set_unscaled_position(32,0)
        church.set_player_position(14,16)
        church.exits = [ EXIT_LEFT, EXIT_DOWN ]
        church.encounters = [
            # Ambush occurs once the player has exhausted Gorren dialogue
            encounter_factory.cemetery_second_stage_ambush(),

            # This encounter is set after the player completes the Vaelthorne Crypt
            encounter_factory.cemetery_third_stage_3(),

            # Set once the ritual is interrupted
            encounter_factory.soul_tethered_herald()
        ]
        church.features = [
            # Talking to Gorren finishes Cemetery Stage 1
            feature_factory.gorren_initial_meeting(),

            feature_factory.gorren_banishment_ritual()
        ]
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
        burial_chamber.encounters = [ encounter_factory.get_crypt_encounter_3() ]
        d.add_room((1,0), burial_chamber)

        ritual_room = Room("Ritual Room", (23,79,37,31))
        ritual_room.add_description(
            "Two large pools of still, murky water dominate the room, their surfaces reflecting the dim glow of shattered Bloodstones lying inert within them. "
            "The air is damp, heavy with an unnatural energy, and the faint scent of iron lingers. "
            "At the far end, an :YELLOW:Ancient Chest:YELLOW: rests in the gloom, its ornate design hinting at something long forgotten."
        )
        ritual_room.set_unscaled_position(16,63)
        ritual_room.set_player_position(19,14)
        ritual_room.features = [ ] # Treasure Chest
        ritual_room.exits = [ EXIT_UP ]
        ritual_room.encounters = [ encounter_factory.get_crypt_encounter_2() ]
        d.add_room((1,2), ritual_room)

        return d

    def new_caravan_wreckage(self, area):
        d = Dungeon("Caravan Wreckage",
                    "The remains of the caravan smolder in the midday sun—charred wagons overturned, splintered crates spilling their contents across the dirt. "
                    "The stench of burnt wood and flesh lingers in the air, and blood darkens the earth where the traders made their last stand.",
                    area, 2, 2)
        d.set_unscaled_size(64,64)
        d.start_player_pos = (0,0)

        entrance = Room("Caravan Wreckage", (1,111,32,32))
        entrance.add_description("Wagon wheels lie shattered, their cargo scattered and looted. "
                                 "A strongbox sits pried open and empty, its lock twisted and broken. "
                                 "Among the wreckage, a few bodies remain—stripped of valuables, left to the scavengers.")
        entrance.set_unscaled_position(0,0)
        entrance.set_player_position(16,21)
        entrance.exits = [ EXIT_RIGHT, EXIT_DOWN ]
        entrance.exit_dungeon_direction = EXIT_LEFT
        d.add_room((0,0), entrance)

        raider = Room("Raider Hiding Spot", (1,144,32,32))
        raider.add_description("The scattered remains of a small camp sit nestled between the boulders. "
                               "Burnt-out torches, discarded arrow shafts, and a crude firepit long gone cold. "
                               "Whoever was here has already moved on.")
        raider.set_unscaled_position(0,32)
        raider.set_player_position(16,17)
        raider.exits = [ EXIT_UP ]
        raider.encounters = [ encounter_factory.caravan_wreckage_1() ]
        d.add_room((0,1), raider)

        second = Room("Caravan Wreckage", (34,111,32,32))
        second.add_description("The ground is littered with torn banners and trampled supplies. "
                               "A set of bloodied footprints lead away from the scene, vanishing into the undergrowth beyond.")
        second.set_unscaled_position(32,0)
        second.set_player_position(12,21)
        second.exits = [ EXIT_LEFT, EXIT_DOWN ]
        second.encounters = [ encounter_factory.caravan_wreckage_2() ]
        d.add_room((1,0), second)

        forest = Room("Forest Road", (34,144,32,32))
        forest.add_description("A thick canopy of leaves sways overhead, casting flickering shadows on the path. "
                               "The air is thick with the scent of damp earth and old blood, the silence broken only by the distant call of carrion birds. "
                               "The bandit trail ends here...")
        forest.set_unscaled_position(32,32)
        forest.set_player_position(12,17)
        forest.exits = [ EXIT_UP ]
        forest.features = [ feature_factory.rangu_initial_meeting() ]
        d.add_room((1,1), forest)

        return d
