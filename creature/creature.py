from main.constants import *
from main.messenger import *

messenger = get_messenger()

class Creature:
    def __init__(self, name, sprite_rect, max_hp, defense, armor, damage):
        self.name = name
        self.sprite_rect = sprite_rect
        self.max_hp = max_hp
        self.hp = max_hp
        self.defense = defense
        self.max_armor = armor
        self.armor = armor
        self.damage = damage
        self.ai = None

    def take_turn(self, allies, enemies):
        if self.ai:
            self.ai.take_turn(allies, enemies)

    def attack(self, target):
        dam = max(self.damage - target.defense, 0)
        total_dam = dam
        if target.armor > 0:
            armor_dam = min(target.armor, dam)
            target.armor -= armor_dam
            dam -= armor_dam
        target.hp -= dam
        messenger.add(f"{self.name} attacks {target.name} for {total_dam} damage.")
        if target.hp <= 0:
            target.dies()

    def is_alive(self):
        return self.hp > 0

    def dies(self):
        messenger.add(f"{self.name} dies.")
