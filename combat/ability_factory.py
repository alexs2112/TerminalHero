from random import random, randint
from creature.creature import Creature
from creature.player import Player
from creature.ai.priority import Priority
from combat.ability import Ability
from combat.effect_factory import get_effect_factory
from world.area import Area
from world.encounter import Encounter
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
    return random() * (100 + 5 * c.stat('accuracy'))

def strength_melee_attack(c: Creature, t: Creature):
    success = attack_roll(c) > t.stat('dodge') * 5
    if not success:
        messenger.add(f"{c.name} misses {t.name} with an attack.")
    return success

def default_offensive_priority(a: Ability, c: Creature, p: Player, e: Encounter):
    # Assume they will only target creatures allied to the player
    out = []
    for ally in p.party:
        if a.can_target(ally):
            # Priority 1 of using this ability on that ally
            out.append(Priority(a, ally, 1))
    return out

def high_offensive_priority(a: Ability, c: Creature, p: Player, e: Encounter):
    out = default_offensive_priority(a,c,p,e)
    for prio in out:
        prio.priority = 3
    return out

def default_bolstered_priority(a: Ability, c: Creature, p: Player, e: Encounter):
    # Assume they will only target creatures friendly to the enemy
    out = []
    for enemy in e.enemies:
        if a.can_target(enemy):
            if enemy.has_effect('Bolstered'):
                if enemy.armor < enemy.max_armor() / 2:
                    prio = 2
                else:
                    prio = 0
            else:
                if enemy.armor < enemy.max_armor() / 2:
                    prio = 3
                else:
                    prio = 1
            out.append(Priority(a, enemy, prio))
    return out

