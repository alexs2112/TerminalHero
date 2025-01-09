import pygame
from main.constants import *
from main.colour import *
from main.util import *
from main.clock import get_clock
from main.notification import set_notification
from screen.screen import Screen
from screen.area_screen import AreaScreen
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
        self.update_rooms()

        # Cache how the dungeon is supposed to look as it is resource intensive, this is to scale
        self.dungeon_sprite = None
        self.update_sprite()

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.frame_num = 0
                self.local_time = 0

                # This should probably be condensed
                if event.key == pygame.K_UP:
                    if EXIT_UP in self.current_room.exits:
                        self.player_pos = (self.player_pos[0], self.player_pos[1] - 1)
                        self.update_rooms()
                    elif EXIT_UP == self.current_room.exit_dungeon_direction:
                        self.return_screen.refresh(area=self.dungeon.area)
                        return self.return_screen
                elif event.key == pygame.K_RIGHT:
                    if EXIT_RIGHT in self.current_room.exits:
                        self.player_pos = (self.player_pos[0] + 1, self.player_pos[1])
                        self.update_rooms()
                    elif EXIT_RIGHT == self.current_room.exit_dungeon_direction:
                        self.return_screen.refresh(area=self.dungeon.area)
                        return self.return_screen
                elif event.key == pygame.K_DOWN:
                    if EXIT_DOWN in self.current_room.exits:
                        self.player_pos = (self.player_pos[0], self.player_pos[1] + 1)
                        self.update_rooms()
                    elif EXIT_DOWN == self.current_room.exit_dungeon_direction:
                        self.return_screen.refresh(area=self.dungeon.area)
                        return self.return_screen
                elif event.key == pygame.K_LEFT:
                    if EXIT_LEFT in self.current_room.exits:
                        self.player_pos = (self.player_pos[0] - 1, self.player_pos[1])
                        self.update_rooms()
                    elif EXIT_LEFT == self.current_room.exit_dungeon_direction:
                        self.return_screen.refresh(area=self.dungeon.area)
                        return self.return_screen
                elif event.key == pygame.K_RETURN:
                    return AreaScreen(self.canvas, self.current_room, self.player, self)

                # If the new current_room has an encounter in it, force the player into the room to start combat
                if self.current_room.enabled_encounters():
                    return AreaScreen(self.canvas, self.current_room, self.player, self)

        return self

    def display(self):
        super().display()

        self.local_time += clock.get_time()
        if self.local_time >= 500:
            self.local_time = 0
            self.frame_num = 1 - self.frame_num

        self.draw_line((self.divider_x, 0), (self.divider_x, SCREEN_HEIGHT))
        self.draw_scaled_sprite()

        room = self.current_room
        if room:
            self.write_room_info(room)

        self.display_notifications()

    def refresh(self, **kwargs):
        self.update_rooms()

    def update_rooms(self):
        self.current_room = self.dungeon.rooms[self.player_pos[0]][self.player_pos[1]]
        self.room_description = fit_text(self.current_room.description, SCREEN_WIDTH - self.divider_x - 32)
        self.current_room.revealed = True
        self.update_sprite()

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
        for f in room.features:
            self.write(f, (x,y), YELLOW)
            y += FONT_HEIGHT + 2

        y += 8
        self.write('[enter]', (x,y), DIMGRAY)

    def draw_player_sprite(self, room: Room, x, y):
        if self.frame_num == 1:
            return
        sx, sy = room.unscaled_position
        px, py = room.player_position[0], room.player_position[1]
        dx, dy = (sx + px - 7) * DUNGEON_SCALE, (sy + py - 8) * DUNGEON_SCALE
        draw_sprite(self.canvas, creature_sprites, self.player.get_sprite_rect(), x+dx, y+dy, scale=DUNGEON_SCALE)
