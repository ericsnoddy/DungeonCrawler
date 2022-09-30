# std lib
import sys

# import
import pygame as pg
from pygame.locals import *

from constants import WIDTH, HEIGHT

pg.init()

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Dungeon Crawler')

# game loop
running = True
while running:

    # event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
sys.exit()