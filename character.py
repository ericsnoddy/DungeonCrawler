# 3rd party
import pygame as pg

# local
from constants import RED

class Character:
    def __init__(self, x, y, animation_list):
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = pg.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

        # animation
        self.facing_left = False
        

    def move(self, dx, dy):

        # infer image direction from movement
        if dx < 0:
            self.facing_left = True
        if dx > 0:
            self.facing_left = False

        # normalize diagonal movement
        direction_vect = pg.math.Vector2(dx, dy)
        if direction_vect.magnitude() != 0:
            pg.math.Vector2.normalize(direction_vect)

        # update the position
        self.rect.x += direction_vect[0]
        self.rect.y += direction_vect[1]

    def update(self):

        animation_cooldown = 70

        # update image
        self.image = self.animation_list[self.frame_index]

        # check if enough time has passed
        now = pg.time.get_ticks()
        if now - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
            self.update_time = now


    def draw(self, surf):

        flippped_image = pg.transform.flip(self.image, self.facing_left, False)
        surf.blit(flippped_image, self.rect)
        pg.draw.rect(surf, RED, self.rect, 1)