import json
from serialization.save_creature import load_creature
from serialization.get_by_name import *
from main.player_log import get_player_log
from item.inventory import get_inventory
import quests.quest_factory
from quests.quest_handler import get_quest_handler
from creature.level_up_handler import get_level_up_handler

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
        self.load_level_up_handler(world.player.party)
        self.load_player_location(world, world.player)

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

    def load_level_up_handler(self, party):
        levels = get_level_up_handler()
        levels.creatures.clear()
        levels.xp = self.data['xp_tracker']

        # Instead of storing the party, just add all of them on load
        for c in party:
            levels.add_creature(c)

    # This is kind of a mess
    def load_player_location(self, world, player):
        area_id = player.area
        for a in world.get_areas():
            if a.id == area_id and a.condition_met():
                player.area = a
                a.player = player

                room_id = player.room
                if a.dungeon:
                    for r in a.dungeon.get_rooms():
                        if r.id == room_id:
                            player.room = r
                            r.player = player
                            return
                    player.room = None
                return
        player.area = None
        player.room = None

    # Callable outside of loading, get the last screen that the player was on
    # This is super ugly but works, we can clean it up when we need to
    def get_screen(self, canvas, world):
        # pylint: disable=import-outside-toplevel
        if self.data['load_screen'] == 'world':
            from screen.world_screen import WorldScreen
            return WorldScreen(canvas, world)
        elif self.data['load_screen'] == 'area':
            from screen.area_screen import AreaScreen
            from screen.world_screen import WorldScreen
            return AreaScreen(canvas, world.player.area, world.player, WorldScreen(canvas, world))
        elif self.data['load_screen'] == 'dungeon':
            from screen.dungeon_screen import DungeonScreen
            from screen.area_screen import AreaScreen
            from screen.world_screen import WorldScreen
            return DungeonScreen(canvas, world.player.area.dungeon, world.player,
                                    AreaScreen(canvas, world.player.area, world.player, WorldScreen(canvas, world)))
