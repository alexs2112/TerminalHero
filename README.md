### Terminal Hero (name to be revised)
Simple text-based RPG. Written in Python using the Pygame library.

Game design document can be found in [design](design/Act%20I/)

![World.png](resources/screenshots/world.png)
![Dialogue.png](resources/screenshots/dialogue.png)

Using a modified version of Urizen 1Bit Tileset: https://vurmux.itch.io/urizen-onebit-tileset
Using a modified version of Kenney 1-Big Pack: https://kenney-assets.itch.io/1-bit-pack

Using ChatGPT for placeholder dialogue and for fleshing out the game design documents.

### Rough To-Do List
- Add some sort of player log that keeps track of quests and NPCs and stuff like that, it can be initialized similar to the messenger class
- Update the map so that instead of walking around, there is a list of known locations on the right that you can move around to
    - Use this player log to keep track of locations that the player knows about to gradually unlock more locations
    - Start only knowing about the village, talking to the elder will unlock more locations for the player to explore and the map will gradually grow
