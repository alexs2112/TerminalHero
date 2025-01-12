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

        self.player = creature_factory.new_player()
        self.world = self.generate_world()
        self.world.player = self.player
        if self.args.stats:
            for s in self.player.stats:
                self.player.stats[s] += 30
            self.player.hp = self.player.max_hp()
            self.player.armor = self.player.max_armor()

        if self.args.companion:
            # This will currently break the first quest when you get a second companion
            self.player.party.append(creature_factory.new_companion_1())

        if args_list.all:
            # pylint: disable=import-outside-toplevel,ungrouped-imports
            from dialog.dialog_functions import set_initial_village, add_quest_grave_concerns
            set_initial_village(None)
            add_quest_grave_concerns(self.player)

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
        base_node = load_dialog('resources/dialog/gorren_questline.json')
        self.screen = DialogScreen(self.canvas, None, base_node['start'], self.player)

    def dungeon_test(self, dungeon_name, set_revealed, no_enemies):
        # pylint: disable=import-outside-toplevel
        from world.dungeon_builder import DungeonBuilder
        from screen.dungeon_screen import DungeonScreen
        if dungeon_name == 'crypt':
            d = DungeonBuilder().new_vaelthorne_crypt(None)
            update_log('runebound_stalker_defeated')
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
        from creature.item_factory import get_item_factory
        i = get_item_factory()
        self.player.inventory = [ i.new_axe(), i.new_hammer(), i.new_leather_armor(), i.new_robe(), i.new_axe(),
                                  i.new_hammer(), i.new_axe(), i.new_hammer(), i.new_axe(), i.new_hammer() ]
        self.player.key_items = [ i.new_sword(), i.new_staff(), i.new_staff(), i.new_staff(), i.new_staff() ]
        self.screen = InventoryScreen(self.canvas, self.player, None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug and info statements')
    parser.add_argument('-d', '--dialog', action='store_true', help='test dialog')
    parser.add_argument('-c', '--companion', action='store_true', help='test a companion in the player party')
    parser.add_argument('-a', '--all', action='store_true', help='enable "all" player_log fields')
    parser.add_argument('-l', '--log', help='comma separated list of player_log entries to start with')
    parser.add_argument('-u', '--dungeon', help='test dungeon display by name')
    parser.add_argument('-r', '--revealed', action='store_true', help='for dungeon mode, set all rooms as revealed')
    parser.add_argument('-e', '--no-enemies', action='store_true', help='for dungeon mode, remove all encounters')
    parser.add_argument('-s', '--stats', action='store_true', help='gives the player massively enhanced stats')
    parser.add_argument('-i', '--inventory', action='store_true', help='show the inventory test screen')
    args = parser.parse_args()

    game = Game(args)
    if args.dialog:
        game.dialog_test()
    game.game_loop()
