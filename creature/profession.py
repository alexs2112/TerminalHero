class Profession:
    def __init__(self, name):
        self.name = name
        self.abilities = []
        self.stats = {}

    def add_ability(self, ability):
        self.abilities.append(ability)

    def set_stats(self, **kwargs):
        self.stats = kwargs
