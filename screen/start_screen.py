import os.path
import pygame
from screen.screen import Screen
from screen.world_screen import WorldScreen
from screen.profession_screen import ProfessionScreen
from main.constants import *
from main.colour import *
from serialization.deserializer import Deserializer
from world.world_builder import get_world

world = get_world()

class StartScreen(Screen):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.index = 0
        self.options = [
            "New Game"
        ]
        if os.path.isfile(SAVE_FILE):
            self.options.append("Load Game")
        self.options.append("Exit")

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_UP:
                    self.index -= 1
                    if self.index < 0:
                        self.index = len(self.options) - 1
                elif event.key == pygame.K_DOWN:
                    self.index += 1
                    if self.index >= len(self.options):
                        self.index = 0
                elif event.key == pygame.K_RETURN:
                    if self.options[self.index] == "New Game":
                        if world.player:
                            # If the player is already assigned via commands
                            return WorldScreen(self.canvas, world)
                        return ProfessionScreen(self.canvas)
                    elif self.options[self.index] == "Load Game":
                        d = Deserializer(SAVE_FILE)
                        d.deserialize(world)
                        return d.get_screen(self.canvas, world)
                    elif self.options[self.index] == "Exit":
                        return None
        return self

    def display(self):
        self.canvas.fill(BLACK)
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 - 3 * (FONT_HEIGHT + 4) - 8
        self.write_center_x("Hello World!", (x,y), WHITE)
        y += FONT_HEIGHT + 16

        for i in range(len(self.options)):
            c = GREEN if i == self.index else LIGHTGRAY
            self.write_center_x(self.options[i], (x,y), c)
            y += FONT_HEIGHT + 4
