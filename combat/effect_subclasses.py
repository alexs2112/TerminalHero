from combat.effect import Effect
from main.colour import *
from main.messenger import get_messenger
messenger = get_messenger()

class BurningEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Burning", duration, ORANGE)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} catches fire!")
        dam = creature.take_damage(self.strength, 'fire')
        messenger.add(f"{creature.name} burns for {dam} :ORANGE:fire damage:ORANGE:!")

    def effect_turn(self, creature):
        dam = creature.take_damage(self.strength, 'fire')
        messenger.add(f"{creature.name} burns for {dam} :ORANGE:fire damage:ORANGE:!")
        self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} puts out the flames.")

    def combine(self, _, other_effect):
        if other_effect.name == self.name:
            self.duration = max(other_effect.duration, self.duration)
            self.strength = max(other_effect.strength, self.strength)
            messenger.add("The flames burn brighter!")
            return True
        return False

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

class StunEffect(Effect):
    def __init__(self, duration):
        super().__init__("Stunned", duration, CYAN)

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is :CYAN:stunned:CYAN:.")
        # skip_next_turn gets reset at the start of a creatures turn, doesn't need to go here

    def effect_turn(self, creature):
        messenger.add(f"{creature.name} is :CYAN:stunned:CYAN:.")
        creature.skip_next_turn = True
        self.duration -= 1

    def effect_end(self, creature):
        messenger.add(f"{creature.name} recovers from the stun.")

    def combine(self, _, other_effect):
        if other_effect.name == self.name:
            self.duration += other_effect.duration
            return True
        return False

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
            intelligence=self.str_buff
        )

    def effect_turn(self, _):
        self.duration -= 1

    def effect_end(self, creature):
        creature.add_temp_stats(
            strength=-self.str_buff,
            dexterity=-self.str_buff,
            intelligence=-self.str_buff
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

class BleedEffect(Effect):
    def __init__(self, duration, strength):
        super().__init__("Bleeding", duration, RED)
        self.strength = strength

    def effect_start(self, creature):
        messenger.add(f"{creature.name} is bleeding!")

    def effect_turn(self, creature):
        dam = creature.take_damage(self.strength, 'physical', ignore_armor=True)
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
