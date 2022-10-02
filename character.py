# installed
import pygame as pg

# local
from constants import ANIMATION_SPEED, ELF_OFFSET, SCALE, RED

class Character:
    def __init__(self, x, y, health, mob_animations, char_type):

        self.char_type = char_type  # int corresponds to mob_types index (see main.py)
        self.animation_list = mob_animations[self.char_type]
        self.action = 0     # 0 - 'idle', 1 - 'run'        
        self.facing_left = False
        self.running = False
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pg.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

        self.health = health
        self.alive = True

    def move(self, direction_vect):

        # infer image direction from x-axis movement
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

        # check if char is alive
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # check what action the player is performing
        if self.running:
            self.update_action(1)
        else: self.update_action(0)

        animation_cooldown = ANIMATION_SPEED

        # update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed
        now = pg.time.get_ticks()
        if now - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            self.update_time = now


    def draw(self, surf):

        flipped_image = pg.transform.flip(self.image, self.facing_left, False)

        # adjust the elf sprite
        if self.char_type == 0:
            surf.blit(flipped_image, (self.rect.x, self.rect.y - ELF_OFFSET * SCALE))
        else:
            surf.blit(flipped_image, self.rect)
        pg.draw.rect(surf, RED, self.rect, 1)