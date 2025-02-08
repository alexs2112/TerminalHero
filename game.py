#!/bin/python3

import argparse
import pygame
from main.constants import *
from main.colour import *
from main.messenger import get_messenger
from main.clock import get_clock
from main.player_log import get_player_log, update_log
from creature.creature_factory import get_creature_factory
from world.world_builder import WorldBuilder
from screen.start_screen import StartScreen
from serialization.serializer import Serializer
from serialization.deserializer import Deserializer

clock = get_clock()
creature_factory = get_creature_factory()
player_log = get_player_log()

class Game:
    def __init__(self, args_list):
        pygame.init()
        pygame.display.set_caption("Terminal Hero")
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.args = args_list
        messenger = get_messenger(self.args)
        if self.args.verbose:
            messenger.set_verbose()
        messenger.clear()

        self.world = self.generate_world()

        if self.args.profession:
            self.player = creature_factory.new_player(self.args.profession)
            self.world.player = self.player
        else:
            # This still needs to be set for other cmd line args
            self.player = creature_factory.new_player('champion')

        # Temporary testing of saving and loading game state
        s = Serializer(SAVE_FILE)
        s.serialize(self.world)
        d = Deserializer(SAVE_FILE)
        d.load_companions()
        d.load_player_log()

        if self.args.stats:
            print("Increasing all player stats by 30")
            for s in self.player.stats:
                self.player.stats[s] += 30
            self.player.hp = self.player.max_hp()
            self.player.armor = self.player.max_armor()
            if not self.args.profession:
                print("[WARNING] Player profession not set, stats will be overwritten when profession is selected.")

        if args_list.all:
            # pylint: disable=import-outside-toplevel,ungrouped-imports
            from dialog.dialog_functions import set_initial_village, add_quest_grave_concerns
            set_initial_village(None)
            add_quest_grave_concerns(None)
            update_log('tavern_open')
            update_log('tavern_store_unlocked')
            update_log('tavern_room_unlocked')

        if args_list.log:
            logs = args_list.log.split(',')
            for l in logs:
                update_log(l)

        self.screen = StartScreen(self.canvas, self.world)

        if args_list.dungeon:
            self.dungeon_test(args_list.dungeon, args_list.revealed, args_list.no_enemies)

        if args_list.inventory:
            self.inventory_test()

    def generate_world(self):
        world_builder = WorldBuilder(9,9)
        return world_builder.build_world()

    def game_loop(self):
        while True:
            clock.tick(FRAMERATE)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return

            self.screen = self.screen.check_events(events)
            if not self.screen:
                return

            self.screen.display()
            pygame.display.update()

    def dialog_test(self):
        # pylint: disable=import-outside-toplevel
        from screen.dialog_screen import DialogScreen
        from dialog.dialog_parser import load_dialog
        base_node = load_dialog('resources/dialog/test_elder_varik.json')
        self.screen = DialogScreen(self.canvas, None, base_node['start'], self.player)

    def dungeon_test(self, dungeon_name, set_revealed, no_enemies):
        # pylint: disable=import-outside-toplevel
        from world.dungeon_builder import DungeonBuilder
        from screen.dungeon_screen import DungeonScreen
        from dialog.dialog_functions import add_quest_grave_concerns
        if dungeon_name == 'crypt':
            d = DungeonBuilder().new_vaelthorne_crypt(None)
            update_log('runebound_stalker_defeated')
        elif dungeon_name == 'cemetery':
            d = DungeonBuilder().new_arad_cemetery(None)
            add_quest_grave_concerns(None)
        elif dungeon_name == 'caravan':
            d = DungeonBuilder().new_caravan_wreckage(None)
        elif dungeon_name == 'camp':
            d = DungeonBuilder().new_bandit_camp(None)
        else:
            print(f"Error: Could not find dungeon {dungeon_name}")
            exit(1)

        if set_revealed:
            for r in d.get_rooms():
                r.revealed = True

        if no_enemies:
            for a in d.room_list:
                for e in a.encounters:
                    e.completed = True
        self.screen = DungeonScreen(self.canvas, d, self.player, None)

    def inventory_test(self):
        # pylint: disable=import-outside-toplevel
        from screen.inventory_screen import InventoryScreen
        from item.item_factory import get_item_factory
        from item.inventory import get_inventory
        i = get_item_factory()
        inventory = get_inventory()
        inventory.add_list([ i.new_axe(), i.new_hammer(), i.new_leather_armor(), i.new_robe(), i.new_axe(), i.new_hammer(),
                             i.new_axe(), i.new_hammer(), i.new_axe(), i.new_hammer(), i.new_staff(), i.new_staff(),
                             i.new_axe(), i.new_hammer(), i.new_leather_armor() ])
        self.screen = InventoryScreen(self.canvas, self.player, None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug and info statements')
    parser.add_argument('-d', '--dialog', action='store_true', help='test dialog')
    parser.add_argument('-p', '--profession', help='set the starting profession of the player')
    parser.add_argument('-a', '--all', action='store_true', help='enable "all" player_log fields')
    parser.add_argument('-l', '--log', help='comma separated list of player_log entries to start with')
    parser.add_argument('-u', '--dungeon', help='test dungeon display by name')
    parser.add_argument('-r', '--revealed', action='store_true', help='for dungeon mode, set all rooms as revealed')
    parser.add_argument('-e', '--no-enemies', action='store_true', help='for dungeon mode, remove all encounters')
    parser.add_argument('-s', '--stats', action='store_true', help='gives the player massively enhanced stats, must be used with the profession option')
    parser.add_argument('-i', '--inventory', action='store_true', help='show the inventory test screen')
    args = parser.parse_args()

    game = Game(args)
    if args.dialog:
        game.dialog_test()
    game.game_loop()
