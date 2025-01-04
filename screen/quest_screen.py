import pygame
from screen.screen import Screen
from creature.player import Player
from main.constants import *
from main.util import fit_text

class QuestScreen(Screen):
    def __init__(self, canvas, player: Player, prev_screen: Screen):
        super().__init__(canvas)
        self.player = player
        self.prev_screen = prev_screen
        self.center_point = SCREEN_WIDTH / 3

        self.index = -1
        self.selected = self.get_selected_quest()
        self.quest_num = len(self.player.main_quests) + len(self.player.side_quests)

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
        y = self.draw_quest_titles("Main Quests", self.player.main_quests, y)
        y = self.draw_quest_titles("Side Quests", self.player.side_quests, y)

        if self.selected:
            self.draw_quest_details(self.selected)
        else:
            x = (SCREEN_WIDTH - self.center_point) / 2 + self.center_point
            y = SCREEN_HEIGHT / 2 - FONT_HEIGHT / 2
            self.write_center_x("Arrow Keys to Select Quest", (x,y), GRAY)
            y += FONT_HEIGHT + 2
            self.write_center_x("[escape] to exit", (x,y), GRAY)

    def get_selected_quest(self):
        for i in range(len(self.player.main_quests)):
            if i == self.index:
                return self.player.main_quests[i]
        for j in range(len(self.player.side_quests)):
            if j + len(self.player.main_quests) == self.index:
                return self.player.side_quests[j]
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
