#!/bin/python3

import argparse
import pygame
from main.constants import *
from main.messenger import get_messenger

class Game:
    def __init__(self, args_list):
        pygame.init()
        pygame.display.set_caption("Terminal Hero")
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.args = args_list
        self.messenger = get_messenger(self.args)
        self.messenger.clear()

        # This needs to be called after messenger is created or else it will be empty
        # pylint: disable=import-outside-toplevel
        from screen.start_screen import StartScreen
        self.screen = StartScreen(self.canvas)

    def game_loop(self):
        while True:
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
        # pylint: disable=import-outside-toplevel,line-too-long
        from screen.dialog_screen import DialogScreen
        from dialog.dialog_node import DialogNode
        node1_1 = DialogNode("Elder",
                               "Some say the creature is vulnerable to fire, others claim only a silver blade can pierce its hide. No one knows for sure, but you may find a blacksmith in the village who could forge a weapon for you.",
                               [("Where can I find the blacksmith?", None),
                                ("I'll figure it out myself, thank you.", None)
                               ])
        node1_2 = DialogNode("Elder",
                               "The ruins are deep within the forest, past the ancient oak tree. If you venture that far, be cautious. The beast's scent grows stronger near the stones.",
                               [("Thank you, I will go there immediately.", None),
                                ("I'll think about it first.", None)
                               ])
        node1 = DialogNode("Elder",
                             "You must be speaking of the Forest Beast. Many have vanished in the woods recently. It's said to be lurking near the old ruins. Tread carefully, traveler",
                             [("Do you know how to defeat it?", node1_1),
                              ("Where exactly are the ruins?", node1_2),
                              ("I'll find it myself.", None)
                             ])
        node2_1 = DialogNode("Elder",
                               "Ah, the mind is a powerful ally. To gain wisdom, you must listen to the world around you—its people, its nature, and its history. Seek out the library in the northern hills for more knowledge.",
                               [("I'll head to the library.", None),
                                ("I have other matters to attend to.", None)
                               ])
        node2_2 = DialogNode("Elder",
                               "Strength comes from within, but a good weapon and training help. If you seek to grow in power, visit the training grounds near the village gate.",
                               [("I'll go there now.", None),
                                ("Maybe later.", None)
                               ])
        node2 = DialogNode("Elder",
                             "Guidance, eh? The road ahead is not an easy one. Do you seek wisdom of the mind or strength of the body?",
                             [("I seek wisdom.", node2_1),
                              ("I need strength.", node2_2)
                             ])
        node3_1 = DialogNode("Elder",
                               "Bandits have been spotted near the eastern pass. And there are rumors of strange creatures lurking in the night. If you wish to be safe, stay in the village until dawn.",
                               [("I'll risk it.", None),
                                ("I'll stay the night.", None)
                               ])
        node3 = DialogNode("Elder",
                             "I see. Be wary, traveler. The roads are not as safe as they once were. Keep your wits about you.",
                             [("What dangers lie on the road?", node3_1),
                              ("I'll be fine, thank you.", None)
                             ])
        base_node = DialogNode("Elder",
                                 "Ah, a traveler! What brings you to our humble village?",
                                 [("I'm looking for information on a dangerous creature nearby", node1),
                                  ("I seek guidance. Can you help me?", node2),
                                  ("Just passing through.", node3)]
                                )
        self.screen = DialogScreen(self.canvas, base_node)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug and info statements')
    parser.add_argument('-d', '--dialog', action='store_true', help='log debug and info statements')
    args = parser.parse_args()

    game = Game(args)
    if args.dialog:
        game.dialog_test()
    game.game_loop()
    