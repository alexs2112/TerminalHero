import pygame
from screen.screen import Screen
from screen.game_over_screen import GameOverScreen
from main.constants import *
from main.messenger import *
from main.util import draw_sprite, creature_sprites
from world.area import Area

messenger = get_messenger()

ENEMY_KEYS = ['q','w','e','r']
ALLY_KEYS  = ['s','d','f']
PLAYER_KEY = 'a'

class CombatScreen(Screen):
    def __init__(self, canvas, area: Area, last_screen=None):
        super().__init__(canvas)
        self.last_screen = last_screen
        self.area = area
        messenger.clear_latest()

    def check_events(self, events):
        # Don't let the player do multiple things at once
        turn_taken = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                messenger.clear_latest()
                if event.key == pygame.K_RETURN:
                    if not self.area.player.is_alive():
                        return GameOverScreen(self.canvas)

                    if not self.area.enemies:
                        # For now just assume this is an AreaScreen, it needs to refresh
                        if self.last_screen:
                            self.last_screen.initialize_area(self.area)
                        return self.last_screen

                # Attack another creature
                target = self.get_creature_by_code(event.key)
                if target:
                    self.area.player.attack(target)
                    turn_taken = True

        # Enemies take their turns after the player
        if turn_taken:
            self.enemy_turns()

        # Remove creatures that have died
        to_remove = []
        for i in range(len(self.area.allies)):
            if not self.area.allies[i].is_alive():
                to_remove.append(i)
        for i in to_remove:
            self.area.allies.pop(i)
        to_remove.clear()
        for i in range(len(self.area.enemies)):
            if not self.area.enemies[i].is_alive():
                to_remove.append(i)
        for i in to_remove:
            self.area.enemies.pop(i)
            if not self.area.enemies and self.area.player.is_alive():
                messenger.add("All enemies have been defeated.")
                messenger.add("Press [enter] to return.")

        return self

    def get_creature_by_code(self, event_key):
        for i in range(len(ENEMY_KEYS)):
            if event_key == pygame.key.key_code(ENEMY_KEYS[i]):
                if i < len(self.area.enemies):
                    return self.area.enemies[i]
        if event_key == pygame.key.key_code(PLAYER_KEY):
            return self.area.player
        for i in range(len(ALLY_KEYS)):
            if event_key == pygame.key.key_code(ALLY_KEYS[i]):
                if i < len(self.area.allies):
                    return self.area.allies[i]
        return None

    def enemy_turns(self):
        for e in self.area.enemies:
            if e.is_alive():
                e.take_turn(self.area)

    def display(self):
        super().display()

        segment_width = SCREEN_WIDTH / 2 / (len(self.area.allies) + 2) # + 1 for the player
        x = segment_width
        y = SCREEN_HEIGHT / 2 - 72

        if self.area.player.is_alive():
            self.draw_creature(self.area.player, PLAYER_KEY, x, y)
            x += segment_width

        for i in range(len(self.area.allies)):
            self.draw_creature(self.area.allies[i], ALLY_KEYS[i], x, y)
            x += segment_width

        segment_width = SCREEN_WIDTH / 2 / (len(self.area.enemies) + 1)
        x = segment_width + SCREEN_WIDTH / 2
        for i in range(len(self.area.enemies)):
            self.draw_creature(self.area.enemies[i], ENEMY_KEYS[i], x, y)
            x += segment_width

        self.draw_messages()

    def draw_creature(self, creature, letter, x, y):
        draw_sprite(self.canvas, creature_sprites, creature.sprite_rect, x - 36, y, scale=6)
        y += 100

        text = self.font.render(f"{letter}:{creature.name}", False, WHITE)
        self.canvas.blit(text, text.get_rect(center=(x, y)))

        y += 16
        armor_width = int(80 * (creature.armor / creature.max_armor))
        armor_rect = (x - 40, y, armor_width, 8)
        full_armor_rect = (x - 40, y, 80, 8)
        pygame.draw.rect(self.canvas, DIMGRAY, full_armor_rect)
        pygame.draw.rect(self.canvas, TURQOISE, armor_rect)

        y += 8
        health_width = int(80 * (creature.hp / creature.max_hp))
        health_rect = (x - 40, y, health_width, 8)
        full_health_rect = (x - 40, y, 80, 8)
        pygame.draw.rect(self.canvas, DIMGRAY, full_health_rect)
        pygame.draw.rect(self.canvas, RED, health_rect)
