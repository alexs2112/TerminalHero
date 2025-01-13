from world.feature import *
from creature.player import Player
from dialog.dialog_loader import *
from main.player_log import get_player_log
from main.notification import set_notification

player_log = get_player_log()

# pylint: disable=invalid-name
_feature_factory = None
def get_feature_factory():
    global _feature_factory
    if not _feature_factory:
        _feature_factory = FeatureFactory()
    return _feature_factory

class FeatureFactory():
    def vaelthorne_shrine(self):
        f = DialogFeature("Rune Pillar")
        f.set_dialog_function(vaelthorne_rune_pillar)
        def enabled():
            return not player_log['shrine_opened']
        f.set_enabled_function(enabled)
        return f

    def vaelthorne_crypt_entrance(self):
        f = DialogFeature("Locked Door")
        f.set_dialog_function(vaelthorne_crypt_entrance)
        def enabled():
            return not player_log['crypt_unlocked']
        f.set_enabled_function(enabled)
        return f

    def bartender_doran(self):
        f = DialogFeature("Doran the Red")
        f.set_dialog_function(doran_dialogue)
        def enabled():
            return player_log['tavern_open']
        f.set_enabled_function(enabled)
        return f

    def tavern_rest(self):
        f = FunctionFeature("Rest at the Tavern")
        def enabled():
            return player_log['tavern_room_unlocked']
        f.set_enabled_function(enabled)

        def func(player: Player, _):
            set_notification([':GREEN:Party Rested!:GREEN:',
                              'Party healed to full HP, any lingering conditions have ended.'])
            for c in player.party:
                c.temporary_stats = {}
                c.temporary_resistances = {}
                c.effects = []
                c.hp = c.max_hp()
                c.armor = c.max_armor()
        f.set_function(func)
        return f
