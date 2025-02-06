from main.messenger import *
from combat.ability import Ability
from combat.effect import Effect
from creature.profession import Profession
from creature.creature_sprite import CreatureSprite
from item.item import *

messenger = get_messenger()

class Creature:
    def __init__(self, name, level):
        self.name = name
        self.description = "placeholder text"
        self.type = 'creature'
        self.sprite: CreatureSprite = None

        self.level = level
        self.abilities: list[Ability] = []
        self.ai = None
        self.profession: Profession = None

        # Floating stat and ability points for leveling up
        self.stat_points = 0
        self.ability_points = 0

        self.base_hp = 0
        self.hp = 0
        self.armor = 0

        self.stats = {
            # Defensive Stats
            'defense': 0,   # Bonus to max_armor
            'dodge': 0,
            'will': 0,
            'endurance': 0,

            # Offensive Stats
            'speed': 0,
            'accuracy': 0,
            'strength': 0,
            'dexterity': 0,
            'intelligence': 0,
            'wisdom': 0
        }
        self.temporary_stats = {}

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
        self.temporary_resistances = {}

        self.equipment: dict[str, Item] = {}
        for slot in ITEM_SLOTS:
            self.equipment[slot] = None

        # Combat Status effects
        self.effects: list[Effect] = []
        self.skip_next_turn = False
        self.has_corpse = True
        self.action_points = 0
        self.action_point_replenish = 2

        # The food the creature has eaten, stats will be stored in temporary_stats
        self.food = None

        # If this creature is allied with the player
        self.allied = False

    def set_description(self, description):
        self.description = description

    def set_sprite(self, sprite: CreatureSprite):
        self.sprite = sprite
        self.update_sprite()

    def get_sprite(self):
        return self.sprite.get_sprite(self)

    def update_sprite(self):
        self.sprite.update(self)

    def set_profession(self, profession):
        self.profession = profession

    def set_defensive_stats(self, base_hp, defense, dodge, will, endurance):
        self.base_hp = base_hp

        # Essentially additional health that refreshes at the start of each combat
        self.armor = defense
        self.stats['defense'] = defense

        # Ability to resist status effects and certain attacks
        self.stats['dodge'] = dodge
        self.stats['will'] = will
        self.stats['endurance'] = endurance

        self.hp = self.max_hp()

    def set_offensive_stats(self, speed, strength, dexterity, intelligence, wisdom):
        # Determines turn order
        self.stats['speed'] = speed

        # Attributes that benefit abilities
        self.stats['strength'] = strength
        self.stats['dexterity'] = dexterity
        self.stats['intelligence'] = intelligence
        self.stats['wisdom'] = wisdom

    def add_temp_stats(self, **kwargs):
        old_hp = self.max_hp()
        old_armor = self.max_armor()

        for stat, value in kwargs.items():
            if stat in self.temporary_stats:
                self.temporary_stats[stat] += value
            else:
                self.temporary_stats[stat] = value

        # Make sure benefits to endurance/defense are represented
        if self.max_hp() > old_hp:
            self.hp += self.max_hp() - old_hp
        if self.max_armor() > old_armor:
            self.armor += self.max_armor() - old_armor
        if self.hp > self.max_hp():
            self.hp = self.max_hp()
        if self.armor > self.max_armor():
            self.armor = self.max_armor()

    def stat(self, stat_name):
        s = self.stats[stat_name]
        if self.profession and stat_name in self.profession.stats:
            s += self.profession.stats[stat_name]
        if stat_name in self.temporary_stats:
            s += self.temporary_stats[stat_name]
        for item in self.equipment.values():
            if item and stat_name in item.stats:
                s += item.stats[stat_name]
        return s

    def max_hp(self):
        return self.base_hp + self.stat('endurance') * self.level

    def max_armor(self):
        return self.stat('defense') + self.level

    def gain_hp(self, num):
        diff = min(self.max_hp() - self.hp, num)
        self.hp += diff
        return diff

    def gain_armor(self, num):
        diff = min(self.max_armor() - self.armor, num)
        self.armor += diff
        return diff

    def set_resistances(self, **kwargs):
        for key, value in kwargs.items():
            self.resistances[key] = value

    def add_temp_resistances(self, **kwargs):
        for resist, value in kwargs.items():
            if resist in self.temporary_resistances:
                self.temporary_resistances[resist] += value
            else:
                self.temporary_resistances[resist] = value

    def get_resistance(self, resistance):
        r = self.resistances[resistance]
        if self.profession and resistance in self.profession.resistances:
            r += self.profession.resistances[resistance]
        if resistance in self.temporary_resistances:
            r += self.temporary_resistances[resistance]
        for item in self.equipment.values():
            if item and resistance in item.resistances:
                r += item.resistances[resistance]
        return r

    def add_ability(self, ability: Ability):
        self.abilities.append(ability)

    def get_abilities(self):
        a = self.abilities.copy()
        for item in self.equipment.values():
            if item and item.abilities:
                a += item.abilities
        if self.profession:
            a += self.profession.abilities
        return a

    def has_usable_abilities(self):
        for a in self.get_abilities():
            if a.is_usable(self):
                return True
        return False

    def equip_item(self, item: Item):
        old = None
        if self.equipment[item.slot]:
            old = self.equipment[item.slot]
        self.equipment[item.slot] = item
        self.update_sprite()
        return old

    def set_ai(self, ai):
        self.ai = ai

    def start_turn(self):
        self.skip_next_turn = False
        self.action_points = min(self.action_points + self.action_point_replenish, 4)
        for a in self.get_abilities():
            a.cooldown = max(0, a.cooldown - 1)
        for e in self.effects:
            e.effect_turn(self)

    def end_turn(self):
        to_remove: list[Effect] = []
        for e in self.effects:
            if e.duration <= 0:
                to_remove.append(e)

        for e in to_remove:
            e.effect_end(self)
            self.effects.remove(e)

    def take_turn(self, player, area):
        if self.ai:
            self.ai.take_turn(player, area)

    def use_ability(self, ability: Ability, target, area):
        ability.set_cooldown()
        ability.activate(self, target, area)

    def take_damage(self, damage: int, dam_type: str, ignore_armor=False):
        dam = int(damage * (100 - self.get_resistance(dam_type)) / 100)
        total_dam = dam
        if not ignore_armor and self.armor > 0:
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

        # For now just remove all active effects
        # We may want to revisit this in the future
        self.effects.clear()

    def add_effect(self, effect: Effect):
        dont_apply = False
        for e in self.effects:
            # If this new effect successfully combines with a current one, don't apply it
            if e.combine(self, effect):
                dont_apply = True

        if not dont_apply:
            self.effects.append(effect)
            effect.effect_start(self)

    def has_effect(self, effect_name: str):
        for e in self.effects:
            if e.name == effect_name:
                return True
        return False

    def eat_food(self, food):
        self.food = food
        self.add_temp_stats(**food.stats)
        self.add_temp_resistances(**food.resistances)

    def refresh(self):
        self.temporary_stats = {}
        self.temporary_resistances = {}
        self.effects = []
        self.hp = self.max_hp()
        self.armor = self.max_armor()
        self.food = None
