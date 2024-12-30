import pygame
from screen.screen import Screen
from main.constants import *
from main.messenger import *
from main.util import *
from dialog.dialog_node import DialogNode

messenger = get_messenger()

class DialogScreen(Screen):
    def __init__(self, canvas, root_node: DialogNode):
        super().__init__(canvas)
        self.select_node(root_node)

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                for i in range(len(self.current_node.children)):
                    if event.key == pygame.key.key_code(str(i + 1)):
                        return self.select_child(i)
        return self

    def select_node(self, node):
        self.current_node = node
        messenger.add(node.text)

    def select_child(self, index):
        if self.current_node.children[index][1] is None:
            return None

        self.select_node(self.current_node.children[index][1])
        return self

    def display(self):
        super().display()

        x, y = 20, 20
        self.write_center_x(self.current_node.name, (int(SCREEN_WIDTH / 2), y))
        y += FONT_HEIGHT + 8

        lines = fit_text(self.current_node.text, SCREEN_WIDTH - 32)
        for line in lines:
            self.write_center_x(line, (int(SCREEN_WIDTH / 2), y))
            y += FONT_HEIGHT + 2
        y += 8

        index = 1
        index_size = FONT_WIDTH * 3 + 6
        for child in self.current_node.children:
            self.write(f'[{index}]', (x,y))
            lines = fit_text(child[0], SCREEN_WIDTH - 32 - index_size)
            colour = WHITE if child[1] else GRAY
            for line in lines:
                self.write(line, (x + index_size, y), colour)
                y += FONT_HEIGHT + 2
            y += 4
            index += 1
