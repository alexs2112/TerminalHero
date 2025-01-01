from main.constants import *
from main.messenger import *
from combat.ability import Ability

messenger = get_messenger()

class Creature:
    def __init__(self, name, sprite_rect):
        self.name = name
        self.sprite_rect = sprite_rect
        self.description = ""

        self.abilities: list[Ability] = []
        self.ai = None

        # Defensive Stats
        self.max_hp = 0
        self.hp = 0
        self.max_armor = 0
        self.armor = 0
        self.dodge = 0
        self.will = 0
        self.endurance = 0

        # Offensive Stats
        self.speed = 0
        self.strength = 0
        self.dexterity = 0
        self.intelligence = 0

        # Resistances (as a percentage, can be positive or negative)
        self.resistances = {
            'physical': 0,
            'fire' : 0,
            'cold' : 0,
            'air'  : 0,
            'poison':0,
            'holy' : 0,
            'dark' : 0
        }

        # For NPCs
        self.dialog_function = None

    def set_description(self, description):
        self.description = description

    def set_defensive_stats(self, max_hp, armor, dodge, will, endurance):
        self.max_hp = max_hp
        self.hp = max_hp

        # Essentially additional health that refreshes at the start of each combat
        self.max_armor = armor
        self.armor = armor

        # Ability to resist status effects and certain attacks
        self.dodge = dodge
        self.will = will
        self.endurance = endurance

    def set_offensive_stats(self, speed, strength, dexterity, intelligence):
        # Determines turn order
        self.speed = speed

        # Attributes that benefit abilities
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence

    def set_resistances(self, **kwargs):
        for key, value in kwargs:
            self.resistances[key] = value

    def add_ability(self, ability: Ability):
        self.abilities.append(ability)

    def set_ai(self, ai):
        self.ai = ai

    def start_turn(self):
        for a in self.abilities:
            a.cooldown = max(0, a.cooldown - 1)

    def take_turn(self, player, area):
        if self.ai:
            self.ai.take_turn(player, area)

    def use_ability(self, ability: Ability, target):
        ability.set_cooldown()
        if ability.success(self, target):
            ability.apply(self, target)

    def take_damage(self, damage: int, dam_type: str):
        dam = int(damage * (100 - self.resistances[dam_type]) / 100)
        total_dam = dam
        if self.armor > 0:
            armor_dam = min(self.armor, dam)
            self.armor -= armor_dam
            dam -= armor_dam
        self.hp -= dam
        if self.hp <= 0:
            self.dies()
        return total_dam

    def is_alive(self):
        return self.hp > 0

    def dies(self):
        messenger.add(f"{self.name} dies.")
