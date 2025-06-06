from random import random
from combat.effect import Effect
from combat.damage import Damage
from main.colour import *
from main.messenger import get_messenger
messenger = get_messenger()

# Take fire damage at the start of the effect and at the start of each turn
class BurningEffect(Effect):
    def __init__(self, duration, damage, caster, shake_off_chance):
        super().__init__("Burning", duration, ORANGE)
        self.damage = damage
        self.caster = caster
        self.shake_off_chance = shake_off_chance

    def effect_start(self, creature):
        messenger.add(f"{creature.name} catches fire!")
        self.deal_damage(creature)

    def effect_turn(self, creature):
        self.deal_damage(creature)
        if random() * 100 < self.shake_off_chance + creature.stat('endurance') * 5:
            messenger.add(f"{creature.name} shakes off the fire.")
            self.duration = 0
        else:
            self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} puts out the flames.")

    def deal_damage(self, creature):
        damage = self.damage.clone()
        damage = self.caster.calculate_total_damage(creature, self.damage)
        dam = damage.roll_damage()
        messenger.add(f"{creature.name} burns for {dam} :ORANGE:Fire Damage:ORANGE:.")
        creature.take_damage(dam)

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            min_dam = max(self.damage.min, other_effect.damage.min)
            max_dam = max(self.damage.max, other_effect.damage.max)
            self.damage = Damage(min_dam, max_dam, 'fire')
            self.duration = max(other_effect.duration, self.duration)
            self.shake_off_chance = max(other_effect.shake_off_chance, self.shake_off_chance)
            messenger.add("The flames burn brighter!")
            self.deal_damage(creature)
            return True
        return False

# Drastically reduce your accuracy
class DisarmedEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Disarmed", duration, DIMGRAY)
        self.strength = strength

    def effect_start(self, creature):
        creature.add_temp_stats(accuracy=-self.strength)

    def effect_turn(self, _):
        self.duration -= 1

    def effect_end(self, creature):
        creature.add_temp_stats(accuracy=self.strength)

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.effect_end(creature)
            self.strength = max(self.strength, other_effect.strength)
            self.effect_start(creature)
            return True
        return False

# Skip your turn, still gain AP
class DazedEffect(Effect):
    def __init__(self, duration):
        super().__init__("Dazed", duration, GRAY)

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :GRAY:Dazed:GRAY:.")
        # skip_next_turn gets reset at the start of a creatures turn, doesn't need to go here

    def effect_turn(self, creature):
        messenger.add(f"{creature.name} is :GRAY:Dazed:GRAY:.")
        creature.skip_next_turn = True
        self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} recovers from the stun.")

    def combine(self, _, other_effect):
        if other_effect.name == self.name:
            self.duration += other_effect.duration
            return True
        return False

# Gain no AP this turn
class ShockEffect(Effect):
    def __init__(self, duration):
        super().__init__("Shocked", duration, CYAN)

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :CYAN:Shocked:CYAN:.")
        # skip_next_turn gets reset at the start of a creatures turn, doesn't need to go here

    def effect_turn(self, creature):
        messenger.add(f"{creature.name} is :CYAN:Shocked:CYAN:.")

        # There is probably a better way to do this, but this works for now
        creature.action_points -= creature.action_point_replenish
        self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} recovers from the shock.")

# Skip your turn and gain no AP
class StunEffect(Effect):
    def __init__(self, duration):
        super().__init__("Stunned", duration, CYAN)

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :CYAN:Stunned:CYAN:.")
        # skip_next_turn gets reset at the start of a creatures turn, doesn't need to go here

    def effect_turn(self, creature):
        messenger.add(f"{creature.name} is :CYAN:Stunned:CYAN:.")
        creature.skip_next_turn = True

        # There is probably a better way to do this, but this works for now
        creature.action_points -= creature.action_point_replenish
        self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} recovers from the stun.")

    def combine(self, _, other_effect):
        if other_effect.name == self.name:
            self.duration += other_effect.duration
            return True
        return False

