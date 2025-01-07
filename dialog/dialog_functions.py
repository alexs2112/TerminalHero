from main.player_log import get_player_log
from main.notification import set_notification
from world.encounter_factory import get_encounter_factory
from creature.player import Player
from quests.quest_factory import *
player_log = get_player_log()
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
    set_notification(["Quest Received!", q.name])
    player.side_quests.append(q)

def set_met_gorren(_):
    player_log['met_gorren'] = True

def add_corpse_pile_encounter_2(player: Player):
    # I hate having a factory here, but I can't think of a better way ATM
    player.area.encounters.append(encounter_factory.get_cemetery_encounter_2())

    # Assume there is only Gorren in the area
    gorren = player.area.npcs[0]
    player.party.append(gorren)

def add_gorren_to_party(player: Player):
    # At this point, assume that the only NPC in the area is Gorren
    if len(player.party) < 2:
        player.party = [player, player.area.npcs[0]]
    player.area.npcs.clear()

def reject_gorren(player: Player):
    player.party = [player]
