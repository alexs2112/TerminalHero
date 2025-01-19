from item.item import Item

# pylint: disable=invalid-name
_inventory = None
def get_inventory():
    global _inventory
    if not _inventory:
        _inventory = InventoryHandler()
    return _inventory

class InventoryHandler:
    def __init__(self):
        self.items: list[Item] = []

    def add(self, item: Item):
        self.items.append(item)

    def remove(self, item: Item):
        self.items.remove(item)

    def is_empty(self):
        return not self.items

    def count(self):
        return len(self.items)

    def add_list(self, items: list[Item]):
        self.items += items
