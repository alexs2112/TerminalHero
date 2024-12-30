import pygame
from main.constants import *
from main.util import world_sprites, creature_sprites, draw_sprite, fit_text
from screen.screen import Screen
from screen.area_screen import AreaScreen
from world.world import World

class WorldScreen(Screen):
    def __init__(self, canvas, world: World):
        super().__init__(canvas)
        self.world = world
        self.center_x = SCREEN_WIDTH / 2 + 64
        self.clock = pygame.time.Clock()
        self.local_time = 0
        self.frame_num = 0

    def check_events(self, events):
        x,y = self.world.player_position
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x = min(x + 1, self.world.width - 1)
                elif event.key == pygame.K_LEFT:
                    x = max(x - 1, 0)
                elif event.key == pygame.K_DOWN:
                    y = min(y + 1, self.world.height - 1)
                elif event.key == pygame.K_UP:
                    y = max(y - 1, 0)
                if (x,y) != self.world.player_position:
                    self.world.player_position = (x,y)
                    self.frame_num = 0
                    self.local_time = 0
                if event.key == pygame.K_RETURN:
                    return AreaScreen(self.canvas, self.world.areas[x][y], self.world)
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
                sprite_rect = self.world.get_area_sprite_rect(x, y)
                draw_sprite(self.canvas, world_sprites, sprite_rect, draw_x, draw_y, scale=4)
                draw_y += WORLD_TILE_HEIGHT * WORLD_TILE_MODIFIER + 2
            draw_x += WORLD_TILE_WIDTH * WORLD_TILE_MODIFIER + 2

        if self.frame_num == 0:
            player_x = start_x + self.world.player_position[0] * (WORLD_TILE_WIDTH * WORLD_TILE_MODIFIER + 2)
            player_y = start_y + self.world.player_position[1] * (WORLD_TILE_HEIGHT * WORLD_TILE_MODIFIER + 2)
            draw_sprite(self.canvas, creature_sprites, self.world.player.sprite_rect, player_x, player_y, scale=4)

        self.draw_tile_info(self.world.player_position[0], self.world.player_position[1])

    def draw_tile_info(self, x, y):
        tile = self.world.areas[x][y]
        self.write_center_x(tile.name, ((SCREEN_WIDTH - self.center_x) / 2 + self.center_x, 24))

        x = self.center_x + 16
        y = 24 + FONT_HEIGHT + 16
        lines = fit_text(tile.description, SCREEN_WIDTH - self.center_x - 32)
        for line in lines:
            self.write(line, (x, y))
            y += FONT_HEIGHT + 2

        y += 12
        if tile.npcs:
            self.write("Notable People:", (x,y))
            y += FONT_HEIGHT + 2

        for npc in tile.npcs:
            self.write(npc.name, (x+12,y), GREEN)
            y += FONT_HEIGHT + 2

        y += 12
        if tile.enemies:
            self.write("Hostiles:", (x,y))
            y += FONT_HEIGHT + 2

        for enemy in tile.enemies:
            self.write(enemy.name, (x+12, y), RED)
            y += FONT_HEIGHT + 2
