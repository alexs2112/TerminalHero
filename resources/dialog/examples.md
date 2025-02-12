Valid Dialogue Trees should take the following form
```json
{
    "nodes": {
        "<node_name>": {
            "name": "<speaker_name>",
            "text": "<dialogue_text>",
            "children": [
                [ "<dialogue_option>", "<option_node_name>" ]
            ]
        }
    }
}
```

Each node can also have the following options:
```
"function": "<function_name>"
"condition": "<run_if_log_entry>"
"unless": "<run_unless_log_entry>"
"stats": { "<stat_name>": 5, "<stat_2_name>": 3, etc... }
```

Children leading to the node name of `"None"` will exit dialogue when the option is chosen

If a node has their `text` as `"None"`, when this node is chosen it will fulfill any function calls and immediately exit dialogue.

Encasing a word in colours defined in [colour.py](/main/colour.py) will colour that word.
- Example: `"Hello, my name is :RED:World:RED:`
