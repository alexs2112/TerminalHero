import pygame
from main.constants import *
from main.colour import *
from main.util import world_sprites, draw_sprite, draw_creature
from main.clock import get_clock
from screen.screen import Screen
from screen.area_screen import AreaScreen
from screen.quest_screen import QuestScreen
from screen.inventory_screen import InventoryScreen
from screen.creature_screen import CreatureScreen
from screen.escape_screen import EscapeScreen
from world.world import World

clock = get_clock()

class WorldScreen(Screen):
    def __init__(self, canvas, world: World):
        super().__init__(canvas)
        self.world = world
        self.player = self.world.player
        self.center_x = SCREEN_WIDTH / 2 + 64
        self.local_time = 0
        self.frame_num = 0

        self.known_areas = []
        self.index = 0
        self.refresh()

    def refresh(self, **kwargs):
        self.known_areas = self.world.get_known_areas()
        if self.player.area:
            self.index = self.known_areas.index(self.player.area)
        else:
            self.move_into(self.known_areas[0])

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.frame_num = 0
                self.local_time = 0
                if event.key == pygame.K_DOWN:
                    self.index = min(self.index + 1, len(self.known_areas) - 1)
                    self.move_into(self.known_areas[self.index])
                elif event.key == pygame.K_UP:
                    self.index = max(self.index - 1, 0)
                    self.move_into(self.known_areas[self.index])
                elif event.key == pygame.K_RETURN:
                    return AreaScreen(self.canvas, self.known_areas[self.index], self.world.player, self)
                elif event.key == pygame.K_l:
                    return QuestScreen(self.canvas, self)
                elif event.key == pygame.K_i:
                    return InventoryScreen(self.canvas, self.world.player, self)
                elif event.key == pygame.K_c:
                    return CreatureScreen(self.canvas, self.world.player, self)
                elif event.key == pygame.K_ESCAPE:
                    return EscapeScreen(self.canvas, self, can_save = True, load_screen = 'world')
        return self

    def move_into(self, area):
        self.player.area = area
        area.player = self.player

    def display(self):
        super().display()

        self.local_time += clock.get_time()
        if self.local_time >= 500:
            self.local_time = 0
            self.frame_num = 1 - self.frame_num

        self.draw_line((self.center_x, 0), (self.center_x, SCREEN_HEIGHT))
        self.draw_world()
        self.list_known_areas()
        self.display_notifications()

    def draw_world(self):
        # For now, just start at (0,0)
        # This can be revisited when we draw proper world sprites
        tile_size = WORLD_TILE_SIZE * WORLD_TILE_MODIFIER + 2
        for area in self.known_areas:
            x,y = self.world.positions[area]
            draw_sprite(self.canvas, world_sprites, area.sprite_rect, x * tile_size, y * tile_size, scale=WORLD_TILE_MODIFIER)
        
        # For now, just draw filler
        for area in [ a for a in self.world.areas if a.is_filler ]:
            x,y = self.world.positions[area]
            draw_sprite(self.canvas, world_sprites, area.sprite_rect, x * tile_size, y * tile_size, scale=WORLD_TILE_MODIFIER)

        if self.frame_num == 0:
            x,y = self.world.positions[self.player.area]
            px = x * tile_size
            py = y * tile_size
            draw_creature(self.canvas, self.player.get_sprite(), self.player.sprite.dimensions(), (px,py), scale=4)

    def list_known_areas(self):
        i = 1
        x = self.center_x + 16
        y = 24
        for area in self.known_areas:
            colour = WHITE
            if (i - 1) == self.index:
                colour = GREEN
            self.write(f"{i}) {area.name}", (x,y), colour)
            y += FONT_HEIGHT + 2
            if (i - 1) == self.index:
                for feature in area.enabled_features():
                    self.write(feature.name, (x + FONT_WIDTH * 3, y))
                    y += FONT_HEIGHT + 2
            i += 1
