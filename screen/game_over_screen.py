import pygame
from main.constants import *
from screen.screen import Screen

class GameOverScreen(Screen):
    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                from screen.start_screen import StartScreen
                return StartScreen(self.canvas)
        return self

    def display(self):
        self.canvas.fill(BLACK)
        text = ['you died.',
                'press escape to exit',
                'press any other key to return to start']
        x = SCREEN_WIDTH / 2
        y = (SCREEN_HEIGHT / 2) - (len(text) * int(FONT_HEIGHT / 2 + 2))
        for line in text:
            t = self.font.render(line, True, WHITE)
            r = t.get_rect(center=(x, y))
            y += FONT_HEIGHT + 2
            self.canvas.blit(t, r)
