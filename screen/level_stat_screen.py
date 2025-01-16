import pygame
from main.constants import *
from main.util import *
from screen.screen import Screen
from creature.creature import Creature

# Some constant rects for UI elements
RIGHT_ARROW = (12,12,12,12)
LEFT_ARROW  = (36,12,12,12)
NUMBERS_START = (0,24)

# These icons should be changed to something cool
STR_ICON = (0,36,12,12)
DEX_ICON = (12,36,12,12)
INT_ICON = (24,36,12,12)

class LevelStatScreen(Screen):
    def __init__(self, canvas, creature: Creature, last_screen: Screen):
        super().__init__(canvas)
        self.creature = creature
        self.last_screen = last_screen

        self.index = 0
        self.points = creature.stat_points
        self.base_stats = {
            'STR': creature.stats['strength'],
            'DEX': creature.stats['dexterity'],
            'INT': creature.stats['intelligence']
        }
        self.stats = self.base_stats.copy()
        self.stat_names = [ 'STR', 'DEX', 'INT' ]

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.index += 1
                    if self.index == 3:
                        self.index = 0
                elif event.key == pygame.K_UP:
                    self.index -= 1
                    if self.index < 0:
                        self.index = 3
                elif event.key == pygame.K_LEFT:
                    current = self.stat_names[self.index]
                    if self.stats[current] > self.base_stats[current]:
                        self.stats[current] -= 1
                        self.points += 1
                elif event.key == pygame.K_RIGHT:
                    current = self.stat_names[self.index]
                    if self.points > 0:
                        self.stats[current] += 1
                        self.points -= 1
                elif event.key == pygame.K_RETURN:
                    self.finalize_changes()
                    # May need to refresh last screen from here?
                    return self.last_screen
                elif event.key == pygame.K_ESCAPE:
                    return self.last_screen
        return self

    def finalize_changes(self):
        name_to_stat = {
            'STR': 'strength',
            'DEX': 'dexterity',
            'INT': 'intelligence'
        }
        for stat, value in self.stats.items():
            s = name_to_stat[stat]
            self.creature.stats[s] = value
        self.creature.stat_points = self.points

    def display(self):
        super().display()

        # Draw character portrait, name, and profession
        x = 64
        y = SCREEN_HEIGHT / 2 - 48
        self.write(self.creature.name, (x,y))
        y += FONT_HEIGHT + 6
        self.draw_box((x, y, 64, 64))
        draw_sprite(self.canvas, creature_sprites, self.creature.get_sprite_rect(), x + 8, y + 8)
        x += 32
        y += 72
        self.write_center_x(f"Level {self.creature.level}", (x,y), LIGHTGRAY)
        y += FONT_HEIGHT + 2
        self.write_center_x(self.creature.profession.name, (x,y), LIGHTGRAY)

        # Draw stats
        x += 184
        y = 64
        self.write(f"Stat Points: {self.points}", (x - 32,y))

        y = (SCREEN_HEIGHT - 64 * 3) / 2
        i = 0
        for stat in self.stat_names:
            self.draw_stat(stat, x, y, i == self.index)
            y += 76
            i += 1

    def draw_stat(self, stat, x, y, selected):
        c = GRAY
        if selected:
            c = GREEN
        elif self.stats[stat] > self.base_stats[stat]:
            c = CYAN

        self.draw_box((x,y,56*2,56), width=4, colour=c)
        r = {
            'STR': STR_ICON,
            'DEX': DEX_ICON,
            'INT': INT_ICON
        }[stat]
        draw_sprite(self.canvas, interface_sprites, r, x+4, y+4)
        self.draw_line((x + 56, y), (x + 56, y + 52), width=4, colour=c)

        r = (NUMBERS_START[0] + self.stats[stat] * 12, NUMBERS_START[1], 12, 12)
        draw_sprite(self.canvas, interface_sprites, r, x + 60, y + 4)

        if selected:
            if self.stats[stat] > self.base_stats[stat]:
                draw_sprite(self.canvas, interface_sprites, LEFT_ARROW, x - 64, y)
            if self.points > 0:
                draw_sprite(self.canvas, interface_sprites, RIGHT_ARROW, x + 128, y)
