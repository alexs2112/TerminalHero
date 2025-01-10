from math import ceil
from main.constants import *
from main.util import *
from screen.screen import Screen
from screen.equip_item_screen import EquipItemScreen
from creature.player import Player
from creature.item import Item

class InventoryScreen(Screen):
    def __init__(self, canvas, player: Player, last_screen: Screen):
        super().__init__(canvas)
        self.player = player
        self.last_screen = last_screen

        # This really doesn't like odd numbers for some reason
        self.items_per_row = 6
        self.center_x = self.items_per_row * 76 - 4

        self.row = 0
        self.column = 0
        self.item = None
        self.num_rows = 0
        self.refresh()

    def refresh(self, **kwargs):
        self.row = 0
        self.column = 0
        self.item = self.selected_item()
        self.num_rows = ceil(len(self.player.key_items) / self.items_per_row) \
                      + ceil(len(self.player.inventory) / self.items_per_row)

    def check_events(self, events):
        if self.check_notifications(events):
            return self
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return EquipItemScreen(self.canvas, self.item, self.player, self)
                elif event.key == pygame.K_ESCAPE:
                    return self.last_screen
                elif event.key == pygame.K_RIGHT:
                    self.move_cursor(1,0)
                elif event.key == pygame.K_LEFT:
                    self.move_cursor(-1,0)
                elif event.key == pygame.K_UP:
                    self.move_cursor(0,-1)
                elif event.key == pygame.K_DOWN:
                    self.move_cursor(0,1)
                self.item = self.selected_item()
        return self

    def display(self):
        super().display()

        self.draw_line((self.center_x, 0), (self.center_x, SCREEN_HEIGHT))
        self.write("Inventory", (16,16))
        self.draw_items()
        self.write_item_details(self.item)
        self.display_notifications()

    def move_cursor(self, dx, dy):
        self.column += dx
        if self.column == self.items_per_row:
            self.column = 0
        elif self.column < 0:
            self.column = self.items_per_row - 1
        self.row += dy
        if self.row < 0:
            self.row = self.num_rows - 1
        if self.row == self.num_rows:
            self.row = 0

        # Move to the next valid space
        r = self.row
        if self.player.key_items:
            key_rows = ceil(len(self.player.key_items) / self.items_per_row)
            if r == key_rows - 1:
                cols = len(self.player.key_items) % self.items_per_row
                if self.column >= cols:
                    self.column = cols - 1
                    return
            r -= key_rows
        if self.player.inventory:
            inv_rows = ceil(len(self.player.inventory) / self.items_per_row)
            if r == inv_rows - 1:
                cols = len(self.player.inventory) % self.items_per_row
                if self.column >= cols:
                    self.column = cols - 1
                    return
        # There is an edge case here where if you move Right on the last item in a row, it won't
        # cycle back to the first item in that row if len(row) < self.items_per_row - 1

    def selected_item(self):
        r = self.row
        if self.player.key_items:
            key_rows = ceil(len(self.player.key_items) / self.items_per_row)
            if r < key_rows:
                return self.player.key_items[r * self.items_per_row + self.column]
            r -= key_rows
        if self.player.inventory:
            return self.player.inventory[r * self.items_per_row + self.column]
        return None

    def draw_items(self):
        x, y = 16, 48
        current = (0,0)
        if self.player.key_items:
            self.write("Key Items:", (x,y))
            y += FONT_HEIGHT + 2
            x, y, current = self.draw_item_list(self.player.key_items, current, x, y)
            y += 12

        self.write("Items:", (x, y))
        y += FONT_HEIGHT + 2
        if self.player.inventory:
            x, y, current = self.draw_item_list(self.player.inventory, current, x, y)
        else:
            y += 8
            self.write("There's nothing here...", (x + 32, y), DIMGRAY)

    def draw_item_list(self, item_list, current, x, y):
        base_x = 16
        for item in item_list:
            c = GRAY
            if current == (self.column, self.row):
                c = GREEN
            self.draw_box((x, y, 48 + 16, 48 + 16), 4, c)
            draw_sprite(self.canvas, item_sprites, item.sprite_rect, x + 8, y + 8)

            if current[0] == self.items_per_row - 1 or item == item_list[-1]:
                x = base_x
                current = (0, current[1] + 1)
                y += 64 + 8
            else:
                current = (current[0] + 1, current[1])
                x += 64 + 8
        return x, y, current

    def write_item_details(self, item: Item):
        if not item:
            return
        x = self.center_x + 16
        y = 32
        self.write_center_x(item.name, ((SCREEN_WIDTH - self.center_x) / 2 + self.center_x, y))
        y += FONT_HEIGHT + 10

        if item.stats:
            for stat, value in item.stats.items():
                self.write(f"{stat}: {value}", (x,y), LIGHTGRAY)
                y += FONT_HEIGHT + 2
            y += 8

        if item.resistances:
            self.write("Resistances:", (x, y), WHITE)
            y += FONT_HEIGHT + 2
            for resist, value in item.resistances.items():
                self.write(f"{resist}: {value}%", (x + 16, y), LIGHTGRAY)
                y += FONT_HEIGHT + 2
            y += 8

        width = SCREEN_WIDTH - self.center_x - 32 - 16
        if item.abilities:
            self.write("Abilities:", (x,y), WHITE)
            y += FONT_HEIGHT + 2

            for a in item.abilities:
                self.write(f"{a.name}{f' ({a.max_cooldown})' if a.max_cooldown > 1 else ''}", (x,y), LIGHTGRAY)
                y += FONT_HEIGHT + 2
                ds = fit_text(a.description, width)
                for d in ds:
                    self.write(d, (x + 16, y), LIGHTGRAY)
                    y += FONT_HEIGHT + 2
                y += 8
