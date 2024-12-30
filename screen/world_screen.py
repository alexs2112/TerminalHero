import pygame
from main.constants import *
from main.util import world_sprites, creature_sprites, draw_sprite
from screen.screen import Screen
from screen.area_screen import AreaScreen
from world.world import World

class WorldScreen(Screen):
    def __init__(self, canvas, world: World, start_area=None):
        super().__init__(canvas)
        self.world = world
        self.center_x = SCREEN_WIDTH / 2 + 64
        self.clock = pygame.time.Clock()
        self.local_time = 0
        self.frame_num = 0

        self.known_areas = self.initialize_areas()
        self.index = self.index_by_area(start_area)

    def initialize_areas(self):
        out = {}
        for x in range(self.world.width):
            for y in range(self.world.height):
                if self.world.areas[x][y].condition_met() and not self.world.areas[x][y].is_filler:
                    out[(x,y)] = self.world.areas[x][y]
        return out

    def index_by_area(self, area):
        if area is None:
            return 0
        areas = list(self.known_areas.values())
        for i in range(len(areas)):
            if areas[i] == area:
                return i
        return 0

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.index = min(self.index + 1, len(self.known_areas) - 1)
                elif event.key == pygame.K_UP:
                    self.index = max(self.index - 1, 0)
                self.frame_num = 0
                self.local_time = 0
                if event.key == pygame.K_RETURN:
                    return AreaScreen(self.canvas, self.area_by_index(self.index), self.world)
        return self

    def display(self):
        super().display()

        self.local_time += self.clock.tick()
        if self.local_time >= 500:
            self.local_time = 0
            self.frame_num = 1 - self.frame_num

        self.draw_line((self.center_x, 0), (self.center_x, SCREEN_HEIGHT))
        self.draw_world()

    def draw_world(self):
        start_x = self.center_x / 2 - ((self.world.width / 2) * (WORLD_TILE_WIDTH * WORLD_TILE_MODIFIER + 2))
        start_y = SCREEN_HEIGHT / 2 - ((self.world.height / 2) * (WORLD_TILE_HEIGHT * WORLD_TILE_MODIFIER + 2))

        draw_x = start_x
        for x in range(self.world.width):
            draw_y = start_y
            for y in range(self.world.height):
                if self.world.areas[x][y].condition_met():
                    sprite_rect = self.world.get_area_sprite_rect(x, y)
                    draw_sprite(self.canvas, world_sprites, sprite_rect, draw_x, draw_y, scale=4)
                draw_y += WORLD_TILE_HEIGHT * WORLD_TILE_MODIFIER + 2
            draw_x += WORLD_TILE_WIDTH * WORLD_TILE_MODIFIER + 2

        if self.frame_num == 0:
            cx, cy = self.pos_by_index(self.index)
            player_x = start_x + cx * (WORLD_TILE_WIDTH * WORLD_TILE_MODIFIER + 2)
            player_y = start_y + cy * (WORLD_TILE_HEIGHT * WORLD_TILE_MODIFIER + 2)
            draw_sprite(self.canvas, creature_sprites, self.world.player.sprite_rect, player_x, player_y, scale=4)

        self.list_known_areas()

    def pos_by_index(self, index):
        areas = list(self.known_areas)
        if index >= 0 and index < len(areas):
            return areas[index]
        return areas[0]

    def area_by_index(self, index):
        areas = list(self.known_areas.values())
        print(areas)
        if index >= 0 and index < len(areas):
            return areas[index]
        return areas[0]

    def list_known_areas(self):
        i = 1
        x = self.center_x + 16
        y = 24
        for area in self.known_areas.values():
            colour = WHITE
            if (i - 1) == self.index:
                colour = GREEN
            self.write(f"{i}) {area.name}", (x,y), colour)
            y += FONT_HEIGHT + 2
            if (i - 1) == self.index:
                for npc in area.npcs:
                    self.write(npc.name, (x + FONT_WIDTH * 3, y))
                    y += FONT_HEIGHT + 2
                for enemy in area.enemies:
                    self.write(enemy.name, (x + FONT_WIDTH * 3, y), RED)
                    y += FONT_HEIGHT + 2
            i += 1
