import pygame
from main.constants import *

class Screen:
    def __init__(self, canvas):
        self.canvas = canvas
        self.load_resources()

    def load_resources(self):
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def check_events(self, _):
        return self

    def display(self):
        pass
