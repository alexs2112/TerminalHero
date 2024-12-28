from main.constants import *
from creature.creature import Creature
from main.messenger import *

messenger = get_messenger()

class Player(Creature):
    def dies(self):
        messenger.add('You die.')
        messenger.add('Press any key to continue.')