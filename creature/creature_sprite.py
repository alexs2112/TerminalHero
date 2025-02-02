import pygame
from item.item import ARMOR, WEAPON
from main.util import creature_sprites
equipped_sprites = pygame.image.load('resources/equipped.png')

class CreatureSprite:
    def __init__(self, sprite_rect, dead_rect):
        self.sprite_rect = sprite_rect
        self.dead_rect = dead_rect
        self.cached = None
        self.dead_cached = None
        self.width = sprite_rect[2]
        self.height = sprite_rect[3]

    def update(self, _):
        cached = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        cached.blit(creature_sprites, (0,0), self.sprite_rect)
        self.cached = cached
        self.update_dead()

    def update_dead(self):
        if not self.dead_cached:
            cached = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            cached.blit(creature_sprites, (0,0), self.dead_rect)
            self.dead_cached = cached

    def get_sprite(self, creature):
        if creature.is_alive():
            return self.cached
        return self.dead_cached

    def dimensions(self):
        return (self.width, self.height)

class ModularSprite(CreatureSprite):
    def update(self, creature):
        cached = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        cached.blit(creature_sprites, (0,0), self.sprite_rect)
        if creature.equipment[ARMOR] and creature.equipment[ARMOR].equipped_sprite_rect:
            cached.blit(equipped_sprites, (0,0), creature.equipment[ARMOR].equipped_sprite_rect)
        if creature.equipment[WEAPON] and creature.equipment[WEAPON].equipped_sprite_rect:
            cached.blit(equipped_sprites, (0,0), creature.equipment[WEAPON].equipped_sprite_rect)
        self.cached = cached
        self.update_dead()
