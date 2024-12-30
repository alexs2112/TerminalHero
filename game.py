#!/bin/python3

import argparse
import pygame
from main.constants import *
from main.messenger import get_messenger
from world.world_builder import WorldBuilder
from creature.creature_factory import CreatureFactory

class Game:
    def __init__(self, args_list):
        pygame.init()
        pygame.display.set_caption("Terminal Hero")
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.args = args_list
        self.messenger = get_messenger(self.args)
        self.messenger.clear()

        self.world = self.generate_world()

        self.creature_factory = CreatureFactory()
        self.player = self.creature_factory.new_player()
        self.world.player = self.player
        self.world.player_position = (0,1)

        # This needs to be called after messenger is created or else it will be empty
        # pylint: disable=import-outside-toplevel
        # from screen.start_screen import StartScreen
        # self.screen = StartScreen(self.canvas)

        from screen.world_screen import WorldScreen
        self.screen = WorldScreen(self.canvas, self.world)

    def generate_world(self):
        world_builder = WorldBuilder(3,3)
        return world_builder.build_world()

    def game_loop(self):
        while True:
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
        self.screen = DialogScreen(self.canvas, base_node['root_node'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug and info statements')
    parser.add_argument('-d', '--dialog', action='store_true', help='log debug and info statements')
    args = parser.parse_args()

    game = Game(args)
    if args.dialog:
        game.dialog_test()
    game.game_loop()
