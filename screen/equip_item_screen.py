from screen.screen import Screen
from main.constants import *
from main.colour import *
from main.util import *
from creature.item import *
from creature.player import Player
from creature.creature import Creature

class EquipItemScreen(Screen):
    def __init__(self, canvas, item: Item, player: Player, last_screen: Screen):
        super().__init__(canvas)
        self.item = item
        self.player = player
        self.last_screen = last_screen
        self.party = player.party
        self.index = 0
        self.box_width = 192

        # Move all inventory items to the player
        for c in self.party:
            if c.type == 'player':
                continue
            if c.inventory:
                for item in c.inventory:
                    self.player.inventory.append(item)
                c.inventory.clear()

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.last_screen
                elif event.key == pygame.K_RIGHT:
                    self.index = min(self.index + 1, len(self.party) - 1)
                elif event.key == pygame.K_LEFT:
                    self.index = max(self.index - 1, 0)
                elif event.key == pygame.K_RETURN:
                    old_item = self.party[self.index].equip_item(self.item)
                    if old_item:
                        self.player.inventory.append(old_item)
                    if self.item in self.player.inventory:
                        self.player.inventory.remove(self.item)
                    elif self.item in self.player.key_items:
                        self.player.key_items.remove(self.item)
                    self.last_screen.refresh()
                    return self.last_screen
        return self

    def display(self):
        super().display()

        self.write_center_x(f"Equipping {self.item.name}", (SCREEN_WIDTH / 2, 20))

        section_width = SCREEN_WIDTH / len(self.party)
        i = 0
        for c in self.party:
            x = section_width * i + (section_width - self.box_width) / 2
            y = 48
            self.draw_creature(c, x, y, i)
            i += 1

    def draw_creature(self, creature: Creature, x: int, y: int, i: int):
        # width = 168
        # creature sprite: 6*12 = 72
        # creature border: 72 + 20 = 92
        c = GREEN if i == self.index else WHITE
        self.draw_box((x, y, self.box_width, SCREEN_HEIGHT - 72), colour=c)
        offset_x = (self.box_width - 92) / 2
        self.draw_box((x + offset_x, y + 16, 92, 92), 4)
        draw_sprite(self.canvas, creature_sprites, creature.get_sprite_rect(), x + offset_x + 10, y + 26, scale=6)
        y += 118
        self.write_center_x(creature.name, (x + self.box_width / 2, y), c)
        y += FONT_HEIGHT + 4
        if creature.profession:
            self.write_center_x(creature.profession.name, (x + self.box_width / 2, y), DIMGRAY)
        y += FONT_HEIGHT + 12

        for slot in ITEM_SLOTS:
            ix = x + (self.box_width - 64) / 2
            self.draw_item(creature.equipment[slot], slot, ix, y, i)
            y += 76

    def draw_item(self, item: Item, slot: str, x: int, y: int, i: int):
        # item sprite: 4 * 12 = 48
        # item border: 48 + 16 = 64
        c = GREEN if self.index == i and self.item.slot == slot else GRAY
        self.draw_box((x, y, 64, 64), 4, c)
        if item:
            draw_sprite(self.canvas, item_sprites, item.sprite_rect, x + 8, y + 8, scale=4)
    