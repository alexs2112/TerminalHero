import pygame
from main.constants import *
from main.colour import *
from main.util import *
from main.clock import get_clock
from main.notification import set_notification
from screen.screen import Screen
from screen.combat_screen import CombatScreen
from screen.dialog_screen import DialogScreen
from creature.player import Player
from world.dungeon import Dungeon
from world.room import *

clock = get_clock()

class DungeonScreen(Screen):
    def __init__(self, canvas, dungeon: Dungeon, player: Player, return_screen):
        super().__init__(canvas)
        self.dungeon = dungeon
        self.player = player
        self.player_pos = dungeon.start_player_pos

        # When the player leaves the dungeon, return to this screen
        self.return_screen = return_screen

        # When the player first enters the dungeon, display a notification
        set_notification([dungeon.name] + fit_text(dungeon.description, SCREEN_WIDTH - 160))

        self.local_time = 0
        self.frame_num = 0

        self.divider_x = SCREEN_WIDTH / 2 + 64
        self.center_x = self.divider_x / 2
        self.center_y = SCREEN_HEIGHT / 2

        # The player has moved into a new room, update it
        self.current_room = None
        self.room_description = []
        self.options = []           # [(text, function, colour)]
        self.dialog = {}            # { index: DialogFeature }
        self.encounters = {}        # { index: Encounter }
        self.dungeon_sprite = None  # Cache how the dungeon is supposed to look as it is resource intensive, this is to scale
        self.update_rooms()

        # Temporary message shown at the bottom of the screen
        self.message = ""
        self.message_time = 0
        self.message_time_max = 1500

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.frame_num = 0
                self.local_time = 0
                if event.key == pygame.K_UP:
                    return self.player_move((0,-1))
                elif event.key == pygame.K_RIGHT:
                    return self.player_move((1,0))
                elif event.key == pygame.K_DOWN:
                    return self.player_move((0,1))
                elif event.key == pygame.K_LEFT:
                    return self.player_move((-1,0))

                elif event.key in NUMBERS:
                    i = int(pygame.key.name(event.key)) - 1
                    if i < len(self.options):
                        return self.options[i][1](i)
        return self

    def display(self):
        super().display()

        dt = clock.get_time()
        self.local_time += dt
        if self.local_time >= 500:
            self.local_time = 0
            self.frame_num = 1 - self.frame_num
        if self.message:
            self.message_time += dt
            if self.message_time >= self.message_time_max:
                self.clear_message()

        self.draw_line((self.divider_x, 0), (self.divider_x, SCREEN_HEIGHT))
        self.draw_scaled_sprite()

        room = self.current_room
        if room:
            self.write_room_info(room)

        if self.message:
            self.write_center_x(self.message, (self.divider_x / 2, SCREEN_HEIGHT - 16 - FONT_HEIGHT), RED)

        self.display_notifications()

    def refresh(self, **kwargs):
        self.update_rooms()

    def update_rooms(self):
        self.current_room = self.dungeon.rooms[self.player_pos[0]][self.player_pos[1]]
        self.current_room.enter_area(self.player)
        self.room_description = fit_text(self.current_room.get_description(), SCREEN_WIDTH - self.divider_x - 32)
        self.current_room.revealed = True
        self.clear_message()
        self.define_options()
        self.update_sprite()

    def define_options(self):
        opts = []
        new_encounters = {}
        new_dialog = {}
        i = 0
        for e in self.current_room.enabled_encounters():
            opts.append((e.name, self.begin_encounter, RED))
            new_encounters[i] = e
            i += 1

        for d in self.current_room.get_dialog_features():
            node = d.get_dialog_node()
            if node.area_option:
                opts.append((node.area_option, self.start_dialog, CYAN))
            else:
                opts.append((d.name, self.start_dialog, YELLOW))
            new_dialog[i] = d
            i += 1

        self.options = opts
        self.encounters = new_encounters
        self.dialog = new_dialog

    def player_move(self, direction):
        for e in self.current_room.enabled_encounters():
            if e.block_exit:
                self.update_message("Can't Leave: Enemies Present!")
                return self
        if direction in self.current_room.locked:
            self.update_message("That Door is Locked!")
        elif direction in self.current_room.exits:
            self.player_pos = (self.player_pos[0] + direction[0], self.player_pos[1] + direction[1])
            self.update_rooms()
            return self
        elif direction == self.current_room.exit_dungeon_direction:
            self.return_screen.refresh(area=self.dungeon.area)
            return self.return_screen
        return self

    def update_sprite(self):
        w, h = self.dungeon.unscaled_width, self.dungeon.unscaled_height
        s = pygame.Surface((w,h))
        for room in self.dungeon.get_rooms():
            if room.revealed:
                s.blit(dungeon_sprites, room.unscaled_position, room.sprite_rect)
        scaled = pygame.transform.scale(s, (w * DUNGEON_SCALE, h * DUNGEON_SCALE))
        self.dungeon_sprite = scaled

    def draw_scaled_sprite(self):
        dx, dy = self.dungeon_sprite.get_size()
        x = self.center_x - dx / 2
        y = self.center_y - dy / 2
        self.canvas.blit(self.dungeon_sprite, (x,y))
        self.draw_player_sprite(self.current_room, x, y)

    def write_room_info(self, room: Room):
        x = self.divider_x + 16
        y = 16

        self.write(room.name, (x,y))
        y += FONT_HEIGHT + 2

        for l in self.room_description:
            self.write(l, (x,y), LIGHTGRAY)
            y += FONT_HEIGHT + 2
        y += 8
        x += 16
        i = 1
        for o in self.options:
            self.write(f"{i}: {o[0]}", (x,y), o[2])
            y += FONT_HEIGHT + 2

    def draw_player_sprite(self, room: Room, x, y):
        if self.frame_num == 1:
            return
        sx, sy = room.unscaled_position
        px, py = room.player_position[0], room.player_position[1]
        dx, dy = (sx + px - 7) * DUNGEON_SCALE, (sy + py - 8) * DUNGEON_SCALE
        draw_sprite(self.canvas, creature_sprites, self.player.get_sprite_rect(), x+dx, y+dy, scale=DUNGEON_SCALE)

    def update_message(self, message):
        self.message = message
        self.message_time = 0
    
    def clear_message(self):
        self.message = ""
        self.message_time = 0

    # Functions called by the room option the player selects
    # These are essentially the same as in AreaScreen
    def begin_encounter(self, index):
        return CombatScreen(self.canvas, self.encounters[index], self.current_room, self.player, self)

    def start_dialog(self, index):
        root_node = self.dialog[index].get_dialog_node()
        return DialogScreen(self.canvas, self, root_node, self.player)
