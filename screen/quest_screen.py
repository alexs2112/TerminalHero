import pygame
from screen.screen import Screen
from quests.quest_handler import get_quest_handler
from main.constants import *
from main.colour import *
from main.util import fit_text

quest_handler = get_quest_handler()

class QuestScreen(Screen):
    def __init__(self, canvas, prev_screen: Screen):
        super().__init__(canvas)
        self.prev_screen = prev_screen
        self.center_point = SCREEN_WIDTH / 3

        self.index = 0
        self.quest_num = len(quest_handler.get()) + len(quest_handler.get_done())
        self.selected = self.get_selected_quest()

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.index == self.quest_num - 1:
                        self.index = 0
                    else:
                        self.index = min(self.quest_num - 1, self.index + 1)
                    self.selected = self.get_selected_quest()
                elif event.key == pygame.K_UP:
                    self.index -= 1
                    if self.index < 0:
                        self.index = self.quest_num - 1
                    self.selected = self.get_selected_quest()
                elif event.key == pygame.K_ESCAPE:
                    return self.prev_screen
        return self

    def display(self):
        super().display()

        self.draw_line((self.center_point, 0), (self.center_point, SCREEN_HEIGHT))

        y = 16
        y = self.draw_quest_titles("Quests", quest_handler.get(), y)
        if quest_handler.done:
            y = self.draw_quest_titles("Completed", quest_handler.get_done(), y)

        if self.selected:
            self.draw_quest_details(self.selected)
        else:
            x = (SCREEN_WIDTH - self.center_point) / 2 + self.center_point
            y = SCREEN_HEIGHT / 2 - FONT_HEIGHT / 2
            self.write_center_x("Arrow Keys to Select Quest", (x,y), GRAY)
            y += FONT_HEIGHT + 2
            self.write_center_x("[escape] to exit", (x,y), GRAY)

    def get_selected_quest(self):
        for i in range(self.quest_num):
            if i == self.index:
                return quest_handler.get(i)
        for j in range(len(quest_handler.get_done())):
            if j + self.quest_num == self.index:
                return quest_handler.get_done(j)
        return None

    def draw_quest_titles(self, header, quests, y):
        x = 16
        self.write(header, (x, y))
        y += FONT_HEIGHT + 2
        x += 8

        if quests:
            for q in quests:
                c = LIGHTGRAY
                if q == self.selected:
                    c = GREEN
                self.write(q.name, (x,y), c)
                y += FONT_HEIGHT + 2
        else:
            self.write("none", (x,y), GRAY)
            y += FONT_HEIGHT + 2
        return y + 8

    def draw_quest_details(self, quest):
        x = self.center_point + 16
        y = 16

        self.write(quest.name, (x, y), CYAN if quest.complete else WHITE)
        x += 8
        y += FONT_HEIGHT + 2
        lines = fit_text(quest.description, SCREEN_WIDTH - 48 - self.center_point)
        for line in lines:
            self.write(line, (x,y), LIGHTGRAY)
            y += FONT_HEIGHT + 2

        for step in quest.steps:
            if not step.is_enabled():
                continue
            y += 8
            self.write(step.name, (x, y), CYAN if step.complete else WHITE)
            y += FONT_HEIGHT + 2

            lines = fit_text(step.description, SCREEN_WIDTH - 56 - self.center_point)
            for line in lines:
                self.write(line, (x+8, y), LIGHTGRAY)
                y += FONT_HEIGHT + 2
