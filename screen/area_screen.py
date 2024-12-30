import pygame
from screen.screen import Screen
from world.area import Area
from world.world import World
from main.constants import *
from main.util import fit_text, NUMBERS

# Some basic functions that are called by the option the player selects
def leave_area(canvas, world):
    # pylint: disable=import-outside-toplevel
    from screen.world_screen import WorldScreen
    return WorldScreen(canvas, world)

class AreaScreen(Screen):
    def __init__(self, canvas, area: Area, world: World):
        super().__init__(canvas)
        self.area = area
        self.description_lines = fit_text(self.area.description)
        self.world = world
        self.index = 0
        self.options = self.define_options()

    def define_options(self):
        opts = []
        opts.append(("Leave Area", leave_area))
        return opts

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.index = min(self.index + 1, len(self.options) - 1)
                elif event.key == pygame.K_UP:
                    self.index = max(0, self.index - 1)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.index][1](self.canvas, self.world)
                elif event.key in NUMBERS:
                    i = int(pygame.key.name(event.key)) - 1
                    if i < len(self.options):
                        return self.options[i][1](self.canvas, self.world)
        return self

    def display(self):
        super().display()

        y = 20
        self.write_center_x(self.area.name, (int(SCREEN_WIDTH / 2), y))
        y += FONT_HEIGHT + 8
        for line in self.description_lines:
            self.write_center_x(line, (int(SCREEN_WIDTH / 2), y))
            y += FONT_HEIGHT + 2

        x = 64
        y += 16
        for i in range(len(self.options)):
            opt = self.options[i][0]
            colour = WHITE
            if i == self.index:
                colour = GREEN
            self.write(f"[{i+1}]: {opt}", (x,y), colour)
