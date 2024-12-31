import pygame
from main.constants import *

NUMBERS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

def fit_text(text, width=SCREEN_WIDTH-32):
    max_char = int(width / FONT_WIDTH)

    words = iter(text.split())
    lines, current = [], next(words)
    for word in words:
        if len(current) + 1 + len(word) > max_char:
            lines.append(current)
            current = word
        else:
            current += " " + word
    lines.append(current)
    return lines

creature_sprites = pygame.image.load('resources/onebit.png')
world_sprites = pygame.image.load('resources/world.png')
interface_sprites = pygame.image.load('resources/interface.png')
ARROW_UP = (1,1,12,12)
ARROW_RIGHT = (14,1,12,12)
ARROW_DOWN = (27,1,12,12)
ARROW_LEFT = (40,1,12,12)
def draw_sprite(surface, sprite_sheet, sprite_rect, x, y, scale=4):
    # This seems terribly inefficient
    width, height = sprite_rect[2], sprite_rect[3]
    cropped = pygame.Surface((width, height))
    cropped.blit(sprite_sheet, (0,0), sprite_rect)
    scaled = pygame.transform.scale(cropped, (width * scale, height * scale))
    surface.blit(scaled, (x,y))
