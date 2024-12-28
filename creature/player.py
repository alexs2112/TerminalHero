from main.constants import *
from main.messenger import *
from creature.creature import Creature

messenger = get_messenger()

class Player(Creature):
    def dies(self):
        messenger.add('You die.')
        messenger.add('Press any key to continue.')
