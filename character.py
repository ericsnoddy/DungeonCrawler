# 3rd party
import pygame as pg

# local
from constants import RED

class Character:
    def __init__(self, x, y):
        self.rect = pg.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)


    def draw(self, surf):
        pg.draw.rect(surf, RED, self.rect)