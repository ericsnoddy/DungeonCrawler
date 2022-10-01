# std lib
import math

# installed
import pygame as pg

# local
from debug import debug


class Weapon:
    def __init__(self, image):

        self.original_image = image
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()

    def update(self, player):

        self.rect.center = player.rect.center

        mouse_pos = pg.mouse.get_pos()              
        x_dist = mouse_pos[0] - self.rect.centerx
        y_dist = -(mouse_pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

    def draw(self, surf):

        surf.blit(self.image, self.rect)
        debug([
            f'{self.angle}'
        ])