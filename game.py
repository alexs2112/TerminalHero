#!/bin/python3

import pygame
from main.constants import *
from screen.start_screen import StartScreen

def setup_logger():
    # https://docs.python.org/3/howto/logging.html#configuring-logging
    import logging
    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class Game:
    def __init__(self):
        pygame.init()        
        pygame.display.set_caption("Eee")
        self.canvas = pygame.display.set_mode((800,480))
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
    setup_logger()
    game = Game()
    game.game_loop()
    