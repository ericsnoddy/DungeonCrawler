# 3rd party
import pygame as pg

# local
from constants import RED

class Character:
    def __init__(self, x, y, animations):
        self.animations = animations
        self.action = 0     # 0 - 'idle', 1 - 'run'
        self.facing_left = False
        self.running = False
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.animations[self.action][self.frame_index]
        self.rect = pg.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

        # animation
        

    def move(self, direction_vect):

        # infer image direction from movement
        if direction_vect[0] < 0:
            self.facing_left = True
        if direction_vect[0] > 0:
            self.facing_left = False

        # normalize diagonal movement and infer action
        if direction_vect.magnitude() != 0:
            pg.math.Vector2.normalize(direction_vect)
            self.running = True
        else:
            self.running = False

        # update the position
        self.rect.x += direction_vect[0]
        self.rect.y += direction_vect[1]

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def update(self):

        # check what action the player is performing
        if self.running:
            self.update_action(1)
        else: self.update_action(0)

        animation_cooldown = 70

        # update image
        self.image = self.animations[self.action][self.frame_index]

        # check if enough time has passed
        now = pg.time.get_ticks()
        if now - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.action]):
                self.frame_index = 0
            self.update_time = now


    def draw(self, surf):

        flippped_image = pg.transform.flip(self.image, self.facing_left, False)
        surf.blit(flippped_image, self.rect)
        pg.draw.rect(surf, RED, self.rect, 1)