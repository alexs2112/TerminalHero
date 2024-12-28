import pygame
from screen.screen import Screen
from screen.combat_screen import CombatScreen
from main.constants import *

class StartScreen(Screen):
    def __init__(self, canvas):
        super().__init__(canvas)

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                return CombatScreen(self.canvas)
        return self

    def display(self):
        self.canvas.fill(BLACK)
        text = ['Hello World.',
                'Press any key to continue.']
        x = SCREEN_WIDTH / 2
        y = (SCREEN_HEIGHT / 2) - (len(text) * int(FONT_HEIGHT / 2 + 2))
        for line in text:
            t = self.font.render(line, True, WHITE)
            r = t.get_rect(center=(x, y))
            y += FONT_HEIGHT + 2
            self.canvas.blit(t, r)
