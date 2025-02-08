import json
from serialization.save_creature import save_creature
from world.world import World

class Serializer:
    def __init__(self, file):
        self.file = file
        self.data = {}

    def serialize(self, world: World):
        self.data['player'] = save_creature(world.player)
        self.data['companions'] = {}
        for p in world.player.party:
            if p == world.player:
                continue
            self.data['companions'][p.id] = save_creature(p)

        with open(self.file, 'w+', encoding='utf-8') as f:
            json.dump(self.data, f)
