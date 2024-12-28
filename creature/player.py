from main.constants import *
from creature.creature import Creature

import logging
logger = logging.getLogger(LOG_NAME)

class Player(Creature):
    def dies(self):
        logger.info('You die.')
        logger.info('Press any key to continue.')