import pygame
from main.constants import *
from main.messenger import *
from main.notification import get_notification

messenger = get_messenger()

class Screen:
    def __init__(self, canvas):
        self.canvas = canvas
        self.load_resources()

    def load_resources(self):
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def check_events(self, events):
        pass

    def display(self):
        self.canvas.fill(BLACK)
        self.draw_border()

    def refresh(self, **kwargs):
        pass

    def check_notifications(self, events):
        notification = get_notification()
        if notification:
            notification.check_events(events)
            return True
        return False

    def display_notifications(self):
        notification = get_notification()
        if notification:
            notification.display(self)

    def write(self, text, location, colour=WHITE):
        t = self.font.render(text, True, colour)
        self.canvas.blit(t, location)

    def write_center_x(self, text, location, colour=WHITE):
        t = self.font.render(text, True, colour)
        new_x = location[0] - (len(text) * FONT_WIDTH) / 2
        self.canvas.blit(t, (new_x, location[1]))

    def draw_border(self):
        self.draw_box((0,0,SCREEN_WIDTH,SCREEN_HEIGHT))

    def draw_box(self, rect, width=6):
        pygame.draw.rect(self.canvas, GRAY, rect)
        pygame.draw.rect(self.canvas, BLACK, (rect[0] + width, rect[1] + width, rect[2] - (width*2), rect[3] - (width*2)))

    def draw_line(self, start, end):
        pygame.draw.line(self.canvas, GRAY, start, end, width=6)

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
