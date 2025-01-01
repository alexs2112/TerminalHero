#!/bin/python3

import argparse
import pygame
from main.constants import *
from main.messenger import get_messenger
from main.clock import get_clock
from world.world_builder import WorldBuilder
from creature.creature_factory import CreatureFactory

clock = get_clock()

class Game:
    def __init__(self, args_list):
        pygame.init()
        pygame.display.set_caption("Terminal Hero")
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.args = args_list
        self.messenger = get_messenger(self.args)
        self.messenger.clear()

        self.creature_factory = CreatureFactory()
        self.player = self.creature_factory.new_player()
        self.world = self.generate_world()
        self.world.player = self.player
        self.player.party.append(self.creature_factory.new_companion_1())

        # This needs to be called after messenger is created or else it will be empty
        # pylint: disable=import-outside-toplevel
        from screen.start_screen import StartScreen
        self.screen = StartScreen(self.canvas, self.world)

    def generate_world(self):
        world_builder = WorldBuilder(3,3, self.creature_factory)
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
        base_node = load_dialog('resources/dialog/initial_elder_varik.json')
        self.screen = DialogScreen(self.canvas, None, base_node['root_node'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug and info statements')
    parser.add_argument('-d', '--dialog', action='store_true', help='test dialog')
    parser.add_argument('-c', '--companion', action='store_true', help='test a companion in the player party')
    parser.add_argument('-a', '--all', action='store_true', help='enable all player_log fields')
    args = parser.parse_args()

    if args.all:
        # pylint: disable=import-outside-toplevel,ungrouped-imports
        from main.player_log import get_player_log
        player_log = get_player_log()
        for key in player_log:
            player_log[key] = True

    game = Game(args)
    if args.dialog:
        game.dialog_test()
    game.game_loop()
