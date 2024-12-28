import pygame
from main.constants import *
from main.messenger import *

messenger = get_messenger()

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

    def draw_messages(self, max_messages=8):
        latest = len(messenger.latest_messages)
        max_messages = max(latest, max_messages)
        messages = messenger.get_latest(max_messages)
        messages.reverse()

        x, y = 16, SCREEN_HEIGHT - 16 - FONT_HEIGHT - 2
        for i in range(len(messages)):
            colour = WHITE if i < latest else GRAY
            text = self.font.render(messages[i], False, colour)
            self.canvas.blit(text, (x, y))
            y -= (FONT_HEIGHT + 2)
