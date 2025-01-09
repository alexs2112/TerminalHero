from random import random, randint
from creature.creature import Creature
from combat.ability import Ability
from combat.effect_factory import get_effect_factory
from world.area import Area
from main.messenger import get_messenger

messenger = get_messenger()
effects = get_effect_factory()

# pylint: disable=invalid-name
_ability_factory = None
def get_ability_factory():
    global _ability_factory
    if not _ability_factory:
        _ability_factory = AbilityFactory()
    return _ability_factory

# A whole bunch of ability functions that are used many times
# pylint: disable=unused-argument
def attack_roll(c: Creature):
    return random() * (100 + c.stat('accuracy'))

def strength_melee_attack():
    def out(c: Creature, t: Creature, a: Area):
        success = attack_roll(c) > t.stat('dodge') * 5
        if not success:
            messenger.add(f"{c.name} misses {t.name} with an attack.")
        return success
    return out

def strength_melee_effect(dam_min, dam_max):
    def out(c: Creature, t: Creature, a: Area):
        dam = randint(dam_min + c.stat('strength'), dam_max + c.stat('strength'))
        messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
        t.take_damage(dam, 'physical')
    return out

class AbilityFactory:
    def basic_attack(self, min_damage, max_damage):
        a = Ability("Attack", cooldown=1)
        a.set_description("Melee attack an enemy.")
        a.set_to_hit(strength_melee_attack())
        def effect(c: Creature, t: Creature, a: Area):
            dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
            messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
            t.take_damage(dam, 'physical')
        a.set_effect(effect)
        return a

    # Sword
    def disarming_strike(self, min_damage, max_damage):
        a = Ability("Disarming Strike", cooldown=3)
        a.set_description("A precise hit that lowers your targets Accuracy.")
        a.set_to_hit(strength_melee_attack())
        def effect(c: Creature, t: Creature, a: Area):
            dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
            messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
            t.take_damage(dam, 'physical')
            if t.is_alive():
                t.add_effect(effects.create_disarmed_effect(1, 50))
        a.set_effect(effect)
        return a

    # Hammer
    def heavy_blow(self, min_damage, max_damage, base_stun_chance):
        # Higher cooldown to make up for it basically being strictly better than disarming_strike
        a = Ability("Heavy Blow", cooldown=4)
        a.set_description("Swing a heavy blow to stun your target.")
        a.set_to_hit(strength_melee_attack())
        def effect(c: Creature, t: Creature, a: Area):
            dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
            messenger.add(f"{c.name} heavy attacks {t.name} for {dam} damage!")
            t.take_damage(dam, 'physical')
            if t.is_alive():
                roll = random() * 100
                if roll < base_stun_chance - t.stat('endurance') * 5 + c.stat('strength') * 5:
                    t.add_effect(effects.create_stun_effect(1))
                else:
                    messenger.add(f"{t.name} shrugs off the stun.")
        a.set_effect(effect)
        return a

    # Axe
    def cleave(self, min_damage, max_damage, splash_damage):
        a = Ability("Cleave", cooldown=2)
        a.set_description("Cleave through your target, dealing damage to each other enemy.")
        a.set_to_hit(strength_melee_attack())
        def effect(c: Creature, t: Creature, a: Area):
            dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
            messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
            t.take_damage(dam, 'physical')
            for e in a.get_encounter().enemies:
                if t != e:
                    roll = random() * 100
                    success = roll > e.stat('dodge') * 5
                    if success:
                        dam = randint(splash_damage, splash_damage + c.stat('strength'))
                        messenger.add(f"{e.name} takes {dam} cleave damage!")
                        e.take_damage(dam, 'physical')
        a.set_effect(effect)
        return a

    def flickering_flames(self, base_hit_chance):
        a = Ability("Flickering Flames", cooldown=3)
        a.set_description("Attempt to light an enemy on fire.")
        def to_hit(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > (100-base_hit_chance) + t.stat('dodge') * 5 - c.stat('intelligence') * 5
            if not success:
                messenger.add(f"{c.name} throws flame at {t.name} but misses.")
            return success
        a.set_to_hit(to_hit)
        def effect(c: Creature, t: Creature, a: Area):
            messenger.add(f"{c.name} casts Flickering Flames.")
            t.add_effect(effects.create_burning_effect(c.stat('intelligence'), 2 + c.stat('intelligence')))
        a.set_effect(effect)
        return a

    # Necromancer
    def drain_life(self, base_hit_chance, min_damage, max_damage):
        a = Ability("Drain Life", cooldown=1)
        a.set_description("Deal Dark damage, restore half of damage dealt to your armor.")
        def to_hit(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > (100-base_hit_chance) + t.stat('will') * 5
            if not success:
                messenger.add(f"{c.name} reaches out. {t.name} resists.")
            messenger.add(f"{c.name} reaches out.")
            return success
        a.set_to_hit(to_hit)
        def effect(c: Creature, t: Creature, a: Area):
            dam = randint(min_damage + c.stat('intelligence'), max_damage + c.stat('intelligence'))
            messenger.add(f"{t.name} takes {dam} damage!")
            d = t.take_damage(dam, 'dark')
            c.gain_armor(int(d/2))
        a.set_effect(effect)
        return a

    def corpse_explosion(self, min_damage, max_damage):
        a = Ability("Corpse Explosion", cooldown=4)
        a.set_description("Explode target inert corpse, dealing Dark damage to each enemy.")
        def to_hit(_, t: Creature, a: Area):
            if t.is_alive() or not t.has_corpse:
                # Come up with a way to just not make this a valid target, rather than failing and skipping your turn
                messenger.add("Must target an inert corpse.")
                return False
            return True
        a.set_to_hit(to_hit)
        def effect(c: Creature, t: Creature, a: Area):
            messenger.add(f"{c.name} gestures and the corpse of {t.name} explodes!")
            t.has_corpse = False
            multiplier = 1
            for e in a.get_encounter().enemies:
                if not e.is_alive() and e.has_corpse:
                    multiplier += 1
            # Figure out a way to also count dead party members
            for e in a.get_encounter().enemies:
                if e.is_alive() and attack_roll(c) > e.stat('endurance') * 5:
                    base_dam = randint(min_damage + c.stat('intelligence'), max_damage + c.stat('intelligence'))
                    dam = base_dam * multiplier
                    messenger.add(f"{e.name} takes {dam}{f' ({base_dam}x{multiplier})' if multiplier > 1 else ''} damage!")
                    e.take_damage(dam, 'dark')
        a.set_effect(effect)
        return a

    def curse_of_decay(self):
        a = Ability("Curse of Decay", cooldown=5)
        a.set_description("Target creature gains the Decaying status, reducing their resistance every turn.")
        def to_hit(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > t.stat('endurance') * 5
            if not success:
                messenger.add(f"{c.name} fails to curse {t.name}.")
            return success
        a.set_to_hit(to_hit)
        def effect(c: Creature, t: Creature, a: Area):
            dam = randint(int(c.stat('intelligence') / 2), c.stat('intelligence'))
            messenger.add(f"{t.name} takes {dam} damage!")
            t.take_damage(dam, 'dark')
            t.add_effect(effects.create_decaying_effect(4, c.stat('intelligence') * 3))
        a.set_effect(effect)
        return a
