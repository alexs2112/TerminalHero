from world.feature import *
from world.encounter_factory import get_encounter_factory
from creature.player import Player
from dialog.dialog_loader import *
from main.player_log import get_player_log
from main.notification import add_notification
from item.store_builder import get_store_builder

player_log = get_player_log()
store_builder = get_store_builder()
encounter_factory = get_encounter_factory()

# pylint: disable=invalid-name
_feature_factory = None
def get_feature_factory():
    global _feature_factory
    if not _feature_factory:
        _feature_factory = FeatureFactory()
    return _feature_factory

class FeatureFactory():
    def elder_varik(self):
        f = DialogFeature("Speak to Elder Varik")
        f.set_dialog_function(elder_varik_dialog)
        return f

    def bartender_doran(self):
        f = DialogFeature("Speak to Doran the Red")
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
            add_notification([':GREEN:Party Rested!:GREEN:',
                              'Party healed to full HP, any lingering conditions have ended.'])
            for c in player.party:
                c.temporary_stats = {}
                c.temporary_resistances = {}
                c.effects = []
                c.hp = c.max_hp()
                c.armor = c.max_armor()
                c.food = None
        f.set_function(func)
        return f

    def tavern_food(self):
        f = FoodStoreFeature("Eat at the Tavern")
        def enabled():
            return player_log['tavern_store_unlocked']
        f.set_enabled_function(enabled)
        f.set_store(store_builder.tavern_store())
        return f

    def gorren_initial_meeting(self):
        f = DialogFeature("Speak to Gorren")
        f.set_dialog_function(gorren_initial_meeting)
        def enabled():
            if player_log['gorren_leaves_church']:
                return False
            return not player_log['finish_cemetery_stage_1'] or player_log['defeat_cemetery_church_ambush']
        f.set_enabled_function(enabled)
        return f

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

    def gorren_banishment_ritual(self):
        f = DialogFeature("Perform the Ritual")
        f.set_dialog_function(gorren_banishment_ritual)
        def enabled():
            if not player_log['banishment_ritual_can_start'] \
                or player_log['finish_cemetery_stage_3']:
                return False
            if not player_log['gorren_ritual_interrupted'] \
                or player_log['soul_tethered_herald_defeated']:
                return True
            return False
        f.set_enabled_function(enabled)
        return f

    def rangu_initial_meeting(self):
        f = DialogFeature("Speak to Rangu")
        f.set_dialog_function(rangu_initial_meeting)
        def enabled():
            return not player_log['met_rangu']
        f.set_enabled_function(enabled)
        return f
