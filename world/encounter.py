from creature.creature import Creature
from creature.level_up_handler import get_level_up_handler
from item.item import Item
from item.inventory import get_inventory
from main.player_log import get_player_log
from main.notification import add_notification

player_log = get_player_log()
level_up_handler = get_level_up_handler()
inventory = get_inventory()

class Encounter:
    def __init__(self, name):
        self.name: str = name
        self.enemies: list[Creature] = []
        self.completed: bool = False

        self.reward_xp: int = 0
        self.reward_gold: int = 0
        self.reward_items: list[Item] = []

        # Condition in player_log that makes this encounter appear in an area
        self.valid_condition: str = None

        # Condition in player_log that makes this encounter disappear in an area
        self.invalid_condition: str = None

        # Function that is called when the encounter is completed
        self.completed_function = None

        # If True, the player cannot leave the current area until this encounter is dealt with
        self.block_exit: bool = False

    def enabled(self):
        if self.completed:
            return False
        if self.invalid_condition in player_log:
            if player_log[self.invalid_condition]:
                return False
        if self.valid_condition in player_log:
            return player_log[self.valid_condition]
        return True

    def set_completed_function(self, func):
        self.completed_function = func

    def complete(self, player, area):
        self.completed = True
        reward_strings = [':YELLOW:Rewards::YELLOW:']
        if self.reward_xp:
            reward_strings.append(f':CYAN:EXP::CYAN: {self.reward_xp}')
        if self.reward_gold:
            reward_strings.append(f':ORANGE:Gold::ORANGE: {self.reward_gold}')
            # Add gold to player
        for i in self.reward_items:
            inventory.add(i)
            reward_strings.append(i.name)
        add_notification(reward_strings)
        if self.reward_xp:
            # Do this afterwards, so that the level up notification doesn't come before the rewards
            level_up_handler.add_xp(self.reward_xp)
        if self.completed_function:
            self.completed_function(player, area)

    def add_enemies(self, *enemies):
        for e in enemies:
            e.refresh()
            self.enemies.append(e)
        for e in self.enemies:
            e.allies = self.enemies
