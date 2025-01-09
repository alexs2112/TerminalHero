from random import random, randint
from creature.creature import Creature
from combat.ability import Ability
from combat.ability_function_factory import get_ability_function_factory
from combat.effect_factory import get_effect_factory
from world.area import Area
from main.messenger import get_messenger

messenger = get_messenger()
effects = get_effect_factory()
function_factory = get_ability_function_factory()

# pylint: disable=invalid-name
_ability_factory = None
def get_ability_factory():
    global _ability_factory
    if not _ability_factory:
        _ability_factory = AbilityFactory()
    return _ability_factory

# pylint: disable=unused-argument
class AbilityFactory:
    def basic_attack(self, min_damage, max_damage):
        a = Ability("Attack", cooldown=1)
        a.set_description("Melee attack an enemy.")
        a.set_to_hit(function_factory.strength_melee_attack())
        a.set_effect(function_factory.strength_melee_effect(min_damage, max_damage))
        return a

    def heavy_blow(self, min_damage, max_damage):
        a = Ability("Heavy Blow", cooldown=3)
        a.set_description("Swing a heavy blow to stun your target.")
        a.set_to_hit(function_factory.heavy_blow_attack())
        a.set_effect(function_factory.heavy_blow_effect(min_damage, max_damage, 90))
        return a

    def flickering_flames(self, base_hit_chance):
        a = Ability("Flickering Flames", cooldown=3)
        a.set_description("Attempt to light an enemy on fire.")
        a.set_to_hit(function_factory.flickering_flames_attack(base_hit_chance))
        a.set_effect(function_factory.flickering_flames_effect())
        return a

    # Necromancer
    def drain_life(self, base_hit_chance, min_damage, max_damage):
        a = Ability("Drain Life", cooldown=1)
        a.set_description("Deal Dark damage, restore half of damage dealt to your armor.")
        def to_hit(c: Creature, t: Creature, a: Area):
            roll = random() * 100
            success = roll < base_hit_chance - t.stat('will') * 5
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
                if e.is_alive() and random() * 100 > e.stat('endurance') * 5:
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
            roll = random() * 100
            success = roll > t.stat('endurance') * 5
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
