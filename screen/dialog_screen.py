import pygame
from screen.screen import Screen
from main.constants import *
from main.colour import *
from main.util import *
from main.messenger import get_messenger
from main.clock import get_clock
from main.player_log import get_player_log
from dialog.dialog_node import DialogNode
from creature.player import Player

messenger = get_messenger()
clock = get_clock()
player_log = get_player_log()

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

        self.select_node(root_node)

    def select_node(self, node):
        self.current_node: DialogNode = node
        self.children = self.get_valid_children()
        self.current_node.call_function(self.player)
        self.lines = fit_text(self.current_node.text, SCREEN_WIDTH - 100)
        self.char_index = 0
        self.finished = 0
        messenger.add(node.text)

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        if not self.finished:
            self.frame_timer += clock.get_time()
            if self.frame_timer >= DIALOG_CHAR_TIME:
                self.frame_timer = 0
                self.char_index += 1
            if self.char_index >= self.line_length(self.current_node.text):
                self.finished = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.finished:
                    for i in range(len(self.children)):
                        if event.key == pygame.key.key_code(str(i + 1)):
                            return self.select_child(i)
                else:
                    self.finished = True
        return self

    def select_child(self, index):
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

        if self.finished:
            index = 1
            index_size = FONT_WIDTH * 3 + 6
            for child in self.children:
                self.write(f'[{index}]', (x,y))
                lines = fit_text(child[0], SCREEN_WIDTH - 32 - index_size)
                colour = WHITE if child[1] else GRAY
                for line in lines:
                    self.write(line, (x + index_size, y), colour)
                    y += FONT_HEIGHT + 2
                y += 4
                index += 1
        self.display_notifications()
