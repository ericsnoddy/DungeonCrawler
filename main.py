# std lib
import sys

# 3rd party
import pygame as pg
from pygame.locals import *

# local
from constants import WIDTH, HEIGHT
from character import Character



# init display
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Dungeon Crawler')



# create player
player = Character(100,100)



# game loop
running = True
while running:


    # draw player on screen
    player.draw(WIN)


    # event loop
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        # input handler
        if event.type == KEYDOWN:
            if event.key == pg.K_a:
                print('left')
            if event.key == pg.K_d:
                print('right')
            if event.key == pg.K_w:
                print('up')
            if event.key == pg.K_s:
                print('down')
            


    # update the screen
    pg.display.update()

pg.quit()
sys.exit()