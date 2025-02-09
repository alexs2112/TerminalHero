from item.store import Store
from item.item_factory import get_item_factory

items = get_item_factory()

# pylint: disable=invalid-name
_store_builder = None
def get_store_builder():
    global _store_builder
    if not _store_builder:
        _store_builder = StoreBuilder()
    return _store_builder

class StoreBuilder:
    def tavern_store(self):
        s = Store("The Lifeblood Tavern")
        i = [
            items.new_plump_helmet(),
            items.new_buried_torch(),
            items.new_firecut(),
            items.new_stonecurd()
        ]
        s.add_items(i)
        return s