# Reduce all resistances by an increasing amount every turn
class DecayingEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Decaying", duration, BLUEVIOLET)
        self.strength = strength
        self.total = 0

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :BLUEVIOLET:Decaying:BLUEVIOLET:.")

    def effect_turn(self, creature):
        messenger.add(f"{creature.name} :BLUEVIOLET:Decays:BLUEVIOLET:.")
        self.total += self.strength
        creature.add_temp_resistances(
            physical=-self.strength,
            fire=-self.strength,
            cold=-self.strength,
            air=-self.strength,
            poison=-self.strength,
            holy=-self.strength,
            dark=-self.strength
        )
        self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} recovers from :BLUEVIOLET:Decaying:BLUEVIOLET:.")
        creature.add_temp_resistances(
            physical=self.total,
            fire=self.total,
            cold=self.total,
            air=self.total,
            poison=self.total,
            holy=self.total,
            dark=self.total
        )

    def combine(self, _, other_effect):
        if other_effect.name == self.name:
            self.duration = max(self.duration, other_effect.duration)
            self.strength = max(self.strength, other_effect.strength)
            return True
        return False

# Buff your offensive stats and recover some armor
class BolsteredEffect(Effect):
    def __init__(self, duration, str_buff, armor_buff):
        super().__init__("Bolstered", duration, LIGHTGRAY)
        self.str_buff = str_buff
        self.armor_buff = armor_buff

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :LIGHTGRAY:Bolstered:LIGHTGRAY:.")
        creature.gain_armor(self.armor_buff)
        creature.add_temp_stats(
            strength=self.str_buff,
            dexterity=self.str_buff,
            intelligence=self.str_buff,
            wisdom=self.str_buff
        )

    def effect_turn(self, _):
        self.duration -= 1

    def effect_end(self, creature):
        creature.add_temp_stats(
            strength=-self.str_buff,
            dexterity=-self.str_buff,
            intelligence=-self.str_buff,
            wisdom=-self.str_buff
        )

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.effect_end(creature)
            self.armor_buff = max(self.armor_buff, other_effect.armor_buff)
            self.str_buff = max(self.str_buff, other_effect.str_buff)
            self.duration = max(self.duration, other_effect.duration)
            self.effect_start(creature)
            return True
        return False

# Take physical damage every turn, ignoring armor
class BleedEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Bleeding", duration, RED)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is bleeding!")

    def effect_turn(self, creature):
        dam = creature.take_damage(self.strength, ignore_armor=True)
        messenger.add(f"{creature.name} bleeds for {dam} damage.")
        self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} stops bleeding.")

    def combine(self, _, other_effect):
        if other_effect.name == self.name:
            self.duration = max(other_effect.duration, self.duration)
            self.strength = max(other_effect.strength, self.strength)
            return True
        return False

# Boosts your armor, can go past your usual maximum
class ArmorEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Armored", duration, LIGHTGRAY)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} strengthens their armor.")
        creature.add_temp_stats(defense=self.strength)

    def effect_turn(self, _):
        self.duration -= 1

    def effect_end(self, creature):
        creature.add_temp_stats(defense=-self.strength)

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.effect_end(creature)
            self.duration = max(other_effect.duration, self.duration)
            self.strength = max(other_effect.strength, self.strength)
            self.effect_start(creature)
            return True
        return False

# Reduce resistance to dark damage
class DrainedEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Drained", duration, BLUEVIOLET)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} has reduced resistance to Dark.")
        creature.add_temp_resistances(dark = -self.strength)

    def effect_turn(self, _):
        self.duration -= 1

    def effect_end(self, creature):
        creature.add_temp_resistances(dark = self.strength)

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.effect_end(creature)
            self.duration = max(other_effect.duration, self.duration)
            self.strength = max(other_effect.strength, self.strength)
            self.effect_start(creature)
            return True
        return False

