import pygame
from screen.screen import Screen
from screen.world_screen import WorldScreen
from world.world_builder import get_world
from creature.player import Player
from creature.creature_factory import get_creature_factory
from item.item import WEAPON, ARMOR, TRINKET
from main.constants import *
from main.colour import *
from main.util import fit_text, draw_creature

creatures = get_creature_factory()

PROFESSIONS = [
    'champion',
    'duelist',
    'elementalist',
    'luminarch'
]
class ProfessionScreen(Screen):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.index = 0

        self.players = self.initialize_players()

    def initialize_players(self) -> list[Player]:
        players = []
        for p in PROFESSIONS:
            players.append(creatures.new_player(p))
        return players

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.index += 1
                    if self.index >= len(self.players):
                        self.index = 0
                elif event.key == pygame.K_UP:
                    self.index -= 1
                    if self.index < 0:
                        self.index = len(self.players) - 1
                elif event.key == pygame.K_RETURN:
                    world = get_world()
                    world.player = self.players[self.index]
                    return WorldScreen(self.canvas, world)
        return self

    def display(self):
        super().display()
        box_size = 72 + 16
        x = 24
        y = SCREEN_HEIGHT / 2 - box_size - box_size / 2
        y -= (box_size + 8) * self.index

        for i in range(len(self.players)):
            self.draw_box((x, y, box_size, box_size), 4, GREEN if i == self.index else LIGHTGRAY)
            draw_creature(self.canvas, self.players[i].get_sprite(), (12,12), (x + 8, y + 8), scale=6)
            y += (box_size + 8)

        # Make sure the portraits don't overlap the border
        self.draw_line((0,2), (160,2))
        self.draw_line((0,SCREEN_HEIGHT - 4), (160,SCREEN_HEIGHT - 4))

        desc_start = box_size + x * 2
        x = (SCREEN_WIDTH - desc_start) / 2 + desc_start
        y = 24

        self.write_center_x("Choose Your Profession", (x,y))
        y += FONT_HEIGHT + 4
        self.write_center_x("arrow keys to navigate", (x,y), GRAY)
        y += FONT_HEIGHT + 24

        p = self.players[self.index]
        self.write(p.profession.name, (desc_start + 16, y))
        y += FONT_HEIGHT + 8

        lines = fit_text(p.profession.description, SCREEN_WIDTH - desc_start - 48)
        for l in lines:
            self.write(l, (desc_start + 24, y), LIGHTGRAY)
            y += FONT_HEIGHT + 2
        y += 16
        self.write(self.get_equipment_text(p), (desc_start + 24, y), WHITE)
        y += FONT_HEIGHT + 6
        self.write(self.get_ability_text(p), (desc_start + 24, y), WHITE)

        self.write_center_x("press [enter] to continue", (x, SCREEN_HEIGHT - FONT_HEIGHT - 16), GRAY)

    def get_equipment_text(self, player):
        out = "Starts equipped with a "
        if player.equipment[WEAPON]:
            out += player.equipment[WEAPON].name
        if player.equipment[ARMOR]:
            if player.equipment[TRINKET]:
                out += ', a '
            else:
                out += ' and a '
            out += player.equipment[ARMOR].name
        if player.equipment[TRINKET]:
            if player.equipment[ARMOR]:
                out += ','
            out += f" and a {player.equipment[TRINKET].name}"
        out += '.'
        return out

    def get_ability_text(self, player):
        out = "Skills: "
        for i in range(len(player.profession.abilities)):
            out += player.profession.abilities[i].name
            if i < len(player.profession.abilities) - 1:
                out += ', '
        return out
