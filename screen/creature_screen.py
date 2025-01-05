import pygame
from screen.screen import Screen
from creature.creature import Creature
from main.constants import *
from main.util import draw_sprite, creature_sprites, fit_text

class CreatureScreen(Screen):
    def __init__(self, canvas, creature: Creature, prev_screen: Screen):
        super().__init__(canvas)
        self.creature = creature
        self.prev_screen = prev_screen
        self.desc_lines = fit_text(creature.description, SCREEN_WIDTH - 256 - 24 - 20)

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.prev_screen
        return self

    def display(self):
        super().display()

        self.draw_portrait(24, 24)
        self.draw_health(148, 84)
        self.draw_combat_stats(24, 136)
        self.write_description(256, 136)

    def draw_portrait(self, x, y):
        # Character tiles are 12x12, scaled by 6 they are 72x72, +12 for box border, +12 for some extra space
        self.draw_box((x, y, 96, 96))
        draw_sprite(self.canvas, creature_sprites, self.creature.sprite_rect, x + 12, y + 12, scale=6)

        # Write name, level, and profession
        x, y = 136, y + 12
        self.write(self.creature.name.upper(), (x, y))
        y += FONT_HEIGHT + 2
        prof_string = f"Level {self.creature.level}"
        if self.creature.profession:
            prof_string += f" {self.creature.profession}"
        self.write(prof_string, (x, y), LIGHTGRAY)

    def draw_health(self, x, y):
        rect_x = x + FONT_WIDTH * 12 + 12
        if self.creature.armor > 0:
            self.write(f"Armor: {self.creature.armor}/{self.creature.max_armor}", (x, y))
            armor_width = int(120 * (self.creature.armor / self.creature.max_armor))
            armor_rect = (rect_x, y, armor_width, FONT_HEIGHT)
            full_armor_rect = (rect_x, y, 120, FONT_HEIGHT)
            pygame.draw.rect(self.canvas, DIMGRAY, full_armor_rect)
            pygame.draw.rect(self.canvas, TURQOISE, armor_rect)
            y += FONT_HEIGHT + 2
        self.write(f"   HP: {self.creature.hp}/{self.creature.max_hp}", (x, y))
        health_width = int(120 * (self.creature.hp / self.creature.max_hp))
        health_rect = (rect_x, y, health_width, FONT_HEIGHT)
        full_health_rect = (rect_x, y, 120, FONT_HEIGHT)
        pygame.draw.rect(self.canvas, DIMGRAY, full_health_rect)
        pygame.draw.rect(self.canvas, RED, health_rect)
        y += FONT_HEIGHT + 16

    def draw_combat_stats(self, x, y):
        self.draw_box((x, y, 224, 174))
        x += 10
        y += 10
        for stat in [
            ("Speed", self.creature.speed),
            ("Strength", self.creature.strength),
            ("Dexterity", self.creature.dexterity),
            ("Intelligence", self.creature.intelligence),
            ("Dodge", self.creature.dodge),
            ("Will", self.creature.will),
            ("Endurance", self.creature.endurance)
        ]:
            self.write(f"{stat[0]}: {stat[1]}", (x, y))
            y += FONT_HEIGHT + 4

    def write_description(self, x, y):
        self.draw_box((x, y, SCREEN_WIDTH - x - 24, SCREEN_HEIGHT - y - 24))
        y += 10
        for line in self.desc_lines:
            self.write(line, (x + 10, y), LIGHTGRAY)
            y += FONT_HEIGHT + 2

        y += 8
        for ability in self.creature.abilities:
            self.draw_line((x,y), (SCREEN_WIDTH - 30, y), width=4)
            y += 8
            self.write(ability.name, (x + 10,y))
            y += FONT_HEIGHT + 2
            lines = fit_text(ability.description, SCREEN_WIDTH - 256 - 20 - 24 - 20)
            for line in lines:
                self.write(line, (x + 20, y), LIGHTGRAY)
                y += FONT_HEIGHT + 2
