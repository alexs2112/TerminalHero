from main.constants import *
from main.util import world_sprites, draw_sprite
from screen.screen import Screen
from world.world import World

class WorldScreen(Screen):
    def __init__(self, canvas, world: World):
        super().__init__(canvas)
        self.world = world
        self.center_x = SCREEN_WIDTH / 2 + 64

    def display(self):
        super().display()
        self.draw_box((8, 8, SCREEN_WIDTH-16, SCREEN_HEIGHT-16))
        self.draw_line((self.center_x, 10), (self.center_x, SCREEN_HEIGHT - 10))
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
