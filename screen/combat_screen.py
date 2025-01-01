import pygame
from screen.screen import Screen
from screen.game_over_screen import GameOverScreen
from main.constants import *
from main.messenger import get_messenger
from main.clock import get_clock
from main.util import draw_sprite, creature_sprites, interface_sprites, ARROW_DOWN
from creature.creature import Creature
from creature.player import Player
from combat.queue_item import *
from world.area import Area

messenger = get_messenger()
clock = get_clock()

ENEMY_KEYS = ['q','w','e','r']
PARTY_KEYS  = ['a', 's','d','f']

class CombatScreen(Screen):
    def __init__(self, canvas, area: Area, player: Player, last_screen: Screen =None):
        super().__init__(canvas)
        self.last_screen = last_screen
        self.area = area
        self.player = player

        messenger.clear_latest()

        self.queue: list[QueueItem] = []
        self.last_active_creature: Creature = None

        self.frame_timer = 0
        self.frame_num = 0
        self.max_frames = 4

    def check_events(self, events):
        if not self.queue:
            self.reset_queue()

        # If the head of the queue is a creature, check if they are alive and take their turn
        c = self.active_creature()
        if c and not c.is_alive():
            c = None
            self.queue.pop(0)

        if self.queue:
            if self.queue[0].is_type('wait'):
                self.queue[0].time -= clock.get_time()
                if self.queue[0].time <= 0:
                    self.queue.pop(0)

        self.frame_timer += clock.get_time()
        if self.frame_timer >= 250:
            self.frame_timer = 0
            self.frame_num += 1
            if self.frame_num >= self.max_frames:
                self.frame_num = 0

        # Some checks to see if combat should even continue
        if not self.player.is_alive():
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return GameOverScreen(self.canvas)
        elif not self.area.enemies:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # For now just assume this is an AreaScreen, it needs to refresh
                    if self.last_screen:
                        self.last_screen.initialize_area(self.area)
                    return self.last_screen

        # Player Controlled Turn
        elif c and c.ai is None:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    # Attack another creature
                    target = self.get_creature_by_code(event.key)
                    if target:
                        messenger.clear_latest()
                        c.attack(target)
                        self.queue.pop(0)

        # AI Controlled Turn
        elif c:
            c.take_turn(self.player, self.area)
            self.queue.pop(0)
            self.queue.insert(0, QueueWait(COMBAT_TURN_TIME))

        # This check probably doesn't need to happen once per frame
        to_remove = []
        for enemy in self.area.enemies:
            if not enemy.is_alive():
                to_remove.append(enemy)
        for enemy in to_remove:
            self.area.enemies.remove(enemy)

            # This will currently happen more than once if multiple final enemies die simultaneously
            if not self.area.enemies and self.player.is_alive():
                messenger.add("All enemies have been defeated.")
                messenger.add("Press [enter] to return.")

        return self

    def active_creature(self):
        # Get the first queue element
        # Once we add animation handling in the queue, this will need to be changed
        if self.queue:
            if self.queue[0].is_type('creature'):
                self.last_active_creature = self.queue[0].creature
                return self.queue[0].creature
        return None

    def reset_queue(self):
        q = []
        for e in self.area.enemies:
            if e.is_alive():
                q.append(QueueCreature(e))
        for p in self.player.party:
            if p.is_alive():
                q.append(QueueCreature(p))
        q.sort(key=lambda c: c.creature.speed, reverse=True)
        self.queue = q

    def get_creature_by_code(self, event_key):
        for i in range(len(ENEMY_KEYS)):
            if event_key == pygame.key.key_code(ENEMY_KEYS[i]):
                if i < len(self.area.enemies):
                    return self.area.enemies[i]
        for i in range(len(PARTY_KEYS)):
            if event_key == pygame.key.key_code(PARTY_KEYS[i]):
                if i < len(self.player.party):
                    return self.player.party[i]
        return None

    def display(self):
        super().display()

        c = self.last_active_creature
        if c:
            self.write(f"{c.name} Turn", (16, 16))

        segment_width = SCREEN_WIDTH / 2 / (len(self.player.party) + 1)
        x = segment_width
        y = SCREEN_HEIGHT / 2 - 72

        for i in range(len(self.player.party)):
            if self.player.party[i].is_alive():
                self.draw_creature(self.player.party[i], PARTY_KEYS[i], x, y)
                x += segment_width

        segment_width = SCREEN_WIDTH / 2 / (len(self.area.enemies) + 1)
        x = segment_width + SCREEN_WIDTH / 2
        for i in range(len(self.area.enemies)):
            self.draw_creature(self.area.enemies[i], ENEMY_KEYS[i], x, y)
            x += segment_width

        self.draw_messages()

    def draw_creature(self, creature, letter, x, y):
        if creature == self.last_active_creature:
            draw_sprite(self.canvas, interface_sprites, ARROW_DOWN, x - 24, y - 76 + self.frame_num * 4)
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
