from main.messenger import *
from combat.ability import Ability
from combat.effect import Effect
from creature.profession import Profession
from creature.creature_sprite import CreatureSprite
from creature.item import *

messenger = get_messenger()

class Creature:
    def __init__(self, name):
        self.name = name
        self.description = "placeholder text"
        self.type = 'creature'
        self.sprite: CreatureSprite = None

        self.level = 0
        self.abilities: list[Ability] = []
        self.ai = None
        self.profession: Profession = None
        self.inventory: list[Item] = []

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
            'intelligence': 0
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

        # For NPCs
        self.dialog_function = None

        # Combat Status effects
        self.effects: list[Effect] = []
        self.skip_next_turn = False
        self.has_corpse = True

    def set_description(self, description):
        self.description = description

    def set_sprite(self, sprite: CreatureSprite):
        self.sprite = sprite

    def get_sprite_rect(self):
        return self.sprite.get(self)

    def set_profession(self, profession, level):
        self.profession = profession
        self.level = level

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

    def set_offensive_stats(self, speed, strength, dexterity, intelligence):
        # Determines turn order
        self.stats['speed'] = speed

        # Attributes that benefit abilities
        self.stats['strength'] = strength
        self.stats['dexterity'] = dexterity
        self.stats['intelligence'] = intelligence

    def add_temp_stats(self, **kwargs):
        for stat, value in kwargs.items():
            if stat in self.temporary_stats:
                self.temporary_stats[stat] += value
            else:
                self.temporary_stats[stat] = value

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
        return self.base_hp + self.stat('endurance') * 2

    def max_armor(self):
        return self.stat('defense')

    def gain_hp(self, num):
        self.hp = min(self.hp + num, self.max_hp())

    def gain_armor(self, num):
        self.armor = min(self.armor + num, self.max_armor())

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

    def equip_item(self, item: Item):
        old = None
        if self.equipment[item.slot]:
            old = self.equipment[item.slot]
        self.equipment[item.slot] = item
        return old

    def set_ai(self, ai):
        self.ai = ai

    def start_turn(self):
        self.skip_next_turn = False
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
        if ability.success(self, target, area):
            ability.apply(self, target, area)

    def take_damage(self, damage: int, dam_type: str):
        dam = int(damage * (100 - self.get_resistance(dam_type)) / 100)
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

        # For now just remove all active effects
        # We may want to revisit this in the future
        self.effects.clear()

    def add_effect(self, effect: Effect):
        for e in self.effects:
            # If this new effect successfully combines with a current one, don't apply it
            if e.combine(effect, self):
                return
        self.effects.append(effect)
        effect.effect_start(self)
