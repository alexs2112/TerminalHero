import json
from serialization.save_creature import load_creature
from serialization.get_by_name import *
from main.player_log import get_player_log
from item.inventory import get_inventory
import quests.quest_factory
from quests.quest_handler import get_quest_handler

class Deserializer:
    def __init__(self, file):
        self.file = file
        with open(self.file, encoding='utf-8') as f:
            self.data = json.load(f)

    def deserialize(self, world):
        world.player = self.load_companions()['Player']
        self.load_player_log()
        self.load_inventory()
        self.load_quests()

    def load_companions(self):
        out = {}    # Dict of (id: Creature)
        for cid, creature_data in self.data['companions'].items():
            out[cid] = load_creature(creature_data)
        out['Player'] = load_creature(self.data['player'])
        out['Player'].party = []
        for cid in self.data['player']['party']:
            out['Player'].party.append(out[cid])
        return out

    def load_player_log(self):
        log = get_player_log()
        for key, value in self.data['player_log'].items():
            log[key] = value

    def load_inventory(self):
        i = get_inventory()
        i.items.clear()
        for item_name in self.data['inventory']:
            i.add(get_item_by_name(item_name))

    def load_quests(self):
        q = get_quest_handler()
        q.quests.clear()
        q.done.clear()
        for quest_id in self.data['quests']:
            func = getattr(quests.quest_factory, quest_id)
            q.add(func())
        for quest_id in self.data['done_quests']:
            func = getattr(quests.quest_factory, quest_id)
            q.add_done(func())
