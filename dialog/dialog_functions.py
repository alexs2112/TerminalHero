from main.player_log import get_player_log, update_log
from main.notification import add_notification
from world.encounter_factory import get_encounter_factory
from world.dungeon_builder import EXIT_RIGHT
from creature.creature_factory import get_creature_factory
from creature.player import Player
from quests.quest_factory import *
player_log = get_player_log()
creature_factory = get_creature_factory()
encounter_factory = get_encounter_factory()

def set_met_elder_varik(_):
    player_log['met_elder_varik'] = True

def set_initial_village(_):
    player_log['known_cemetery'] = True
    player_log['known_bloodstone_mine'] = True
    player_log['known_garrison'] = True
    player_log['known_tavern'] = True

def add_quest_grave_concerns(player: Player):
    player_log['known_cemetery'] = True
    player_log['accepted_grave_concerns'] = True
    q = grave_concerns()
    add_notification([":YELLOW:Quest Received!:YELLOW:", q.name])
    player.quests.append(q)

def set_met_gorren(_):
    player_log['met_gorren'] = True

def add_gorren_to_party_temp(player: Player):
    gorren = creature_factory.new_gorren()
    player.party.insert(0, gorren)
    update_log('finish_cemetery_stage_1')

def add_gorren_to_party(_):
    # For now, assume Gorren has already been added to the party
    update_log('gorren_leaves_church')
    update_log('known_crypt')
    add_notification([':YELLOW:Area Unlocked!:YELLOW:',
                      'Gorren shows you on your map where the :CYAN:Crypt:CYAN: is.'])

    if not player_log['tavern_open']:
        update_log('tavern_open')
        if player_log['known_tavern']:
            add_notification([':YELLOW:Area Unlocked!:YELLOW:',
                              'The :CYAN:Lifeblood Tavern:CYAN: is open for business!'])

def runebound_stalker(_):
    update_log('shrine_opened')

def unlock_vaelthorne_crypt(player: Player):
    player.area.exits.append(EXIT_RIGHT)
    player.area.locked.clear()
    update_log('crypt_unlocked')

def unlock_tavern_room(_):
    if not player_log['tavern_room_unlocked']:
        update_log('tavern_room_unlocked')
        add_notification([':YELLOW:Tavern Room Unlocked!:YELLOW:',
                          'Use your room at the tavern to heal your companions wounds and clear their conditions.'])

def unlock_tavern_store(_):
    if not player_log['tavern_store_unlocked']:
        update_log('tavern_store_unlocked')
        add_notification([':YELLOW:Tavern Store Unlocked!:YELLOW:',
                          'Purchase food at the tavern to increase your stats temporarily, until your next rest.'])

def unlock_shrine(_):
    update_log('known_shrine')
