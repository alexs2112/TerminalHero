#!/bin/python3

"""
A script designed to generate mermaid markdown files to visualize dialog trees
"""

import argparse
import json
import os

OUT_DIR = 'diagrams'

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    loaded_nodes = []
    for node_id, node_data in data['nodes'].items():
        node_data['id'] = node_id
        loaded_nodes.append(node_data)
    return loaded_nodes

def setup_mermaid(filename):
    out = [
        '```mermaid',
        '---',
        f'title={os.path.basename(filename)}',
        '---',
        'flowchart TB'
    ]
    return out

def write_file(filename, write_lines):
    out_file = f"{os.path.splitext(os.path.basename(filename))[0]}.mermaid.md"
    with open(os.path.join(OUT_DIR, out_file), 'w', encoding='utf-8') as f:
        for line in write_lines:
            f.write(f'{line}\n')
        f.write('```\n')
    print(f"Mermaid diagram can be found in {os.path.join(OUT_DIR, out_file)}")

if __name__==("__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    nodes = load_json(args.filename)
    lines = setup_mermaid(args.filename)

    for node in nodes:
        for child in node['children']:
            lines.append(f"\t{node['id']} --> |{child[0]}| {child[1]}")

    for node in nodes:
        lines.append(f"\t{node['id']}[{node['text']}]")
    lines.append("\tNone[Leave Dialogue]")
    lines.append('')

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    write_file(args.filename, lines)
