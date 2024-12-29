#!/bin/python3

import argparse
import pygame
from main.constants import *
from main.messenger import get_messenger

class Game:
    def __init__(self, args_list):
        pygame.init()
        pygame.display.set_caption("Terminal Hero")
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.args = args_list
        self.messenger = get_messenger(self.args)
        self.messenger.clear()

        # This needs to be called after messenger is created or else it will be empty
        # pylint: disable=import-outside-toplevel
        from screen.start_screen import StartScreen
        self.screen = StartScreen(self.canvas)

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
        # pylint: disable=import-outside-toplevel,line-too-long
        from screen.dialog_screen import DialogScreen
        from dialog.dialog_parser import load_dialog
        base_node = load_dialog('resources/dialog/test.json')
        self.screen = DialogScreen(self.canvas, base_node['base_node'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug and info statements')
    parser.add_argument('-d', '--dialog', action='store_true', help='log debug and info statements')
    args = parser.parse_args()

    game = Game(args)
    if args.dialog:
        game.dialog_test()
    game.game_loop()
    