class AbilityFactory:
    def basic_attack(self, min_damage, max_damage):
        a = Ability("Attack", cooldown=1, cost=1)
        a.set_description("Melee attack an enemy.")
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            if strength_melee_attack(c, t):
                dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
                messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
                t.take_damage(dam, 'physical')
        a.set_effect(effect)
        return a

    def slow_attack(self, min_damage, max_damage):
        a = self.basic_attack(min_damage, max_damage)
        a.action_points = 2
        return a

    def multi_attack(self, min_damage, max_damage, num_attacks=2):
        a = Ability("Multi-Attack", cooldown=1, cost=3)
        a.set_description("Make two melee attacks.")
        a.set_target_priority(high_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            for _ in range(num_attacks):
                if strength_melee_attack(c, t):
                    dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
                    messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
                    t.take_damage(dam, 'physical')
        a.set_effect(effect)
        return a

    def elemental_attack(self, min_damage, max_damage, damage_type, damage_stat):
        a = Ability("Attack", cooldown=1, cost=1)
        a.set_description(f"Attack an enemy for {damage_type} damage.")
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > t.stat('dodge') * 5
            if success:
                dam = randint(min_damage + c.stat(damage_stat), max_damage + c.stat(damage_stat))
                messenger.add(f"{c.name} attacks {t.name} for {dam} {damage_type} damage!")
                t.take_damage(dam, damage_type)
            else:
                messenger.add(f"{c.name} misses {t.name} with an attack.")
        a.set_effect(effect)
        return a

    def flickering_flames(self, base_hit_chance):
        a = Ability("Flickering Flames", cooldown=3)
        a.set_description("Attempt to light an enemy on fire.")
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > (100-base_hit_chance) + t.stat('dodge') * 5 - c.stat('intelligence') * 5
            if success:
                messenger.add(f"{c.name} casts Flickering Flames.")
                t.add_effect(effects.create_burning_effect(c.stat('intelligence'), 2 + c.stat('intelligence')))
            else:
                messenger.add(f"{c.name} throws flame at {t.name} but misses.")
        a.set_effect(effect)
        return a

    # Sword
    def disarming_strike(self, min_damage, max_damage):
        a = Ability("Disarming Strike", cooldown=2)
        a.set_description("A precise hit that lowers your targets Accuracy.")
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            if strength_melee_attack(c,t):
                dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
                messenger.add(f"{c.name} attacks {t.name} for {dam} damage!")
                t.take_damage(dam, 'physical')
                if t.is_alive():
                    t.add_effect(effects.create_disarmed_effect(1, 50))
        a.set_effect(effect)
        return a

    # Hammer
    def heavy_blow(self, min_damage, max_damage, base_stun_chance):
        a = Ability("Heavy Blow", cooldown=2, cost=2)
        a.set_description("Swing a heavy blow to stun your target.")
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            if strength_melee_attack(c,t):
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
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            if strength_melee_attack(c,t):
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

    # Soulwarden
    def drain_life(self, base_hit_chance, min_damage, max_damage):
        a = Ability("Drain Life", cooldown=2)
        a.set_description("Deal Dark damage, restore half of damage dealt to your armor.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            out = default_offensive_priority(a,c,p,e)
            if c.armor < c.max_armor() * 0.6:
                i = 2
            else:
                i = -1
            for prio in out:
                prio.priority += i
            return out
        a.set_target_priority(priority)
        def effect(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > (100-base_hit_chance) + t.stat('will') * 5
            if success:
                messenger.add(f"{c.name} casts Drain Life.")
                dam = randint(min_damage + c.stat('intelligence'), max_damage + c.stat('intelligence'))
                messenger.add(f"{t.name} takes {dam} damage!")
                d = t.take_damage(dam, 'dark')
                c.gain_armor(int(d/2))
            else:
                messenger.add(f"{c.name} casts Drain Life. {t.name} resists.")
        a.set_effect(effect)
        return a
    def corpse_explosion(self, min_damage, max_damage):
        a = Ability("Corpse Explosion", cooldown=4, cost=3)
        a.set_description("Explode target inert corpse, dealing Dark damage to each enemy.")
        def can_target(t: Creature):
            return not t.is_alive() and t.has_corpse
        a.set_can_target(can_target)
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
        a = Ability("Curse of Decay", cooldown=4)
        a.set_description("Target creature gains the Decaying status, reducing their resistance every turn.")
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > t.stat('endurance') * 5
            if success:
                messenger.add(f"{c.name} casts Curse of Decay.")
                dam = randint(int(c.stat('intelligence') / 2), c.stat('intelligence'))
                messenger.add(f"{t.name} takes {dam} damage!")
                t.take_damage(dam, 'dark')
                t.add_effect(effects.create_decaying_effect(4, c.stat('intelligence') * 3))
            else:
                messenger.add(f"{c.name} casts Curse of Decay. {t.name} resists.")
        a.set_effect(effect)
        return a

    # Lanternbearer
    def pale_light(self):
        a = Ability("Pale Light", cooldown=3, cost=2)
        a.set_description("Wave the Pale Lantern, providing armor and strength to a target.")
        a.set_target_priority(default_bolstered_priority)
        def effect(c: Creature, t: Creature, a: Area):
            messenger.add(f"{c.name} waves their :BLUEVIOLET:Pale Lantern:BLUEVIOLET:.")
            t.add_effect(effects.create_bolstered_effect(3, c.stat('intelligence'), c.stat('intelligence') + 2))
        a.set_effect(effect)
        return a

    # Rotten Stray
    def rabid_bite(self, min_damage, max_damage):
        a = Ability("Rabid Bite", cooldown=2, cost=2)
        a.set_description("A quick attack with a chance to bleed the target.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            out = high_offensive_priority(a,c,p,e)
            for prio in out:
                if prio.target.has_effect('Bleeding'):
                    prio.priority -= 1
            return out
        a.set_target_priority(priority)
        def effect(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > t.stat('dodge') * 5
            if success:
                messenger.add(f"{c.name} bites the {t.name}.")
                dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
                messenger.add(f"{t.name} takes {dam} damage!")
                t.take_damage(dam, 'physical')
                if t.is_alive():
                    roll = random() * 75
                    if roll > t.stat('endurance') * 5:
                        t.add_effect(effects.create_bleed_effect(3, 1))
            else:
                messenger.add(f"{c.name} bites at {t.name} but misses.")
        a.set_effect(effect)
        return a
    def chilling_howl(self, name):
        a = Ability("Chilling Howl", cooldown=4, cost=2)
        a.set_description("Howl, providing buffs to other Rotten Strays.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            if c.has_effect('Bolstered'):
                return [ Priority(a, c, 0) ]
            return [ Priority(a, c, 4) ]
        a.set_target_priority(priority)
        def effect(c: Creature, t: Creature, a: Area):
            messenger.add(f"{c.name} lets out a chilling howl.")
            for e in a.get_encounter().enemies:
                if e.name == name and e.is_alive():
                    e.add_effect(effects.create_bolstered_effect(2, 2, 2))
        a.set_effect(effect)
        return a

    # Runebound Stalker
    def astral_lightning(self):
        a = Ability("Astral Lightning", cooldown=2, cost=3)
        a.set_description("Astral lightning jumps from your target to several others.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            return [ Priority(a, c, 4) ]
        a.set_target_priority(priority)
        def effect(c: Creature, t: Creature, a: Area):
            messenger.add(f"{c.name} conjurs :CYAN:Astral Lightning:CYAN:.")
            for target in a.player.party:
                at_least_one_hit = False
                if target.is_alive():
                    success = attack_roll(c) > target.stat('dodge') * 5
                    if success:
                        at_least_one_hit = True
                        dam = randint(c.stat('intelligence'), c.stat('intelligence') + 2)
                        messenger.add(f"{target.name} is struck for {dam} damage.")
                        target.take_damage(dam, 'air')
                if not at_least_one_hit:
                    messenger.add("The lightning arcs wildly, missing all of you.")
        a.set_effect(effect)
        return a
    def runic_chains(self):
        a = Ability("Runic Chains", cooldown=3)
        a.set_description("Lash out with your chains, binding your target.")
        a.set_target_priority(high_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > t.stat('dodge') * 5
            if success:
                dam = randint(1 + c.stat('strength'), 3 + c.stat('strength'))
                messenger.add(f"{c.name} lashes out with :CYAN:Runic Chains:CYAN: at {t.name} for {dam} damage!")
                t.take_damage(dam, 'physical')
                if t.is_alive():
                    t.action_points -= 2
                    t.add_effect(effects.create_stun_effect(1))
            else:
                messenger.add(f"{c.name} lashes out with :CYAN:Runic Chains:CYAN: but misses {t.name}")
        a.set_effect(effect)
        return a

    # Bone Servitor
    def bone_shield(self, strength):
        a = Ability("Bone Shield", cooldown=3)
        a.set_description("Raise your shield, enhancing your armor for a time.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            if c.armor < c.max_armor() / 0.6:
                return [ Priority(a, c, 4) ]
            return [ Priority(a, c, 2) ]
        a.set_target_priority(priority)
        def effect(c: Creature, t: Creature, a: Area):
            c.add_effect(effects.create_armor_effect(3, strength))
        a.set_effect(effect)
        return a

    # Gravebound Watcher
    def hollow_gaze(self, min_damage, max_damage, resist_drain):
        a = Ability("Hollow Gaze", cooldown=3)
        a.set_description("Gaze at a target, dealing dark damage and reducing their dark resistance.")
        a.set_target_priority(high_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > t.stat('will') * 5
            if success:
                dam = randint(min_damage + c.stat('intelligence'), max_damage + c.stat('intelligence'))
                messenger.add(f"{c.name} gazes at {t.name}, draining their lifeforce for {dam} dark damage.")
                t.take_damage(dam, 'dark')
                if t.is_alive():
                    t.add_effect(effects.create_drained_effect(3, resist_drain))
            else:
                messenger.add(f"{c.name} gazes at {t.name} but {t.name} resists")
        a.set_effect(effect)
        return a
    def necrotic_chains(self, min_damage, max_damage, stun_chance):
        a = Ability("Necrotic Chains", cooldown=3)
        a.set_description("Wrap the target in Necrotic Chains, dealing dark damage and stunning them.")
        a.set_target_priority(high_offensive_priority)
        def effect(c: Creature, t: Creature, a: Area):
            success = attack_roll(c) > t.stat('dodge') * 5
            if success:
                dam = randint(min_damage + c.stat('intelligence'), max_damage + c.stat('intelligence'))
                messenger.add(f"{c.name} lashes out with :BLUEVIOLET:Necrotic Chains:BLUEVIOLET: at {t.name} for {dam} dark damage!")
                t.take_damage(dam, 'dark')
                if t.is_alive():
                    if random() * 100 < stun_chance:
                        t.add_effect(effects.create_stun_effect(1))
                    else:
                        messenger.add(f"{t.name} resists the chains effects.")
            else:
                messenger.add(f"{c.name} lashes out with :BLUEVIOLET:Necrotic Chains:BLUEVIOLET: but misses {t.name}")
        a.set_effect(effect)
        return a

    # Unhallowed Guardian
    def greataxe_slash(self, min_damage, max_damage):
        a = Ability("Greataxe Slash", cooldown=2)
        a.set_description("Swing a heavy greataxe blow, dealing damage to each enemy.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            return [ Priority(a, c, 3) ]
        a.set_target_priority(priority)
        def effect(c: Creature, _, a: Area):
            at_least_one = False
            messenger.add(f"The {c.name} swings their unholy greataxe in a wide arc.")
            for t in a.player.party:
                success = attack_roll(c) > t.stat('dodge') * 5
                if success:
                    at_least_one = True
                    dam = randint(min_damage + c.stat('strength'), max_damage + c.stat('strength'))
                    messenger.add(f"{t.name} is hit for {dam} damage!")
                    t.take_damage(dam, 'physical')
            if not at_least_one:
                messenger.add("The greataxe slash misses everyone...")
        a.set_effect(effect)
        return a
    def soul_drain(self, min_damage, max_damage, bonus_armor):
        a = Ability("Soul Drain", cooldown=4, cost=3)
        a.set_description("Call upon unholy energies to drain the souls of your enemies, replenishing yourself.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            if c.armor < c.max_armor() / 0.6:
                return [ Priority(a, c, 4) ]
            return [ Priority(a, c, 2) ]
        a.set_target_priority(priority)
        def effect(c: Creature, _, a: Area):
            at_least_one = False
            messenger.add(f"The {c.name} calls upon unholy energies.")
            armor = c.stat('intelligence')
            for t in a.player.party:
                success = random() * 85 > t.stat('will') * 5
                if success:
                    at_least_one = True
                    armor += bonus_armor
                    dam = randint(min_damage + c.stat('intelligence'), max_damage + c.stat('intelligence'))
                    messenger.add(f"{t.name} is drained for {dam} dark damage.")
                    t.take_damage(dam, 'dark')
            if at_least_one:
                messenger.add(f"The {c.name} replenishes {armor} armor.")
                c.gain_armor(armor)
            else:
                messenger.add("Everybody resists...")
        a.set_effect(effect)
        return a
