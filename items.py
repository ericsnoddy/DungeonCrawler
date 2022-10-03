import pygame as pg

from constants import ITEM_ANIMATION_SPEED, ELF_HEALTH, POTION_STRENGTH, COIN_VALUE

class Item(pg.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list):
        super().__init__()

        self.item_type = item_type  # 0: coin, 1: health potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player):

        # check if item collected
        if self.rect.colliderect(player.rect):
            # coin collected
            if self.item_type == 0:
                player.score += COIN_VALUE
            elif self.item_type == 1:
                player.health += POTION_STRENGTH
                if player.health > ELF_HEALTH:
                    player.health = ELF_HEALTH

            self.kill()

        animation_speed = ITEM_ANIMATION_SPEED
        self.image = self.animation_list[self.frame_index]

        now = pg.time.get_ticks()
        if now - self.update_time >= animation_speed:
            self.frame_index += 1
            self.update_time = now
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            