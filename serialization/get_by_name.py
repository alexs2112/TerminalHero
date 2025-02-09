from creature.profession_factory import get_profession_factory
from item.item_factory import get_item_factory

professions = get_profession_factory()
def get_profession_by_name(name: str):
    func = getattr(professions, name.lower().replace(' ', '_'))
    return func()

items = get_item_factory()
def get_item_by_name(name: str):
    # This can be changed to item_id if needed
    new_name = name.lower()
    new_name = new_name.replace(' ', '_')
    new_name = f'new_{new_name}'
    func = getattr(items, new_name)
    return func()
