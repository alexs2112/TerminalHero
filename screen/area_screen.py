import pygame
from screen.screen import Screen
from screen.dialog_screen import DialogScreen
from screen.combat_screen import CombatScreen
from screen.quest_screen import QuestScreen
from world.area import Area
from world.world import World
from main.constants import *
from main.colour import *
from main.util import fit_text, NUMBERS

class AreaScreen(Screen):
    def __init__(self, canvas, area: Area, world: World):
        super().__init__(canvas)
        self.world = world
        self.player = world.player
        self.index = 0
        self.refresh(area=area)

    def refresh(self, **kwargs):
        self.area: Area = kwargs['area']
        self.area.enter_area(self.player)
        self.encounters = self.area.enabled_encounters()
        self.description_lines = fit_text(self.area.description)
        self.index = 0
        self.dialog = {}                        # dict of {index: npc}
        self.options = self.define_options()    # (text, function, <colour_str>)

    def define_options(self):
        opts = []
        i = 0
        for e in self.encounters:
            opts.append((e.name, self.begin_encounter, 'red'))
            i += 1
        for npc in self.area.npcs:
            if npc.has_dialog():
                self.dialog[i] = npc
                i += 1
                node = npc.get_dialog_node()
                if node.area_option:
                    opts.append((node.area_option, self.speak_to_npc, 'cyan'))
                else:
                    opts.append((f"Speak to {npc.name}", self.speak_to_npc, 'cyan'))

        if self.can_leave():
            opts.append(("Leave Area", self.leave_area))
        return opts

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.index = min(self.index + 1, len(self.options) - 1)
                elif event.key == pygame.K_UP:
                    self.index = max(0, self.index - 1)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.index][1](self.canvas, self.index)
                elif event.key in NUMBERS:
                    i = int(pygame.key.name(event.key)) - 1
                    if i < len(self.options):
                        return self.options[i][1](self.canvas, i)
                elif event.key == pygame.K_l:
                    return QuestScreen(self.canvas, self.player, self)
        return self

    def display(self):
        super().display()

        y = 20
        self.write_center_x(self.area.name, (int(SCREEN_WIDTH / 2), y))
        y += FONT_HEIGHT + 8
        for line in self.description_lines:
            self.write_center_x(line, (int(SCREEN_WIDTH / 2), y))
            y += FONT_HEIGHT + 2

        x = 64
        y += 16
        for i in range(len(self.options)):
            opt = self.options[i][0]
            colour = self.option_colour(i)
            self.write(f"[{i+1}]: {opt}", (x,y), colour)
            y += FONT_HEIGHT + 2

        self.display_notifications()

    def option_colour(self, i):
        if len(self.options[i]) > 2:
            c = self.options[i][2]
            if c == 'cyan':
                if i == self.index:
                    return CYAN
                else:
                    return LIGHTCYAN
            elif c == 'red':
                if i == self.index:
                    return RED
                else:
                    return LIGHTRED
        if i == self.index:
            return GREEN
        else:
            return WHITE

    def can_leave(self):
        for e in self.encounters:
            if e.block_exit:
                return False
        return True

    # Some basic functions that are called by the option the player selects
    def leave_area(self, canvas, _):
        # pylint: disable=import-outside-toplevel
        from screen.world_screen import WorldScreen
        return WorldScreen(canvas, self.world, self.area)

    def begin_encounter(self, canvas, index):
        return CombatScreen(canvas, self.encounters[index], self.area, self.player, last_screen=self)

    def speak_to_npc(self, canvas, index):
        root_node = self.dialog[index].get_dialog_node()
        return DialogScreen(canvas, self, root_node, self.player)
