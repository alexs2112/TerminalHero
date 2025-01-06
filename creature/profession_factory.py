from creature.profession import Profession
from combat.ability_factory import get_ability_factory

abilities = get_ability_factory()

# pylint: disable=invalid-name
_profession_factory = None
def get_profession_factory():
    global _profession_factory
    if not _profession_factory:
        _profession_factory = ProfessionFactory()
    return _profession_factory

class ProfessionFactory:
    def new_enemy_profession(self, name):
        # We don't want enemy professions to add abilities and stats as those should be manually assigned
        return Profession(name)

    def new_test_wizard(self):
        p = Profession("Test Wizard")
        p.set_stats(intelligence=1, will=1)
        p.add_ability(abilities.flickering_flames(85))
        return p
