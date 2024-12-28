#!/bin/python3

import argparse, pygame
from main.constants import *
from main.messenger import get_messenger

class Game:
    def __init__(self, args):
        pygame.init()
        pygame.display.set_caption("Terminal Hero")
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.args = args
        self.messenger = get_messenger(args)

        # This needs to be called after messenger is created or else it will be empty
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug and info statements')
    args = parser.parse_args()

    game = Game(args)
    game.game_loop()
    