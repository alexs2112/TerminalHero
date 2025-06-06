import pygame
from screen.screen import Screen
from screen.escape_screen import EscapeScreen
from main.constants import *
from main.colour import *
from main.util import *
from main.messenger import get_messenger
from main.clock import get_clock
from main.player_log import get_player_log, update_log
from dialog.dialog_node import DialogNode
from dialog.dice_roller import DiceRoller
from creature.player import Player

messenger = get_messenger()
clock = get_clock()
player_log = get_player_log()

# In interface sprites
DICE_START = (120,24,12,12)

class DialogScreen(Screen):
    def __init__(self, canvas, last_screen: Screen, root_node: DialogNode, player: Player):
        super().__init__(canvas)
        self.last_screen = last_screen
        self.player = player

        # Keep track of the gradual text
        self.lines = []
        self.char_index = 0
        self.finished = False
        self.frame_timer = 0

        # Keep track of the dice roll
        self.roller = None              # If roller is set, it means this is a DialogRoll
        self.die_finished = True
        self.die_frame = 0
        self.die_timer = 0
        self.die_total_frames = 9

        self.select_node(root_node)

    def select_node(self, node):
        self.current_node: DialogNode = node
        if self.current_node.only_once:
            update_log(self.current_node.id)
        if self.current_node.set_log:
            update_log(self.current_node.set_log)
        self.children = self.get_valid_children()
        self.current_node.call_function(self.player)
        self.lines = fit_text(self.current_node.text, SCREEN_WIDTH - 32)
        if self.current_node.type == "Roll":
            self.finished = True
            self.roller = DiceRoller()
            self.die_finished = False
            self.die_frame = 0
            self.die_timer = 0
            self.roller.roll()
        else:
            self.roller = None
            self.frame_timer = 0
            self.char_index = 0
            self.finished = False
            messenger.add(node.text)

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        surpassed = clock.get_time()
        if not self.finished:
            self.frame_timer += surpassed
            if self.frame_timer >= DIALOG_CHAR_TIME:
                self.frame_timer = 0
                self.char_index += 1
            if self.char_index >= self.line_length(self.current_node.text):
                self.finished = True
        if not self.die_finished:
            self.die_timer += surpassed
            if self.die_timer >= self.die_frame * self.die_frame * 8:
                self.die_timer = 0
                self.die_frame += 1
                self.roller.roll()
            if self.die_frame >= self.die_total_frames:
                self.die_finished = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                # Die Roll Event: Press Enter to Continue
                if self.roller:
                    if self.die_finished:
                        if event.key == pygame.K_RETURN:
                            success = self.current_node.roll_successful(self.roller.total(), self.player)
                            next_node = self.current_node.success if success else self.current_node.failure
                            self.select_node(next_node)
                            return self
                    else:
                        self.die_finished = True
                        self.roller.roll()
                # Otherwise, normal dialogue, select next option
                elif self.finished:
                    if event.key == pygame.K_ESCAPE:
                        return EscapeScreen(self.canvas, self, can_save=False)
                    for i in range(len(self.children)):
                        if event.key == pygame.key.key_code(str(i + 1)):
                            return self.select_child(i)
                else:
                    self.finished = True
        return self

    def select_child(self, index):
        if self.children[index][1] and not self.children[index][1].meet_stat_requirement(self.player):
            return self

        if self.children[index][1] is None:
            self.last_screen.refresh(area=self.player.area)
            return self.last_screen

        self.select_node(self.children[index][1])
        if self.current_node.text == "None":
            self.last_screen.refresh(area=self.player.area)
            return self.last_screen
        return self

    def get_valid_children(self):
        children = []
        for child in self.current_node.children:
            if child[1] is None or child[1].condition_met():
                children.append(child)
        return children

    def display(self):
        super().display()

        x, y = 20, 20
        self.write_center_x(self.current_node.name, (int(SCREEN_WIDTH / 2), y))
        y += FONT_HEIGHT + 8

        current = self.char_index
        for line in self.lines:
            self.write_center_x(line, (SCREEN_WIDTH / 2, y))

            line_len = self.line_length(line)
            box_start_x = (SCREEN_WIDTH - line_len * FONT_WIDTH) / 2
            box_start_y = y + (FONT_HEIGHT / 2)

            # Sentence is unfinished, draw a black box over the rendered letters lol
            if not self.finished and current < line_len:
                self.draw_line((box_start_x + current * FONT_WIDTH, box_start_y), (SCREEN_WIDTH - 7, box_start_y), width=FONT_HEIGHT, colour=BLACK)
                break
            else:
                current -= line_len

            y += FONT_HEIGHT + 2
        y += 8

        if self.roller:
            y += 16
            self.write_center_x(f"{self.current_node.stat} Challenge: {self.current_node.value}", (SCREEN_WIDTH / 2, y))
            y += FONT_HEIGHT + 6
            a,b = self.roller.get_roll()
            self.draw_box((SCREEN_WIDTH / 2 - 82, y, 56, 56), width=4)
            self.draw_box((SCREEN_WIDTH / 2 + 16, y, 56, 56), width=4)
            a_rect = (DICE_START[0] + 12 * (a-1), DICE_START[1], DICE_START[2], DICE_START[3])
            b_rect = (DICE_START[0] + 12 * (b-1), DICE_START[1], DICE_START[2], DICE_START[3])
            draw_sprite(self.canvas, interface_sprites, a_rect, SCREEN_WIDTH / 2 - 78, y + 4, scale=4)
            draw_sprite(self.canvas, interface_sprites, b_rect, SCREEN_WIDTH / 2 + 20, y + 4, scale=4)
            y += 56 + 16
            if self.die_finished:
                y += 32
                success = self.current_node.roll_successful(self.roller.total(), self.player)
                c = GREEN if success else RED
                self.write_center_x(f"Total: {self.roller.total()} + {self.player.stat(self.current_node.stat)}", (SCREEN_WIDTH / 2, y), c)
                y += FONT_HEIGHT+2
                s,c = ("Success!", GREEN) if success else ("Failure.", RED)
                self.write_center_x(s, (SCREEN_WIDTH/2, y), c)
                y += 32
                self.write_center_x("Press [enter] to continue", (SCREEN_WIDTH / 2, y), GRAY)

        elif self.finished:
            index = 1
            index_size = FONT_WIDTH * 3 + 6
            for child in self.children:
                self.write(f'[{index}]', (x,y))
                if child[1] and not child[1].meet_stat_requirement(self.player):
                    lines = [ child[1].stat_requirement_string() ]
                    colour = GRAY
                elif child[1] and child[1].type == "Roll":
                    percentage = child[1].percentage(self.player)
                    if percentage <= 20:
                        c = ':RED:'
                    elif percentage <= 40:
                        c = ':ORANGE:'
                    elif percentage <= 60:
                        c = ':YELLOW:'
                    elif percentage <= 80:
                        c = ':WHITE:'
                    else:
                        c = ':GREEN:'
                    lines = fit_text(f"{child[0]} [{child[1].stat} challenge {c}{percentage}%{c}]", SCREEN_WIDTH - 32 - index_size)
                    colour = LIGHTGRAY
                else:
                    lines = fit_text(child[0], SCREEN_WIDTH - 32 - index_size)
                    colour = LIGHTGRAY if child[1] else GRAY

                for line in lines:
                    self.write(line, (x + index_size, y), colour)
                    y += FONT_HEIGHT + 2
                y += 4
                index += 1
        self.display_notifications()
