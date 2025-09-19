import pygame
from main.constants import *
from main.colour import *
from screen.screen import Screen

class ControlsScreen(Screen):
    def __init__(self, canvas, prev_screen):
        super().__init__(canvas)
        self.prev_screen = prev_screen
        self.index = 0
        self.text = [
            ("Arrow Keys", "movement and selection keys"),
            ("Enter", "select button"),
            ("Escape", "cancel button, open menu"),
            ("L", "quest log"),
            ("I", "inventory"),
            ("C", "character screen")
        ]

        max_chars = 0
        for a,b in self.text:
            c = len(a) + len(b) + 2
            if c > max_chars:
                max_chars = c
        self.width = max_chars * FONT_WIDTH + 64
        self.start_x = (SCREEN_WIDTH - self.width) / 2
        self.height = (len(self.text) + 3) * (FONT_HEIGHT + 2) + 2
        self.start_y = (SCREEN_HEIGHT - self.height) / 2

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.prev_screen
        return self

    def display(self):
        # Draw this escape menu on top of the last screen
        self.prev_screen.display()
        self.draw_box((self.start_x, self.start_y, self.width, self.height))
        x=self.start_x+16
        y=self.start_y+16
        self.write("Controls:", (x,y))
        x+=16
        y+=FONT_HEIGHT+4
        for button, desc in self.text:
            self.write(f"{button}:", (x,y))
            inc = FONT_WIDTH * (len(button) + 2)
            self.write(desc, (x+inc, y), LIGHTGRAY)
            y += FONT_HEIGHT+2
