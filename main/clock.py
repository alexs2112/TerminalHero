import pygame

# pylint: disable=invalid-name
_clock = None
def get_clock():
    global _clock
    if not _clock:
        _clock = pygame.time.Clock()
    return _clock
