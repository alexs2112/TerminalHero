import json, pathlib
from dialog.dialog_node import DialogNode
from dialog.dialog_roll import DialogRoll

# Format of the JSON file in resources/dialog/*.json
# {
#     "nodes": {
#         "<node_id>": {
#             "name": <name>,
#             "text": <text>,
#             "children: [
#                 ["<option_text>", "<node_name>"],
#                 ...
#             ]
#         },
#         ...
#         "<node_id>": {
#             "type": "Roll",
#             "name": <optional_name>,
#             "text": <optional_text>,
#             "value": <value_to_pass>,
#             "stat": <stat_to_roll>,
#             "success": <node_id>,
#             "failure": <node_id>,
#             ...
#         }
#     }
# }

def load_dialog(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Load each node initially as { node_id: DialogNode }
    loaded_nodes = {}
    for node_id, node_data in data['nodes'].items():
        log_id = f"{pathlib.Path(filename).stem}_{node_id}"
        if 'type' in node_data and node_data['type'] == "Roll":
            loaded_nodes[node_id] = load_roll_initial(log_id, node_data)
        else:
            loaded_nodes[node_id] = load_node_initial(log_id, node_data)

    # Second pass: Structure node children properly
    for node in loaded_nodes.values():
        if node.type == 'Dialog':
            for child in node.children:
                if child[1] == 'None':
                    child[1] = None
                else:
                    child[1] = loaded_nodes[child[1]]
                    # If the child does not have text, the text becomes the option to select it
                    if not child[1].text:
                        child[1].text = child[0]
        elif node.type == 'Roll':
            node.success = loaded_nodes[node.success]
            node.failure = loaded_nodes[node.failure]
    return loaded_nodes

def load_node_initial(log_id, node_data):
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
    only_once = False
    if 'only_once' in node_data:
        only_once = node_data['only_once']

    d = DialogNode(log_id, node_data['name'], node_data['text'], node_data['children'])
    d.set_condition(condition)
    d.set_unless(unless)
    d.set_function_name(func)
    d.set_area_option(area_option)
    d.set_stat_requirement(stat_requirement)
    d.set_only_once(only_once)
    return d

def load_roll_initial(log_id, node_data):
    name = 'System'
    if 'name' in node_data:
        name = node_data['name']
    text = ''
    if 'text' in node_data:
        text = node_data['text']

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
    only_once = False
    if 'only_once' in node_data:
        only_once = node_data['only_once']

    d = DialogRoll(log_id, name, text, node_data['value'], node_data['stat'], node_data['success'], node_data['failure'])
    d.set_condition(condition)
    d.set_unless(unless)
    d.set_function_name(func)
    d.set_area_option(area_option)
    d.set_stat_requirement(stat_requirement)
    d.set_only_once(only_once)
    return d
