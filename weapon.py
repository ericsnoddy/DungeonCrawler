# std lib
import math
from random import randint

# installed
import pygame as pg

# local
from constants import WIDTH, HEIGHT, BOW_COOLDOWN, ARROW_SPEED
from debug import debug


class Weapon:
    def __init__(self, image, arrow_image):

        self.original_image = image
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_fired = pg.time.get_ticks()

    def update(self, player):
        
        shot_cooldown = BOW_COOLDOWN
        self.rect.center = player.rect.center

        mouse_pos = pg.mouse.get_pos()              
        x_dist = mouse_pos[0] - self.rect.centerx
        y_dist = -(mouse_pos[1] - self.rect.centery)   # neg b/c pygame reverses y-axis
        # calc the angle in degrees where E:0, N: 90, W: 180, S: -90
        # using the arc-tangent of the distance y/x method
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # shooting
        arrow = None
        now = pg.time.get_ticks()
        if pg.mouse.get_pressed()[0] and not self.fired and (now - self.last_fired >= shot_cooldown):
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_fired = now

        if not pg.mouse.get_pressed()[0]:
            self.fired = False

        return arrow

    def draw(self, surf):

        self.image = pg.transform.rotate(self.original_image, self.angle)
        x_adjust = self.rect.centerx - self.image.get_width()//2
        y_adjust = self.rect.centery - self.image.get_height()//2
        surf.blit(self.image, (x_adjust, y_adjust))

        # debug([
        #     f'{self.angle}'
        # ])

class Arrow(pg.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        super().__init__()

        self.original_image = image
        self.angle = angle # sprite orientation reqs adjustment by 90 deg
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center = (x,y))
        # calc hor and vert speeds based on angle (neg b/c pygame reverses y-axis)
        self.dx = math.cos(math.radians(self.angle)) * ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * ARROW_SPEED)

    def update(self, enemy_list):

        # reset variable
        damage = 0
        damage_pos = None

        # reposition based on speed
        self.rect.x += self.dx
        self.rect.y += self.dy

        # check if offscreen
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

        # check collision with enemies
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill() # remove arrow
                break   # one enemy per arrow
        
        return damage, damage_pos

    def draw(self, surf):

        x_adjust = self.rect.centerx - self.image.get_width()//2
        y_adjust = self.rect.centery - self.image.get_height()//2
        surf.blit(self.image, (x_adjust, y_adjust))