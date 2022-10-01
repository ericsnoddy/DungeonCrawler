# std lib
import sys
from os.path import join

# 3rd party
import pygame as pg
from pygame.locals import *

# local
from constants import WIDTH, HEIGHT, FPS, SCALE, SPEED, BG
from character import Character



# init display
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Dungeon Crawler')

clock = pg.time.Clock()

### helper functions
# scale
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pg.transform.scale(image, (w * scale, h * scale))

# load frames
animation_list = []
for i in range(4):
    img = pg.image.load(join('assets', 'images', 'characters', 'elf', 'idle', f'{i}.png')).convert_alpha()
    img = scale_img(img, SCALE)
    animation_list.append(img)

player = Character(100, 100, animation_list)

# player control vars
moving_l = False
moving_r = False
moving_u = False
moving_d = False



# game loop
running = True
while running:
    
    # control the framerate
    clock.tick(FPS)

    # bg
    WIN.fill(BG)



    # calculate player movement
    dx = 0
    dy = 0

    if moving_r:
        dx = SPEED
    if moving_l:
        dx = -SPEED
    if moving_d:
        dy = SPEED
    if moving_u:
        dy = -SPEED
    
    # update player
    player.update()

    # draw player on screen
    player.draw(WIN)



    # event loop
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        # input handler
        if event.type == KEYDOWN:

            if event.key == pg.K_a:
                moving_l = True
            if event.key == pg.K_d:
                moving_r = True
            if event.key == pg.K_w:
                moving_u = True
            if event.key == pg.K_s:
                moving_d = True

        if event.type == KEYUP:

            if event.key == pg.K_a:
                moving_l = False
            if event.key == pg.K_d:
                moving_r = False
            if event.key == pg.K_w:
                moving_u = False
            if event.key == pg.K_s:
                moving_d = False

            
    # move the player
    player.move(dx, dy)

    # update the screen
    pg.display.update()

pg.quit()
sys.exit()