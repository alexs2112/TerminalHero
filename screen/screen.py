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

    def write(self, text, location, colour=WHITE):
        t = self.font.render(text, True, colour)
        self.canvas.blit(t, location)
    
    def write_center_x(self, text, location, colour=WHITE):
        t = self.font.render(text, True, colour)
        new_x = location[0] - (len(text) * FONT_WIDTH) / 2
        self.canvas.blit(t, (new_x, location[1]))

    def draw_box(self, rect):
        pygame.draw.rect(self.canvas, GRAY, rect)
        pygame.draw.rect(self.canvas, BLACK, (rect[0] + 6, rect[1] + 6, rect[2] - 12, rect[3] - 12))

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
