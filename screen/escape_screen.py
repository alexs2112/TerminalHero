import pygame
from screen.screen import Screen
from screen.controls_screen import ControlsScreen
from main.constants import *
from main.colour import *
from main.notification import add_notification
from serialization.serializer import Serializer
from serialization.deserializer import Deserializer
from world.world_builder import get_world

world = get_world()

class EscapeScreen(Screen):
    def __init__(self, canvas, prev_screen, can_save=True, load_screen='world'):
        super().__init__(canvas)
        self.prev_screen = prev_screen
        self.can_save = can_save
        self.load_screen = load_screen
        self.index = 0 if can_save else 1
        self.options = [
            "Save",
            "Load",
            "Controls",
            "Exit"
        ]

        self.box_width = FONT_WIDTH * 16
        self.box_height = (FONT_HEIGHT + 4) * (len(self.options) + 2)
        self.box_start = (SCREEN_WIDTH - self.box_width) / 2

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.index += 1
                    if self.index >= len(self.options):
                        self.index = 0
                elif event.key == pygame.K_UP:
                    self.index -= 1
                    if self.index < 0:
                        self.index = len(self.options) - 1
                elif event.key == pygame.K_RETURN:
                    if self.options[self.index] == "Save":
                        if self.can_save:
                            self.save_game()
                            return self.prev_screen
                        else:
                            return self
                    elif self.options[self.index] == "Load":
                        return self.load_game()
                        # I do not remember why this is commented out?
                        # self.prev_screen.refresh()
                        # return self.prev_screen
                    elif self.options[self.index] == "Controls":
                        return ControlsScreen(self.canvas, self.prev_screen)
                    elif self.options[self.index] == "Exit":
                        return None
                elif event.key == pygame.K_ESCAPE:
                    return self.prev_screen
        return self

    def display(self):
        # Draw this escape menu on top of the last screen
        self.prev_screen.display()
        self.draw_box((self.box_start, 128, self.box_width, self.box_height))

        x = SCREEN_WIDTH / 2
        y = 128 + FONT_HEIGHT + 4
        for i in range(len(self.options)):
            # For now, the only special case we need to keep track of is saving the game
            if i == 0 and not self.can_save:
                c = DARKGREEN if i == self.index else GRAY
            else:
                c = GREEN if i == self.index else WHITE
            self.write_center_x(self.options[i], (x, y), c)
            y += FONT_HEIGHT + 4
        self.display_notifications()

    def save_game(self):
        add_notification(['Game Saved!'])
        s = Serializer(SAVE_FILE)
        s.serialize(world, self.load_screen)

    def load_game(self):
        add_notification(['Game Loaded!'])
        d = Deserializer(SAVE_FILE)
        d.deserialize(world)
        return d.get_screen(self.canvas, world)
