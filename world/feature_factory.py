from world.feature import *
from dialog.dialog_loader import *
from main.player_log import get_player_log

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
