import json
from dialog.dialog_node import DialogNode

# Format of the JSON file in resources/dialog/*.json
# {
#     "nodes": {
#         "<node_name>": {
#             "name": <name>,
#             "text": <text>,
#             "children: [
#                 ["<option_text>", "<node_name>"],
#                 ...
#             ]
#         },
#         ...
#     }
# }

def load_dialog(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Load each node initially
    loaded_nodes = {}
    for node_id, node_data in data['nodes'].items():
        loaded_nodes[node_id] = load_node_initial(node_data)

    # Second pass: Structure node children properly
    for node in loaded_nodes.values():
        for child in node.children:
            if child[1] == "None":
                child[1] = None
            else:
                child[1] = loaded_nodes[child[1]]
    return loaded_nodes

def load_node_initial(node_data):
    condition = None
    if 'condition' in node_data:
        condition = node_data['condition']
    unless = None
    if 'unless' in node_data:
        unless = node_data['unless']
    func = None
    if 'function' in node_data:
        func = node_data['function']
    area_option = None
    if 'option' in node_data:
        area_option = node_data['option']
    stat_requirement = None
    if 'stats' in node_data:
        stat_requirement = node_data['stats']

    d = DialogNode(node_data['name'], node_data['text'], node_data['children'])
    d.set_condition(condition)
    d.set_unless(unless)
    d.set_function_name(func)
    d.set_area_option(area_option)
    d.set_stat_requirement(stat_requirement)
    return d
