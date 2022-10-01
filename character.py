# 3rd party
import pygame as pg

# local
from constants import RED

class Character:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pg.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):

        # normalize diagonal movement
        direction_vect = pg.math.Vector2(dx, dy)
        if direction_vect.magnitude() != 0:
            pg.math.Vector2.normalize(direction_vect)

        # update the position
        self.rect.x += direction_vect[0]
        self.rect.y += direction_vect[1]


    def draw(self, surf):
        surf.blit(self.image, self.rect)
        pg.draw.rect(surf, RED, self.rect)