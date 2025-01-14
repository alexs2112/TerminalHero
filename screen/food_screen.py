from screen.screen import Screen
from main.constants import *
from main.colour import *
from main.util import *
from main.clock import get_clock
from main.player_log import get_player_log, update_log
from main.notification import add_notification
from item.item import Food
from creature.player import Player
from creature.creature import Creature

clock = get_clock()
player_log = get_player_log()

class FoodScreen(Screen):
    def __init__(self, canvas, food: Food, player: Player, last_screen: Screen):
        super().__init__(canvas)
        self.food = food
        self.player = player
        self.party = player.party
        self.last_screen = last_screen
        self.index = 0
        self.box_width = 124
        self.box_height = 124 + 32

        # Cache the text for food description and stats
        self.food_desc = fit_text(self.food.description, SCREEN_WIDTH - 200)
        if self.food.is_known():
            self.food_stats = self.food.get_stat_strings()
        else:
            self.food_stats = [ '???' ]

        # If you try to force feed someone multiple times in one day
        self.error_message = "That party member has already eaten!"
        self.show_error_message = False
        self.error_timer = 0
        self.error_timer_max = 1500

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.last_screen
                elif event.key == pygame.K_RIGHT:
                    self.index = min(self.index + 1, len(self.party) - 1)
                elif event.key == pygame.K_LEFT:
                    self.index = max(self.index - 1, 0)
                elif event.key == pygame.K_RETURN:
                    result = self.eat(self.party[self.index])
                    if result:
                        return self.last_screen
        return self

    def eat(self, creature: Creature):
        if creature.food:
            self.show_error_message = True
            self.error_timer = self.error_timer_max
            return False

        creature.eat_food(self.food)
        if not player_log[self.food.log_entry]:
            update_log(self.food.log_entry)
            add_notification([f':GREEN:{self.food.name}:GREEN:'] + self.food.get_stat_strings())
        return True

    def display(self):
        super().display()

        if self.show_error_message:
            self.error_timer -= clock.get_time()
            if self.error_timer <= 0:
                self.show_error_message = False
                self.error_timer = 0

        # Much of this is stolen from the equip_item_screen
        section_width = SCREEN_WIDTH / len(self.party)
        i = 0
        y = 16
        for c in self.party:
            x = section_width * i + (section_width - self.box_width) / 2
            self.draw_creature(c, x, y, i)
            i += 1
        y += self.box_height + 24
        self.draw_box((SCREEN_WIDTH/2 - 32, y, 64, 64), 4, DIMGRAY)
        draw_sprite(self.canvas, item_sprites, self.food.sprite_rect, SCREEN_WIDTH/2 - 24, y + 8, scale=4)
        y += 72

        self.write_center_x(f"Eating: {self.food.name} (:YELLOW:{self.food.cost}:YELLOW:)", (SCREEN_WIDTH/2, y))
        y += FONT_HEIGHT + 6
        for l in self.food_desc:
            self.write_center_x(l, (SCREEN_WIDTH/2, y), DIMGRAY)
            y += FONT_HEIGHT + 2
        y += 8
        self.write_center_x("Effects:", (SCREEN_WIDTH/2, y))
        y += FONT_HEIGHT + 2
        for l in self.food_stats:
            self.write_center_x(l, (SCREEN_WIDTH/2, y))
            y += FONT_HEIGHT + 2

        if self.show_error_message:
            self.write_center_x(self.error_message, (SCREEN_WIDTH/2, SCREEN_HEIGHT - 16 - FONT_HEIGHT), RED)

        self.display_notifications()

    def draw_creature(self, creature: Creature, x: int, y: int, i: int):
        c = GREEN if i == self.index else DIMGRAY
        self.draw_box((x, y, self.box_width, self.box_height), colour=c)
        offset_x = (self.box_width - 92) / 2
        self.draw_box((x + offset_x, y + 16, 92, 92), 4)
        draw_sprite(self.canvas, creature_sprites, creature.get_sprite_rect(), x + offset_x + 10, y + 26, scale=6)
        y += 118
        self.write_center_x(creature.name, (x + self.box_width / 2, y), c)
