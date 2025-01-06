from main.messenger import *
from combat.ability import Ability
from combat.effect import Effect
from creature.profession import Profession

messenger = get_messenger()

class Creature:
    def __init__(self, name, sprite_rect):
        self.name = name
        self.sprite_rect = sprite_rect
        self.description = "placeholder text"

        self.level = 0
        self.abilities: list[Ability] = []
        self.ai = None
        self.profession: Profession = None

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
            'strength': 0,
            'dexterity': 0,
            'intelligence': 0
        }

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

        # Combat Status effects
        self.effects: list[Effect] = []
        self.skip_next_turn = False

    def set_description(self, description):
        self.description = description

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

    def stat(self, stat_name):
        s = self.stats[stat_name]
        if self.profession and stat_name in self.profession.stats:
            s += self.profession.stats[stat_name]
        return s

    def max_hp(self):
        return self.base_hp + self.stat('endurance') * 2

    def max_armor(self):
        return self.stat('defense')

    def set_resistances(self, **kwargs):
        for key, value in kwargs.items():
            self.resistances[key] = value

    def add_ability(self, ability: Ability):
        self.abilities.append(ability)

    def get_abilities(self):
        a = self.abilities
        if self.profession:
            return a + self.profession.abilities
        return a

    def set_ai(self, ai):
        self.ai = ai

    def start_turn(self):
        self.skip_next_turn = False
        for a in self.get_abilities():
            a.cooldown = max(0, a.cooldown - 1)

        to_remove: list[Effect] = []
        for e in self.effects:
            e.effect_turn(self)
            if e.duration <= 0:
                to_remove.append(e)

        for e in to_remove:
            e.effect_end(self)
            self.effects.remove(e)

    def take_turn(self, player, encounter):
        if self.ai:
            self.ai.take_turn(player, encounter)

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

    def add_effect(self, effect: Effect):
        for e in self.effects:
            # If this new effect successfully combines with a current one, don't apply it
            if e.combine(effect):
                return
        self.effects.append(effect)
        effect.effect_start(self)
