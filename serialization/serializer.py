import json
from serialization.save_creature import save_creature
from world.world import World
from main.player_log import get_player_log
from item.inventory import get_inventory

class Serializer:
    def __init__(self, file):
        self.file = file
        self.data = {}

    def serialize(self, world: World):
        self.data['player_log'] = get_player_log()

        self.data['player'] = save_creature(world.player)
        self.data['companions'] = {}
        for p in world.player.party:
            if p == world.player:
                continue
            self.data['companions'][p.id] = save_creature(p)

        self.data['inventory'] = []
        for i in get_inventory().items:
            self.data['inventory'].append(i.name)

        with open(self.file, 'w+', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
