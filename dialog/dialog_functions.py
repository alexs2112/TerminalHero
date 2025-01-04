from main.player_log import get_player_log
from main.notification import set_notification
from creature.player import Player
from world.encounter_factory import EncounterFactory
from quests.quest_factory import *
player_log = get_player_log()

def set_met_elder_varik(_):
    player_log['met_elder_varik'] = True

def set_known_cemetery(_):
    player_log['known_cemetery'] = True

def set_known_bloodstone_mine(_):
    player_log['known_bloodstone_mine'] = True

def set_known_starvation_pit(_):
    player_log['known_starvation_pit'] = True

def set_known_garrison(_):
    player_log['known_garrison'] = True

def add_quest_visit_corpse_pile(player: Player):
    player_log['accepted_sidequest_1'] = True
    q = investigate_corpse_pile()
    set_notification(["Quest Received!", q.name])
    player.side_quests.append(q)

def set_met_gorren(_):
    player_log['met_gorren'] = True

def add_corpse_pile_encounter_2(player: Player):
    # I hate having a factory here, but I can't think of a better way ATM
    player.area.encounters.append(EncounterFactory().get_cemetery_encounter_2())

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
