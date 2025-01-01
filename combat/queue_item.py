from creature.creature import Creature

class QueueItem:
    def __init__(self, item_type: str):
        self.item_type: str = item_type

    def is_type(self, item_type: str):
        return self.item_type == item_type

    def get_type(self):
        return self.item_type

class QueueCreature(QueueItem):
    def __init__(self, creature: Creature):
        super().__init__('creature')
        self.creature = creature

class QueueWait(QueueItem):
    def __init__(self, milliseconds: int):
        super().__init__('wait')
        self.time = milliseconds
