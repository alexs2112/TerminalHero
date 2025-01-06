#!/bin/python3

import argparse
import pygame
from main.constants import *
from main.messenger import get_messenger
from main.clock import get_clock
from creature.creature_factory import get_creature_factory
from world.world_builder import WorldBuilder
from screen.start_screen import StartScreen

clock = get_clock()
creature_factory = get_creature_factory()

class Game:
    def __init__(self, args_list):
        pygame.init()
        pygame.display.set_caption("Terminal Hero")
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.args = args_list
        messenger = get_messenger(self.args)
        if self.args.verbose:
            messenger.set_verbose()
        messenger.clear()

        self.player = creature_factory.new_player()
        self.world = self.generate_world()
        self.world.player = self.player
        if self.args.companion:
            # This will currently break the first quest when you get a second companion
            self.player.party.append(creature_factory.new_companion_1())

        self.screen = StartScreen(self.canvas, self.world)

    def generate_world(self):
        world_builder = WorldBuilder(9,9)
        return world_builder.build_world()

    def game_loop(self):
        while True:
            clock.tick(FRAMERATE)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return

            self.screen = self.screen.check_events(events)
            if not self.screen:
                return

            self.screen.display()
            pygame.display.update()

    def dialog_test(self):
        # pylint: disable=import-outside-toplevel
        from screen.dialog_screen import DialogScreen
        from dialog.dialog_parser import load_dialog
        base_node = load_dialog('resources/dialog/gorren_questline.json')
        self.screen = DialogScreen(self.canvas, None, base_node['start'], self.player)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug and info statements')
    parser.add_argument('-d', '--dialog', action='store_true', help='test dialog')
    parser.add_argument('-c', '--companion', action='store_true', help='test a companion in the player party')
    parser.add_argument('-a', '--all', action='store_true', help='enable all player_log fields')
    args = parser.parse_args()

    if args.all:
        # pylint: disable=import-outside-toplevel,ungrouped-imports
        from main.player_log import get_player_log
        player_log = get_player_log()
        for key in [
            'met_elder_varik',
            'known_cemetery',
            'known_bloodstone_mine',
            'known_starvation_pit',
            'known_garrison'
        ]:
            player_log[key] = True

    game = Game(args)
    if args.dialog:
        game.dialog_test()
    game.game_loop()
