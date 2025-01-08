import pygame
from main.constants import *
from main.colour import *

NUMBERS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

def fit_text(text, width=SCREEN_WIDTH-32):
    max_char = int(width / FONT_WIDTH)

    words = iter(text.split())
    lines, current = [], next(words)
    current_len = get_word_len(current)
    for word in words:
        word_len = get_word_len(word)
        if current_len + 1 + word_len > max_char:
            lines.append(current)
            current = word
            current_len = word_len
        else:
            current += " " + word
            current_len += word_len + 1
    lines.append(current)
    return lines

def get_word_len(word):
    word_len = len(word)
    for colour_string in COLOUR_STRINGS:
        if colour_string in word:
            word_len -= len(colour_string) * word.count(colour_string)
    return word_len

creature_sprites = pygame.image.load('resources/creatures.png')
world_sprites = pygame.image.load('resources/world.png')
interface_sprites = pygame.image.load('resources/interface.png')
dungeon_sprites = pygame.image.load('resources/dungeons.png')
ARROW_UP = (0,0,12,12)
ARROW_RIGHT = (12,0,12,12)
ARROW_DOWN = (24,0,12,12)
ARROW_LEFT = (36,0,12,12)
def draw_sprite(surface, sprite_sheet, sprite_rect, x, y, scale=4):
    # This seems terribly inefficient
    width, height = sprite_rect[2], sprite_rect[3]
    cropped = pygame.Surface((width, height), pygame.SRCALPHA)
    cropped.blit(sprite_sheet, (0,0), sprite_rect)
    scaled = pygame.transform.scale(cropped, (width * scale, height * scale))
    surface.blit(scaled, (x,y))
