from item.item import Item

class Store:
    def __init__(self, name):
        self.name = name
        self.inventory: list[Item] = []

    def add_item(self, item: Item):
        self.inventory.append(item)

    def add_items(self, items: list[Item]):
        self.inventory += items
