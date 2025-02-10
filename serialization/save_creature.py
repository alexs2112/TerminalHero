from serialization.get_by_name import *
from creature.creature import Creature
from creature.player import Player
from creature.creature_sprite import CreatureSprite, ModularSprite
from combat.damage import Damage
from item.item import ITEM_SLOTS

def save_creature(creature: Creature):
    # Take the creature's attributes, then overwrite the ones that cannot be serialized
    out = creature.__dict__.copy()
    out['sprite'] = hash_creature_sprite(creature.sprite)
    out['abilities'] = [ a.name for a in creature.abilities ]
    out['profession'] = creature.profession.name        # Assume that this is not None
    out['base_damage'] = creature.base_damage.__dict__.copy()
    new_equipment = {}
    for s in ITEM_SLOTS:
        new_equipment[s] = ''
    for s, e in out['equipment'].items():
        if out['equipment'][s]:
            new_equipment[s] = e.name
    out['equipment'] = new_equipment
    out['effects'] = []     # This should always be empty anyways, could potentially break things if not
    if creature.food:
        out['food'] = creature.food.name

    if creature.type == 'player':
        out['party'] = [ p.id for p in creature.party ]
        out['area'] = creature.area.id
        if creature.room:
            out['room'] = creature.room.id
        else:
            out['room'] = None

    return out

def load_creature(creature_dict: dict):
    out = creature_dict
    if out['type'] == 'player':
        c = Player("")
    else:
        c = Creature("", -1)

    # Reset all attributes to their atomic equivalent
    for key, value in out.items():
        setattr(c, key, value)

    # Start fixing values that should not be atomic
    # ignore abilities for now, all abilities to player characters are granted via equipment and profession
    c.set_profession(get_profession_by_name(out['profession']))
    c.set_base_damage(Damage(out['base_damage']['min'], out['base_damage']['max'], out['base_damage']['type']))
    for slot, item_name in out['equipment'].items():
        if not item_name:   # empty string
            continue
        c.equipment[slot] = get_item_by_name(item_name)
    c.set_sprite(unhash_creature_sprite(out['sprite']))
    if out['food']:
        c.food = get_item_by_name(out['food'])

    # The party will need to be loaded once all characters are loaded in deserializer

    return c

def hash_creature_sprite(sprite: CreatureSprite):
    out = {
        'sprite_rect': sprite.sprite_rect,
        'dead_rect': sprite.dead_rect,
        'type': sprite.type
    }
    return out

def unhash_creature_sprite(out: dict):
    if out['type'] == 'default':
        return CreatureSprite(out['sprite_rect'], out['dead_rect'])
    else:
        return ModularSprite(out['sprite_rect'], out['dead_rect'])
