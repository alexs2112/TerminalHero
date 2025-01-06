import pygame
from main.colour import *
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

    def write(self, text: str, location, colour=WHITE):
        coloured = self.split_text_on_colours(text, colour)
        for t, c in coloured:
            rendered = self.font.render(t, True, c)
            self.canvas.blit(rendered, location)
            location = (location[0] + len(t) * FONT_WIDTH, location[1])

    def write_center_x(self, text, location, colour=WHITE):
        len_text = len(text)
        for word in COLOUR_STRINGS:
            len_text -= len(word) * text.count(word)
        new_x = location[0] - (len_text * FONT_WIDTH) / 2
        self.write(text, (new_x, location[1]), colour)

    # This is hilariously inefficient when it is called for every write()
    # I am unsure of a better way to handle this
    def split_text_on_colours(self, text: str, colour):
        for word, c in COLOUR_STRINGS.items():
            if word in text:
                t = text.split(word, 2)
                out = [
                    (t[0], colour),
                    (t[1], c)
                ]
                if len(t) > 2:
                    out += self.split_text_on_colours(t[2], colour)
                return out
        return [(text, colour)]

    def line_length(self, line):
        out = len(line)
        for colour_string in COLOUR_STRINGS:
            out -= len(colour_string) * line.count(colour_string)
        return out

    def draw_border(self):
        self.draw_box((0,0,SCREEN_WIDTH,SCREEN_HEIGHT))

    def draw_box(self, rect, width=6):
        pygame.draw.rect(self.canvas, GRAY, rect)
        pygame.draw.rect(self.canvas, BLACK, (rect[0] + width, rect[1] + width, rect[2] - (width*2), rect[3] - (width*2)))

    def draw_line(self, start, end, width=6, colour=GRAY):
        pygame.draw.line(self.canvas, colour, start, end, width=width)

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
