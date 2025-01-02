import pygame
from screen.screen import Screen
from screen.game_over_screen import GameOverScreen
from main.constants import *
from main.util import NUMBERS
from main.messenger import get_messenger
from main.clock import get_clock
from main.util import draw_sprite, creature_sprites, interface_sprites, ARROW_DOWN
from creature.creature import Creature
from creature.player import Player
from combat.queue_item import *
from combat.bump_location import BumpLocation
from combat.ability import Ability
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
        self.selected_ability: Ability = None

        self.frame_timer = 0
        self.frame_num = 0
        self.max_frames = 4
        self.bump_locations: dict[Creature,BumpLocation] = {}

    def check_events(self, events):
        if not self.queue:
            self.reset_queue()

        # If the head of the queue is a creature, check if they are still alive and take their turn
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
        self.update_bumps(clock.get_time())

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
                    # Player selects the ability to use if one is not already selected
                    if not self.selected_ability:
                        if event.key in NUMBERS:
                            i = int(pygame.key.name(event.key)) - 1
                            if i < len(c.abilities):
                                if c.abilities[i].is_usable():
                                    self.selected_ability = c.abilities[i]
                                    return self
                                else:
                                    messenger.add("This ability is still on cooldown.")
                                    return self
                        # Skip turn
                        elif event.key == pygame.K_0:
                            messenger.add(f"{c.name} skips their turn.")
                            self.queue.pop(0)
                    # If the ability to use is already selected:
                    else:
                        # Target another creature
                        target = self.get_creature_by_code(event.key)
                        if target:
                            self.bump_locations[c] = BumpLocation((COMBAT_BUMP_DISTANCE, 0), 100)
                            c.use_ability(self.selected_ability, target)
                            self.selected_ability = None
                            self.queue.pop(0)
                            self.queue.insert(0, QueueWait(COMBAT_TURN_TIME))
                        elif event.key == pygame.K_ESCAPE:
                            self.selected_ability = None
                            return self

        # AI Controlled Turn
        elif c:
            c.take_turn(self.player, self.area)

            # For now just assume the enemy is only attacking
            self.bump_locations[c] = BumpLocation((-COMBAT_BUMP_DISTANCE, 0), 100)

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

        return self

    def active_creature(self):
        # Get the first queue element
        # Once we add animation handling in the queue, this will need to be changed
        if self.queue:
            if self.queue[0].is_type('creature'):

                # Not super happy with having this here
                if self.last_active_creature != self.queue[0].creature:
                    messenger.clear_latest()
                    was_alive = self.queue[0].creature.is_alive()
                    self.queue[0].creature.start_turn()
                    if self.queue[0].creature.is_alive() != was_alive:
                        # was_alive is a lazy solution here
                        # Problem: Enemy dies to effect at the start of their turn, instantly skips to the next turn
                        self.queue.pop(0)
                        self.queue.insert(0, QueueWait(COMBAT_TURN_TIME))
                        return None

                self.last_active_creature = self.queue[0].creature

                # This could probably be cleaned up a bit
                if self.queue[0].creature.skip_next_turn:
                    self.queue.pop(0)
                    self.queue.insert(0, QueueWait(COMBAT_TURN_TIME))
                    return None

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

    def update_bumps(self, time):
        for c, b in self.bump_locations.items():
            if b and b.finished():
                self.bump_locations[c] = None
        for bump in self.bump_locations.values():
            if bump:
                bump.update(time)

    def display(self):
        super().display()

        c = self.last_active_creature
        if c:
            self.write(f"{c.name} Turn", (16, 16))

        # Draw Party
        segment_width = SCREEN_WIDTH / 2 / (len(self.player.party) + 1) + 6
        x = segment_width
        y = 124
        for i in range(len(self.player.party)):
            if self.player.party[i].is_alive():
                self.draw_creature(self.player.party[i], PARTY_KEYS[i], x, y)
                x += segment_width

        # Draw Enemies
        segment_width = SCREEN_WIDTH / 2 / (len(self.area.enemies) + 1) + 6
        x = segment_width + SCREEN_WIDTH / 2
        for i in range(len(self.area.enemies)):
            self.draw_creature(self.area.enemies[i], ENEMY_KEYS[i], x, y)
            x += segment_width

        y += 156

        if not self.player.is_alive():
            y = self.draw_message_box(['You have died.', 'Press [enter] to continue.'], y)
        elif not self.area.enemies:
            y = self.draw_message_box(['Victory!', 'Press [enter] to continue.'], y)
        elif c and not c.ai:
            if not self.selected_ability:
                y = self.draw_abilities(c, y)
            else:
                y = self.draw_message_box(['Select Target'], y)

        self.draw_last_message()

    def draw_creature(self, creature, letter, x, y):
        if creature == self.last_active_creature:
            draw_sprite(self.canvas, interface_sprites, ARROW_DOWN, x - 24, y - 76 + self.frame_num * 4)

        cx, cy = x - 36, y
        dx, dy = 0, 0
        if creature in self.bump_locations and self.bump_locations[creature]:
            dx,dy = self.bump_locations[creature].get_pos_delta()
        draw_sprite(self.canvas, creature_sprites, creature.sprite_rect, cx + dx, cy + dy, scale=6)

        dy = y - (FONT_HEIGHT + 2)
        for e in creature.effects:
            self.write_center_x(f"[{e.name}]", (x, dy), e.colour)
            dy -= FONT_HEIGHT + 2
        y += 80

        self.write_center_x(f"{creature.name}", (x,y))

        y += FONT_HEIGHT + 8
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

        y += 10
        self.write(f"[{letter}]", (x - int(FONT_WIDTH * 1.5), y), DIMGRAY)

    def draw_abilities(self, c: Creature, y: int):
        box_height = (len(c.abilities) + 1) * (FONT_SIZE + 2)
        self.draw_box((16, y, SCREEN_WIDTH - 32, box_height + 20), 4)
        y += 10
        i = 1
        for a in c.abilities:
            colour = WHITE if a.is_usable() else GRAY
            self.write(f"{i}: {a.get_short_desc()}", (24, y), colour)
            y += FONT_SIZE + 2
            i += 1
        self.write("0: Skip Turn", (24, y))

        return box_height + y

    def draw_message_box(self, messages: list[str], y: int):
        box_height = len(messages) * (FONT_SIZE + 2)
        self.draw_box((16, y, SCREEN_WIDTH - 32, box_height + 20), 4)
        y += 10
        for m in messages:
            self.write_center_x(m, (SCREEN_WIDTH / 2, y), WHITE)
            y += FONT_HEIGHT + 2
        return box_height + y

    def draw_last_message(self):
        x, y = SCREEN_WIDTH / 2, SCREEN_HEIGHT - FONT_HEIGHT - 2 - 12
        messages = messenger.latest_messages.copy()
        messages.reverse()
        for m in messages:
            self.write_center_x(m, (x,y))
            y -= FONT_HEIGHT - 2
