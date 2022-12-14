import pygame as pg

from constants import ITEM_ANIMATION_SPEED, ELF_HEALTH, POTION_STRENGTH

class Item(pg.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_coin=False):
        super().__init__()

        self.item_type = item_type  # 0: coin, 1: health potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.dummy_coin = dummy_coin

    def update(self, screen_scroll, player, coin_fx, heal_fx):

        # doesn't apply to dummy coin
        if not self.dummy_coin:

            # reposition based on screen scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]

        # check if item collected
        if self.rect.colliderect(player.rect):
            # coin collected
            if self.item_type == 0:
                player.score += 1
                coin_fx.play()
            elif self.item_type == 1:
                player.health += POTION_STRENGTH
                heal_fx.play()
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

    def draw(self, surf):
        surf.blit(self.image, self.rect)
            