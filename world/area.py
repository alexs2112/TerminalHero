class Area:
    def __init__(self, name, sprite_rect, description):
        self.name = name
        self.sprite_rect = sprite_rect
        self.description = description
        self.player = None
        self.enemies = []
        self.npcs = []
