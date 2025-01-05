class Profession:
    def __init__(self, name):
        self.name = name
        self.abilities = []
        self.stats = {}

    def set_abilities(self, abilities):
        self.abilities = abilities

    def add_ability(self, ability):
        self.abilities.append(ability)
