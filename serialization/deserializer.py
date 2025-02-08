import json
from serialization.save_creature import load_creature

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
