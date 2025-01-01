### Terminal Hero (name to be revised)
Simple text-based RPG. Written in Python using the Pygame library.

Game design document can be found in [design](design/Act%20I/)

Running the main game 
```
>>> ./game.py -h
usage: game.py [-h] [-v] [-d] [-a]

options:
  -h, --help     show this help message and exit
  -v, --verbose  log debug and info statements
  -d, --dialog   test dialog
  -c, --companion  test a companion in the player party
  -a, --all        enable all player_log fields
```

Helper script included for visualizing dialog trees:
```
>>> dialog/dialog_display.py -h
usage: dialog_display.py [-h] filename

positional arguments:
  filename

options:
  -h, --help  show this help message and exit
```

![World.png](resources/screenshots/world.png)
![Dialogue.png](resources/screenshots/dialogue.png)

- Using a modified version of Urizen 1Bit Tileset: https://vurmux.itch.io/urizen-onebit-tileset
- Using a modified version of Kenney 1-Big Pack: https://kenney-assets.itch.io/1-bit-pack
- Using ChatGPT for placeholder dialogue and for fleshing out the game design documents.
- Using [mermaid.js](https://mermaid.js.org/) to visualize dialog trees using the script found in [dialog/dialog_display.py](dialog/dialog_display.py)

### Rough To-Do List
- Player can add characters to their party through dialogue
- Creature combat abilities
- Status effects on creatures
- Combat space (?) effects (fire, pools of water, poison gas, etc)
    - Eventually these effects should interact (poison gas explodes when encountering fire)
- Somehow mark dialogue options that have not been chosen yet
    - Mark the NPC if they have unread dialogue
    - Arrow-key control for dialogue options
