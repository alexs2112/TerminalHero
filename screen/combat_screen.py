import pygame
from screen.screen import Screen
from screen.game_over_screen import GameOverScreen
from main.constants import *
from creature.creature import Creature
from creature.player import Player
from creature.ai.basic_ai import BasicAI

ENEMY_KEYS = ['q','w','e','r']
ALLY_KEYS  = ['a','s','d','f']

class CombatScreen(Screen):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.player = None
        self.allies = []
        self.enemies = []
        self.test_setup()

    def test_setup(self):
        self.player = Player("Player", (1,1,12,12), 10, 2, 5, 5)
        self.allies.append(self.player)

        self.enemies = [
            Creature("Goblin", (1,27,12,12), 5, 1, 2, 3),
            Creature("Kobold", (1,40,12,12), 3, 1, 2, 3),
            Creature("Harold", (1,53,12,12), 4, 4, 2, 3)
        ]
        for e in self.enemies:
            e.ai = BasicAI(e)

    def check_events(self, events):
        # Don't let the player do multiple things at once
        turn_taken = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

                if not self.player.is_alive():
                    return GameOverScreen(self.canvas)

                # Attack another creature
                target = self.get_creature_by_code(event.key)
                if target:
                    self.player.attack(target)
                    turn_taken = True

        # Enemies take their turns after the player
        if turn_taken:
            self.enemy_turns()
        
        # Remove creatures that have died
        to_remove = []
        for i in range(len(self.allies)):
            if not self.allies[i].is_alive():
                to_remove.append(i)
        for i in to_remove:
            self.allies.pop(i)
        to_remove.clear()
        for i in range(len(self.enemies)):
            if not self.enemies[i].is_alive():
                to_remove.append(i)
        for i in to_remove:
            self.enemies.pop(i)

        return self

    def get_creature_by_code(self, event_key):
        for i in range(len(ENEMY_KEYS)):
            if event_key == pygame.key.key_code(ENEMY_KEYS[i]):
                return self.enemies[i]
        for i in range(len(ALLY_KEYS)):
            if event_key == pygame.key.key_code(ALLY_KEYS[i]):
                return self.allies[i]
        return None

    def enemy_turns(self):
        for e in self.enemies:
            if (e.is_alive()):
                e.take_turn(self.allies, self.enemies)

    def display(self):
        self.canvas.fill(BLACK)
        text = self.font.render('Hello World', True, WHITE)
        self.canvas.blit(text, (10, 10))

        segment_width = SCREEN_WIDTH / 2 / (len(self.allies) + 1)
        x = segment_width
        y = SCREEN_HEIGHT / 2 - 60
        for i in range(len(self.allies)):
            self.draw_creature(self.allies[i], ALLY_KEYS[i], x, y)
            x += segment_width

        segment_width = SCREEN_WIDTH / 2 / (len(self.enemies) + 1)
        x = segment_width + SCREEN_WIDTH / 2
        for i in range(len(self.enemies)):
            self.draw_creature(self.enemies[i], ENEMY_KEYS[i], x, y)
            x += segment_width

    def draw_creature(self, creature, letter, x, y):
        creature.draw_sprite(self.canvas, x - 36, y)
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