# Reduce your accuracy
class BlindedEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Blinded", duration, GRAY)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is blinded.")
        creature.add_temp_stats(accuracy=-self.strength)

    def effect_turn(self, _):
        self.duration -= 1

    def effect_end(self, creature):
        creature.add_temp_stats(accuracy=self.strength)

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.effect_end(creature)
            self.duration = max(other_effect.duration, self.duration)
            self.strength = max(other_effect.strength, self.strength)
            self.effect_start(creature)
            return True
        return False

# Higher priority to the target that challenged them, the challenger deals additional percentage damage to this creature
class ChallengedEffect(Effect):
    # Checked when calculating default_offensive_priority
    def __init__(self, duration, strength, creature):
        super().__init__("Challenged", duration, YELLOW)
        self.strength = strength
        self.creature = creature

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :YELLOW:Challenged:YELLOW: by {self.creature.name}")

    def effect_turn(self, _):
        self.duration -= 1

    def modify_total_damage(self, attacker, damage):
        if attacker == self.creature:
            damage.apply_multiplier(1 + self.strength / 100)

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.effect_end(creature)
            self.duration = other_effect.duration
            self.strength = other_effect.strength
            self.creature = other_effect.creature
            self.effect_start(creature)
            return True
        return False

# Reduce accuracy and armor, increase fire resistance, if shocked by lightning you become stunned instead
class WetEffect(Effect):
    def __init__(self, duration, damage, strength):
        super().__init__("Wet", duration, BLUE)
        self.damage = damage
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :BLUE:Wet:BLUE:.")
        creature.add_temp_stats(accuracy=-self.strength)
        creature.add_temp_resistances(fire=25)
        creature.armor = max(creature.armor - self.damage, 0)

    def effect_turn(self, _):
        self.duration -= 1

    def effect_end(self, creature):
        creature.add_temp_stats(accuracy=self.strength)
        creature.add_temp_resistances(fire=-25)

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.effect_end(creature)
            self.duration = max(other_effect.duration, self.duration)
            self.strength = max(other_effect.strength, self.strength)
            self.damage = other_effect.damage
            self.effect_start(creature)
            return True
        elif other_effect.name == "Shocked":
            self.effect_end(creature)
            creature.effects.remove(self)
            creature.add_effect(StunEffect(1))
            messenger.add(f"Electricity runs through the water and :CYAN:Stuns:CYAN: {creature.name}.")
            return True
        return False

class EnchantedWeaponEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Holy Weapon", duration, YELLOW)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} imbues their weapon with a holy light.")

    def effect_turn(self, _):
        self.duration -= 1

    def modify_base_damage(self, _, damage):
        # Assume that physical damage is a weapon attack
        if damage.type == 'physical':
            damage.add_damage(self.strength)
            damage.type = 'holy'

    def effect_end(self, creature):
        messenger.add(f"The holy light of {creature.name}'s weapon fades.")

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.duration = other_effect.duration
            self.strength = other_effect.strength
            self.effect_start(creature)
            return True
        return False

class PoisonedEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Poisoned", duration, BLUEVIOLET)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :BLUEVIOLET:Poisoned:BLUEVIOLET:.")
        creature.add_temp_stats(
            strength = -self.strength,
            dexterity = -self.strength,
            intelligence = -self.strength,
            wisdom = -self.strength
        )

    def effect_turn(self, _):
        self.duration -= 1

    def effect_end(self, creature):
        creature.add_temp_stats(
            strength = self.strength,
            dexterity = self.strength,
            intelligence = self.strength,
            wisdom = self.strength
        )

    def combine(self, creature, other_effect):
        if other_effect.name == self.name:
            self.effect_end(creature)
            self.duration = max(other_effect.duration, self.duration)
            self.strength = max(other_effect.strength, self.strength)
            self.effect_start(creature)
            return True
        return False
