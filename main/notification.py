import pygame
from main.constants import *
from main.util import fit_text

# pylint: disable=invalid-name
_notification = None
def set_notification(text_list: list[str], min_height: int = 0):
    global _notification
    _notification = Notification(text_list, min_height)
def get_notification():
    return _notification
def clear_notification():
    global _notification
    _notification = None

NOTIFICATION_WIDTH = SCREEN_WIDTH - 128
NOTIFICATION_START = 64
class Notification:
    def __init__(self, text_list, min_height):
        self.text: list[str] = text_list
        self.final: str = 'press [enter] to continue'
        self.lines: list[str] = self.get_lines()
        self.height = self.get_height(min_height)

    def get_lines(self):
        out = []
        for t in self.text:
            out += fit_text(t, NOTIFICATION_WIDTH - 32)
        out.append('')
        out.append(self.final)
        return out

    def get_height(self, min_height):
        h = len(self.lines) * (FONT_HEIGHT + 2) + 40
        return max(min_height, h)

    def display(self, screen):
        y = (SCREEN_HEIGHT / 2) - (self.height / 2)
        screen.draw_box((NOTIFICATION_START, y, NOTIFICATION_WIDTH, self.height))
        y += 20

        for line in self.lines:
            # Bad way to do this
            c = GRAY if line == self.final else WHITE

            screen.write_center_x(line, (SCREEN_WIDTH / 2, y), c)
            y += FONT_HEIGHT + 2

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    clear_notification()
