import pygame as pg

from items import Item
from character import Character
from constants import TILESIZE, ELF_HEALTH

class World:
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.enemies = []

    def process_data(self, data, tile_list, item_images, mob_animations):
        self.level_length = len(data)
        coin_images = item_images[0]
        red_potion_image = item_images[1]

        # iter values in level data
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_x = x * TILESIZE
                image_y = y * TILESIZE
                image_rect = image.get_rect(center = (image_x, image_y))
                tile_data = [image, image_rect, image_x, image_y]

                if tile == 7:
                    self.obstacle_tiles.append(tile_data)
                elif tile == 8:
                    self.exit_tile = tile_data
                elif tile == 9:
                    self.item_list.append(Item(image_x, image_y, 0, coin_images))
                    # replace item with corresponding floor tile
                elif tile == 10:
                    self.item_list.append(Item(image_x, image_y, 1, [red_potion_image]))
                    # player character
                elif tile == 11:
                    self.player = Character(image_x, image_y, ELF_HEALTH, mob_animations, 0)
                elif tile == 12:
                    self.enemies.append(Character(image_x, image_y, 100, mob_animations, 1))
                elif tile == 13:
                    self.enemies.append(Character(image_x, image_y, 100, mob_animations, 2))
                elif tile == 14:
                    self.enemies.append(Character(image_x, image_y, 100, mob_animations, 3))
                elif tile == 15:
                    self.enemies.append(Character(image_x, image_y, 100, mob_animations, 4))
                elif tile == 16:
                    self.enemies.append(Character(image_x, image_y, 100, mob_animations, 5))
                elif tile == 17:
                    self.enemies.append(Character(image_x, image_y, 100, mob_animations, 6))

                if tile >= 0:
                    # -1 means do not draw an image
                    self.map_tiles.append(tile_data)

                if tile >= 9 and tile <= 17:
                    tile_data[0] = tile_list[0]
    
    def update(self, screen_scroll):
        # camera
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surf):
        for tile in self.map_tiles:
            surf.blit(tile[0], tile[1])