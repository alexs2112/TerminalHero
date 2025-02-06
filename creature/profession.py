class Profession:
    def __init__(self, name):
        self.name = name
        self.description = "placeholder text"
        self.abilities = []
        self.stats = {}
        self.resistances = {}

    def set_description(self, description):
        self.description = description

    def add_ability(self, ability):
        self.abilities.append(ability)

    def set_stats(self, **kwargs):
        self.stats = kwargs

    def set_resistances(self, **kwargs):
        self.resistances = kwargs
