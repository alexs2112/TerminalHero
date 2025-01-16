### Terminal Hero (name to be revised)
Simple text-based RPG. Written in Python using the Pygame library.

Game design document can be found in [design](design/)

Running the main game 
```
>>> ./game.py -h
usage: game.py [-h] [-v] [-d] [-c] [-a] [-l LOG] [-u DUNGEON] [-r] [-e] [-s] [-i]

options:
  -h, --help            show this help message and exit
  -v, --verbose         log debug and info statements
  -d, --dialog          test dialog
  -c, --companion       test a companion in the player party
  -a, --all             enable "all" player_log fields
  -l LOG, --log LOG     comma separated list of player_log entries to start with
  -u DUNGEON, --dungeon DUNGEON
                        test dungeon display by name
  -r, --revealed        for dungeon mode, set all rooms as revealed
  -e, --no-enemies      for dungeon mode, remove all encounters
  -s, --stats           gives the player massively enhanced stats
  -i, --inventory       show the inventory test screen
```

Helper script included for visualizing dialog trees:
-  An example of this can be found in [elder_varik.mermaid.md](resources/examples/elder_varik.mermaid.md)
```
>>> dialog/dialog_display.py -h
usage: dialog_display.py [-h] filename

positional arguments:
  filename

options:
  -h, --help  show this help message and exit
```

![Combat.png](resources/screenshots/combat.png)
![World.png](resources/screenshots/world.png)
![Dialogue.png](resources/screenshots/dialogue.png)
![Quest_Screen.png](resources/screenshots/quest_screen.png)
![Creature_Screen.png](resources/screenshots/creature_screen.png)
![Dungeon.png](resources/screenshots/dungeon.png)

- Using a modified version of Urizen 1Bit Tileset: https://vurmux.itch.io/urizen-onebit-tileset
- Using a modified version of Kenney 1-Big Pack: https://kenney-assets.itch.io/1-bit-pack
- Using ChatGPT for placeholder dialogue and for fleshing out the game design documents.
- Using [mermaid.js](https://mermaid.js.org/) to visualize dialog trees using the script found in [dialog/dialog_display.py](dialog/dialog_display.py).

### Rough To-Do List (Unordered)
**Area**
- Encounters should have descriptive text that is displayed in the area screen in red

**Quest**
- Quest Steps should have NPCs and Locations, to highlight important steps for the player
- Areas should show quest options as yellow (or with an exclamation point or something)
- World Screen should highlight quest areas
- Quest Log icon at the bottom of the world screen that highlights if changes have been made to the quest log
- Quest log will probably require scrolling
- For now, get rid of main + side quests, just have "Quests" and "Complete"

**Combat**
- Get rid of the funny `qwerasdf` targeting. Instead use arrow keys and highlight targeted enemies (possibly multiples).
  - This also allows showing hit chance, damage, and status effects
  - And allows preventing illegal targeting, etc
- Flee combat? Or just reload previous save lol
- Print the correct post-resistance damage numbers in ability effects before the damage is dealt (in case they die)
- Figure out a concise way to let party members know that their allies are the players party
  - I do not remember why I wanted this
- When balancing, increase all numbers by a bit. This will allow resistances to actually be felt (10% resistance doesn't matter if the damage is like 4)
- Allow certain boss enemies act several times in a row

**Dungeons**
- Dungeons refresh enemies if the player leaves before completing them (defeating boss?)
  - Prevents pseudo save-scumming by finishing each encounter and returning to tavern to full heal before coming back
  - Not that the tavern is a thing yet lol
- Only show the big dungeon entrance notification the very first time that dungeon is entered

**World**
- Draw the world like how dungeons are drawn, instead of using tiles
- This can't just be kept as a dungeon because I still want Area Screens and you can't just walk around to explore it (ie. otherwise keep the interface the same for now)
- Each world area should have a priority or something, sort the areas in the world screen by priority rather than location

**Status Effects**
- Display status effect icon instead of name, effect screen that can be opened in combat to list all status effects off
  - Sort the list by showing currently active ones first

**Dialogue**
- Somehow mark dialogue options that have not been chosen yet
    - Mark the NPC if they have unread dialogue
    - Arrow-key control for dialogue options
- Show the sprite of the NPC you are talking to
- Instead of NPCs with dialogue, just make them DialogueFeatures?
- Coloured text should wrap properly

**Items**
- Magic weapons buff damage of a particular type?
- Get rid of key items? I feel like these as a separate list arent useful, just flag them and border them in blue or something in the inventory screen
- Implement currency and limited product at stores, do we want stores to reset every so often?
  - Maybe they just get new items when certain player_log entries are set
- Rare food from special merchants?

**Screens**
- A screen to store known lore ([J]ournal?)
  - Include a section for known food
- Creature screen rapidly overflows with abilities, add new ability screen that can be accessed from creature screen (or straight from combat)
- Party Screen to view party members
  - Show max of each stat for dialogue skill checks
- Character screen to view self, [tab] to swap to next character in party
- Lots of overlap between StoreScreen and InventoryScreen, should be condensed

**Creatures**:
- Get secondary stats and resistances correctly to account for base (str,dex,int) stats
  - ie. getting a creature's fire resistance should include the benefit from having high int

**Saving**
- This is going to be a bit of an issue

**Other**
- Set Item as superclass of new Equipment and Food classes
- New constant of `FONT_HEIGHT + 2`
- Mouse controls
- If you have unlocked all 6 companions, you unlock a bonus area of a pond with a magic frog.
  - The frog says random sentences at you in dialogue that sound very wise but are either nonsense or unrelated.
