from random import random, randint
from creature.creature import Creature
from creature.player import Player
from creature.ai.priority import Priority
from combat.ability import Ability
from combat.effect_factory import get_effect_factory
from combat.effect_subclasses import *
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
def attack_roll(c: Creature, base=100):
    return random() * (base + c.stat('accuracy'))

def basic_attack_roll(c: Creature, t: Creature):
    success = attack_roll(c) > t.stat('dodge') * 5
    if not success:
        messenger.add(f"{c.name} misses {t.name} with an attack.")
    return success

def default_offensive_priority(a: Ability, c: Creature, p: Player, e: Encounter):
    # Assume they will only target creatures allied to the player
    out = []
    for ally in p.party:
        if a.can_target(c, ally):
            # Priority 1 of using this ability on that ally
            out.append(Priority(a, ally, 1))

    for e in c.effects:
        if e.name == "Challenged":
            for prio in out:
                if prio.target == e.creature:
                    prio.priority += 2
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
        if a.can_target(c, enemy):
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

#pylint: disable=line-too-long, import-outside-toplevel
class AbilityFactory:
    def basic_attack(self, **scaling):
        a = Ability("Attack", cooldown=1, cost=1)
        a.set_description("Attack an enemy.")
        a.set_target_priority(default_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            if basic_attack_roll(c, t):
                damage = c.get_base_damage()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} attacks {t.name} for {dam} {damage.type} damage!")
                t.take_damage(dam)
        a.set_effect(effect)
        return a

    def slow_attack(self, **scaling):
        a = self.basic_attack(**scaling)
        a.action_points = 2
        return a

    def multi_attack(self, num_attacks=2, **scaling):
        a = Ability("Multi-Attack", cooldown=1, cost=3)
        a.set_description(f"Make {num_attacks} basic attacks.")
        a.set_target_priority(default_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            for _ in range(num_attacks):
                if basic_attack_roll(c, t):
                    damage = c.get_base_damage()
                    damage = a.scale_damage(damage, c)
                    damage = c.calculate_total_damage(t, damage)
                    dam = damage.roll_damage()
                    messenger.add(f"{c.name} attacks {t.name} for {dam} {damage.type} damage!")
                    t.take_damage(dam)
        a.set_effect(effect)
        return a

    # Sword
    def disarming_strike(self, **scaling):
        a = Ability("Disarming Strike", cooldown=2)
        a.set_description("A precise hit that lowers your targets Accuracy.")
        a.set_target_priority(default_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            if basic_attack_roll(c,t):
                damage = c.get_base_damage()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} attacks {t.name} for {dam} {damage.type} damage!")
                t.take_damage(dam)
                if t.is_alive():
                    t.add_effect(effects.create_disarmed_effect(1, 50))
        a.set_effect(effect)
        return a

    # Hammer
    def heavy_blow(self, base_stun_chance, **scaling):
        a = Ability("Heavy Blow", cooldown=2, cost=2)
        a.set_description("Swing a heavy blow to daze your target.")
        a.set_target_priority(default_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            if basic_attack_roll(c,t):
                damage = c.get_base_damage()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} heavy attacks {t.name} for {dam} {damage.type} damage!")
                t.take_damage(dam)
                if t.is_alive():
                    roll = random() * 100
                    if roll < base_stun_chance - t.stat('endurance') * 5 + c.stat('strength') * 5:
                        t.add_effect(DazedEffect(1))
                    else:
                        messenger.add(f"{t.name} shrugs off the daze.")
        a.set_effect(effect)
        return a

    # Axe
    def cleave(self, splash_multiplier, **scaling):
        a = Ability("Cleave", cooldown=2)
        a.set_description("Cleave through your target, dealing damage to each other enemy.")
        a.set_target_priority(default_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, area: Area):
            if basic_attack_roll(c,t):
                damage = c.get_base_damage()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} attacks {t.name} for {dam} {damage.type} damage!")
                t.take_damage(dam)
                if c.allied:
                    targets = area.get_encounter().enemies
                else:
                    targets = area.player.party
                for e in targets:
                    if t != e and e.is_alive():
                        if basic_attack_roll(c,e):
                            damage = c.get_base_damage()
                            damage = a.scale_damage(damage, c)
                            damage = c.calculate_total_damage(t, damage)
                            damage.apply_multiplier(splash_multiplier)
                            dam = damage.roll_damage()
                            messenger.add(f"{e.name} takes {dam} cleave damage!")
                            e.take_damage(dam)
        a.set_effect(effect)
        return a

    # Shortbow
    def power_shot(self, **scaling):
        a = self.basic_attack(**scaling)
        a.name = "Power Shot"
        a.action_points = 3
        return a

    # Warrior
    def bolster(self, strength, armour):
        a = Ability("Bolster", cooldown=3, cost=1)
        a.set_description("Recover some of your armor and increase strength for a time.")
        def can_target(c: Creature, o: Creature):
            return o == c
        a.set_can_target(can_target)
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            if c.armor < c.max_armor() * 0.5:
                return [ Priority(a, c, 4) ]
            return [ Priority(a, c, 0) ]
        a.set_target_priority(priority)
        def effect(c: Creature, *_):
            c.add_effect(effects.create_bolstered_effect(3, strength, armour))
        a.set_effect(effect)
        return a

    # Duelist
    def defensive_strike(self, **scaling):
        a = Ability("Defensive Strike", cooldown=2, cost=2)
        a.set_description("Strike with your weapon and recover some armor.")
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
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            if basic_attack_roll(c,t):
                damage = c.get_base_damage()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} strikes {t.name} for {dam} {damage.type} damage!")
                t.take_damage(dam)
                diff = c.gain_armor(c.stat('dexterity'))
                messenger.add(f"{c.name} recovers {diff} armor.")
        a.set_effect(effect)
        return a
    def challenge(self, duration, strength):
        a = Ability("Challenge", cooldown=4, cost=1)
        a.set_description("Challenge the target, incentivizing them to attack you while dealing bonus damage to them.")
        def effect(c: Creature, t: Creature, _):
            t.add_effect(ChallengedEffect(duration, strength, c))
        a.set_effect(effect)
        return a

    # Elementalist
    def rainstorm(self):
        a = Ability("Rainstorm", cooldown=3, cost=2)
        a.set_description("Call upon a torrent of rain, reducing armor of all enemies and making them Wet.")
        def can_target(c: Creature, o: Creature):
            return o == c
        a.set_can_target(can_target)
        def effect(c: Creature, t: Creature, area: Area):
            messenger.add(f"{c.name} calls down a torrent of rain.")
            at_least_one = False
            for e in area.get_encounter().enemies:
                if e.is_alive() and attack_roll(c) > e.stat('endurance') * 5:
                    at_least_one = True
                    e.add_effect(WetEffect(2, c.stat('intelligence') - 2, 20))
            if not at_least_one:
                messenger.add("Everyone resists.")
        a.set_effect(effect)
        return a
    def lightning_strike(self, base_damage, base_effect_chance, **scaling):
        a = Ability("Lightning Strike", cooldown=3, cost=2)
        a.set_description("Strike your target with lightning, shocking them. If the target is wet, they cannot dodge this attack and are stunned instead.")
        a.set_target_priority(default_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            if basic_attack_roll(c,t):
                damage = base_damage.clone()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                base_dam = damage.roll_damage()
                if t.has_effect("Wet"):
                    dam = base_dam + c.level * 2
                    messenger.add(f"{c.name} blasts {t.name} for {dam} ({base_dam} + {c.level * 2}) Air damage!")
                    t.take_damage(dam)
                    success = True
                else:
                    messenger.add(f"{c.name} blasts {t.name} for {base_dam} Air damage!")
                    t.take_damage(base_dam)
                    roll = random() * 100
                    success = roll < base_effect_chance - t.stat('endurance') * 5
                if t.is_alive():
                    if success:
                        t.add_effect(ShockEffect(1))
                    else:
                        messenger.add(f"{t.name} shrugs off the shock.")
        a.set_effect(effect)
        return a

    # Luminarch
    def rallying_cry(self):
        a = Ability("Rallying Cry", cooldown=4, cost=2)
        a.set_description("Rally your companions, bolstering each party member.")
        def can_target(c: Creature, o: Creature):
            return o == c
        a.set_can_target(can_target)
        def effect(c: Creature, t: Creature, a: Area):
            # For now, just assume only a party member will ever use this
            strength = int((c.level + 1) / 2)
            armor = c.stat('wisdom')
            for p in a.player.party:
                if p.is_alive():
                    p.add_effect(BolsteredEffect(3, strength, armor))
        a.set_effect(effect)
        return a
    def enchant_weapon(self):
        a = Ability("Enchant Weapon", cooldown=4, cost=1)
        a.set_description("Enchant your weapon with holy light, causing your attacks to deal bonus damage based on your Wisdom.")
        def can_target(c: Creature, o: Creature):
            return o == c
        a.set_can_target(can_target)
        def effect(c: Creature, t: Creature, _):
            # We will need to fix this when we change ability scaling
            # For now, just increase strength by wisdom
            t.add_effect(EnchantedWeaponEffect(2, c.stat('wisdom')))
        a.set_effect(effect)
        return a

    # Soulwarden
    def drain_life(self, base_hit_chance, base_damage, **scaling):
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
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            success = attack_roll(c) > (100-base_hit_chance) + t.stat('will') * 5
            if success:
                damage = base_damage.clone()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} casts Drain Life.")
                messenger.add(f"{t.name} takes {dam} {damage.type} damage!")
                messenger.add(f"{c.name} restores {c.stat('intelligence')} armor.")
                t.take_damage(dam)
                c.gain_armor(c.stat('intelligence'))
            else:
                messenger.add(f"{c.name} casts Drain Life. {t.name} resists.")
        a.set_effect(effect)
        return a
    def corpse_explosion(self, base_damage, **scaling):
        a = Ability("Corpse Explosion", cooldown=4, cost=3)
        a.set_description("Explode target inert corpse, dealing Dark damage to each enemy.")
        def can_target(c: Creature, o: Creature):
            return not o.is_alive() and o.has_corpse
        a.set_can_target(can_target)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, area: Area):
            messenger.add(f"{c.name} gestures and the corpse of {t.name} explodes!")
            t.has_corpse = False
            multiplier = 1
            at_least_one = False
            for e in area.get_encounter().enemies:
                if (not e.is_alive()) and e.has_corpse:
                    multiplier += 1
            for c in area.player.party:
                if (not c.is_alive()) and c.has_corpse:
                    multiplier += 1
            for e in area.get_encounter().enemies:
                if e.is_alive() and attack_roll(c) > e.stat('endurance') * 5:
                    at_least_one = True
                    damage = base_damage.clone()
                    damage = a.scale_damage(damage, c)
                    damage.apply_multiplier(multiplier)
                    damage = c.calculate_total_damage(t, damage)
                    dam = damage.roll_damage()

                    messenger.add(f"{e.name} takes {dam} {damage.type} damage!")
                    e.take_damage(dam)
            if not at_least_one:
                messenger.add("The explosion failed to hit anything...")
        a.set_effect(effect)
        return a
    def curse_of_decay(self, base_damage, **scaling):
        a = Ability("Curse of Decay", cooldown=4, cost=1)
        a.set_description("Target creature gains the Decaying status, reducing their resistance every turn.")
        a.set_target_priority(default_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            success = attack_roll(c) > t.stat('endurance') * 5
            if success:
                messenger.add(f"{c.name} casts Curse of Decay.")
                damage = base_damage.clone()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{t.name} takes {dam} {damage.type} damage!")
                t.take_damage(dam)
                t.add_effect(effects.create_decaying_effect(4, c.stat('intelligence') * 3))
            else:
                messenger.add(f"{c.name} casts Curse of Decay. {t.name} resists.")
        a.set_effect(effect)
        return a

    # Ashen Stalker
    def blinding_smoke(self, base_accuracy):
        a = Ability("Blinding Smoke", cooldown=3, cost=1)
        a.set_description("Conjure a cloud of blinding smoke, reducing the targets accuracy for a turn.")
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, _):
            success = attack_roll(c, base_accuracy) > t.stat('dodge') * 5
            if success:
                messenger.add(f"{c.name} conjurs a cloud of Blinding Smoke. {t.name} takes 1 physical damage.")
                t.take_damage(1, 'physical')
                t.add_effect(effects.create_blinded_effect(1, 60))
            else:
                messenger.add(f"{c.name} conjurs a cloud of Blinding Smoke but {t.name} dodges it.")
        a.set_effect(effect)
        return a
    def flickering_flames(self, base_hit_chance):
        a = Ability("Flickering Flames", cooldown=3)
        a.set_description("Attempt to light an enemy on fire.")
        a.set_target_priority(default_offensive_priority)
        def effect(c: Creature, t: Creature, _):
            success = attack_roll(c) > (100-base_hit_chance) + t.stat('dodge') * 5 - c.stat('intelligence') * 5
            if success:
                messenger.add(f"{c.name} casts Flickering Flames.")
                t.add_effect(effects.create_burning_effect(c.stat('intelligence'), 2 + c.stat('intelligence')))
            else:
                messenger.add(f"{c.name} throws flame at {t.name} but misses.")
        a.set_effect(effect)
        return a

    # Lanternbearer
    def pale_light(self):
        a = Ability("Pale Light", cooldown=3, cost=2)
        a.set_description("Wave the Pale Lantern, providing armor and strength to a target.")
        a.set_target_priority(default_bolstered_priority)
        def effect(c: Creature, t: Creature, _):
            messenger.add(f"{c.name} waves their :BLUEVIOLET:Pale Lantern:BLUEVIOLET:.")
            t.add_effect(effects.create_bolstered_effect(3, c.stat('intelligence'), c.stat('intelligence') + 2))
        a.set_effect(effect)
        return a

    # Rotten Stray
    def rabid_bite(self, **scaling):
        a = Ability("Rabid Bite", cooldown=2, cost=2)
        a.set_description("A quick attack with a chance to bleed the target.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            out = high_offensive_priority(a,c,p,e)
            for prio in out:
                if prio.target.has_effect('Bleeding'):
                    prio.priority -= 1
            return out
        a.set_target_priority(priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            success = attack_roll(c) > t.stat('dodge') * 5
            if success:
                damage = c.get_base_damage()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} bites the {t.name} for {dam} {damage.type} damage.")
                t.take_damage(dam)
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
    def astral_lightning(self, base_damage, **scaling):
        a = Ability("Astral Lightning", cooldown=2, cost=3)
        a.set_description("Astral lightning jumps from your target to several others.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            return [ Priority(a, c, 4) ]
        a.set_target_priority(priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, area: Area):
            messenger.add(f"{c.name} conjurs :CYAN:Astral Lightning:CYAN:.")
            at_least_one_hit = False
            for target in area.player.party:
                if target.is_alive():
                    success = attack_roll(c) > target.stat('dodge') * 5
                    if success:
                        at_least_one_hit = True
                        damage = base_damage.clone()
                        damage = a.scale_damage(damage, c)
                        damage = c.calculate_total_damage(t, damage)
                        dam = damage.roll_damage()
                        messenger.add(f"{target.name} is struck for {dam} {damage.type} damage.")
                        target.take_damage(dam)
                if not at_least_one_hit:
                    messenger.add("The lightning arcs wildly, missing all of you.")
        a.set_effect(effect)
        return a
    def runic_chains(self, **scaling):
        a = Ability("Runic Chains", cooldown=3)
        a.set_description("Lash out with your chains, binding your target.")
        a.set_target_priority(high_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            success = attack_roll(c) > t.stat('dodge') * 5
            if success:
                damage = c.get_base_damage()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} lashes out with :CYAN:Runic Chains:CYAN: at {t.name} for {dam} {damage.type} damage!")
                t.take_damage(dam)
                if t.is_alive():
                    t.add_effect(StunEffect(1))
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
                return [ Priority(a, c, 3) ]
            return [ Priority(a, c, 1) ]
        a.set_target_priority(priority)
        def effect(c: Creature,*_):
            c.add_effect(effects.create_armor_effect(3, strength))
        a.set_effect(effect)
        return a

    # Gravebound Watcher
    def hollow_gaze(self, base_damage, resist_drain, **scaling):
        a = Ability("Hollow Gaze", cooldown=3)
        a.set_description("Gaze at a target, dealing dark damage and reducing their dark resistance.")
        a.set_target_priority(high_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            success = attack_roll(c) > t.stat('will') * 5
            if success:
                damage = base_damage.clone()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} gazes at {t.name}, draining their lifeforce for {dam} {damage.type} damage.")
                t.take_damage(dam)
                if t.is_alive():
                    t.add_effect(effects.create_drained_effect(3, resist_drain))
            else:
                messenger.add(f"{c.name} gazes at {t.name} but {t.name} resists")
        a.set_effect(effect)
        return a
    def necrotic_chains(self, base_damage, stun_chance, **scaling):
        a = Ability("Necrotic Chains", cooldown=3)
        a.set_description("Wrap the target in Necrotic Chains, dealing dark damage and stunning them.")
        a.set_target_priority(high_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            success = attack_roll(c) > t.stat('dodge') * 5
            if success:
                damage = base_damage.clone()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{c.name} lashes out with :BLUEVIOLET:Necrotic Chains:BLUEVIOLET: at {t.name} for {dam} {damage.type} damage!")
                t.take_damage(dam)
                if t.is_alive():
                    if random() * 100 < stun_chance:
                        t.add_effect(StunEffect(1))
                    else:
                        messenger.add(f"{t.name} resists the chains effects.")
            else:
                messenger.add(f"{c.name} lashes out with :BLUEVIOLET:Necrotic Chains:BLUEVIOLET: but misses {t.name}")
        a.set_effect(effect)
        return a

    # Unhallowed Guardian
    def greataxe_slash(self, **scaling):
        a = Ability("Greataxe Slash", cooldown=2)
        a.set_description("Swing a heavy greataxe blow, dealing damage to each enemy.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            return [ Priority(a, c, 3) ]
        a.set_target_priority(priority)
        a.set_scaling(scaling)
        def effect(c: Creature, _, area: Area):
            at_least_one = False
            messenger.add(f"The {c.name} swings their unholy greataxe in a wide arc.")
            for t in area.player.party:
                if t.is_alive():
                    success = attack_roll(c) > t.stat('dodge') * 5
                    if success:
                        at_least_one = True
                        damage = c.get_base_damage()
                        damage = a.scale_damage(damage, c)
                        damage = c.calculate_total_damage(t, damage)
                        dam = damage.roll_damage()
                        messenger.add(f"{t.name} is hit for {dam} {damage.type} damage!")
                        t.take_damage(dam)
            if not at_least_one:
                messenger.add("The greataxe slash misses everyone...")
        a.set_effect(effect)
        return a
    def soul_drain(self, base_damage, bonus_armor, **scaling):
        a = Ability("Soul Drain", cooldown=4, cost=3)
        a.set_description("Call upon unholy energies to drain the souls of your enemies, replenishing yourself.")
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            if c.armor < c.max_armor() / 0.6:
                return [ Priority(a, c, 4) ]
            return [ Priority(a, c, 2) ]
        a.set_target_priority(priority)
        a.set_scaling(scaling)
        def effect(c: Creature, _, area: Area):
            at_least_one = False
            messenger.add(f"The {c.name} calls upon unholy energies.")
            armor = c.stat('intelligence')
            for t in area.player.party:
                if t.is_alive():
                    success = random() * 85 > t.stat('will') * 5
                    if success:
                        at_least_one = True
                        armor += bonus_armor
                        damage = base_damage.clone()
                        damage = a.scale_damage(damage, c)
                        damage = c.calculate_total_damage(t, damage)
                        dam = damage.roll_damage()
                        messenger.add(f"{t.name} is drained for {dam} {damage.type} damage.")
                        t.take_damage(dam)
            if at_least_one:
                messenger.add(f"The {c.name} recovers {armor} armor.")
                c.gain_armor(armor)
            else:
                messenger.add("Everybody resists...")
        a.set_effect(effect)
        return a

    # Soul-Tethered Herald
    def dark_tether(self, base_damage, **scaling):
        a = Ability("Dark Tether", cooldown=3)
        a.set_description("Tether the target's soul, dealing dark damage and stunning them.")
        a.set_target_priority(high_offensive_priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, _):
            messenger.add(f"{c.name} casts :BLUEVIOLET:Soul Tether:BLUEVIOLET: on {t.name}.")
            success = attack_roll(c) > t.stat('will') * 5
            if success:
                damage = base_damage.clone()
                damage = a.scale_damage(damage, c)
                damage = c.calculate_total_damage(t, damage)
                dam = damage.roll_damage()
                messenger.add(f"{t.name} takes {dam} {damage.type} damage!")
                t.take_damage(dam)
                if t.is_alive():
                    t.add_effect(StunEffect(1))
                    t.action_points -= 2
            else:
                messenger.add(f"{t.name} resists.")
        a.set_effect(effect)
        return a
    def necrotic_wave(self, base_damage, resist_drain, **scaling):
        a = Ability("Necrotic Wave", cooldown=4, cost=3)
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            count = len([alive for alive in p.party if alive.is_alive()])
            if count > 1:
                return [ Priority(a, c, 4) ]
            return [ Priority(a, c, 2) ]
        a.set_target_priority(priority)
        a.set_scaling(scaling)
        def effect(c: Creature, t: Creature, area: Area):
            messenger.add(f"{c.name} unleashes a wave of :BLUEVIOLET:Necrotic Energy:BLUEVIOLET:.")
            at_least_one = False
            for t in area.player.party:
                if t.is_alive():
                    success = attack_roll(c) > t.stat('will') * 5
                    if success:
                        at_least_one = True
                        damage = base_damage.clone()
                        damage = a.scale_damage(damage, c)
                        damage = c.calculate_total_damage(t, damage)
                        dam = damage.roll_damage()
                        messenger.add(f"{t.name} takes {dam} {damage.type} damage!")
                        t.take_damage(dam)
                        if t.is_alive():
                            t.add_effect(effects.create_drained_effect(3, resist_drain))
            if not at_least_one:
                messenger.add("Everybody resists...")
        a.set_effect(effect)
        return a
    def unholy_summons(self):
        a = Ability("Unholy Summons", cooldown=3, cost=4)
        def priority(a: Ability, c: Creature, p: Player, e: Encounter):
            if len(e.enemies) >= 4:
                return []
            return [ Priority(a, c, 6) ]
        a.set_target_priority(priority)
        def effect(c: Creature, t: Creature, a: Area):
            from creature.creature_factory import get_creature_factory
            creature_factory = get_creature_factory()
            messenger.add(f"{c.name} calls upon dread forces.")
            i = randint(0,2)
            if i == 0:
                s = creature_factory.new_bone_servitor()
            else:
                i = randint(0,2)
                if i == 0:
                    s = creature_factory.new_bound_remnant_sword()
                elif i == 1:
                    s = creature_factory.new_bound_remnant_hammer()
                else:
                    s = creature_factory.new_bound_remnant_axe()
            messenger.add(f"A :BLUEVIOLET:{s.name}:BLUEVIOLET: awakens.")
            a.get_encounter().add_enemies(s)
            c.add_effect(effects.create_armor_effect(4, 8))
        a.set_effect(effect)
        return a
