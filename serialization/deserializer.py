import json
from serialization.save_creature import load_creature
from main.player_log import get_player_log

class Deserializer:
    def __init__(self, file):
        self.file = file
        with open(self.file, encoding='utf-8') as f:
            self.data = json.load(f)

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
