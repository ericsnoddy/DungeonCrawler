# std lib
import sys
from os.path import join
from numpy import str0

# installed
import pygame as pg
from pygame.locals import *

# local
from constants import WIDTH, HEIGHT, FPS, SCALE, WEAP_SCALE, SPEED, BG, RED
from character import Character
from weapon import Weapon



# init display
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Diamblo')

clock = pg.time.Clock()

### helper functions
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pg.transform.scale(image, (w * scale, h * scale))

# load weapon images
bow_image = scale_img(pg.image.load(join('assets', 'images', 'weapons', 'bow.png')).convert_alpha(), WEAP_SCALE)
arrow_image = pg.image.load(join('assets', 'images', 'weapons', 'arrow.png')).convert_alpha()
# fireball_image = pg.image.load(join('assets', 'images', 'weapons', 'fireball.png')).convert_alpha()

# build nested animations list by character, action, and frame_index
mob_animations = []
mob_types = ['elf', 'imp', 'skeleton', 'goblin', 'muddy', 'tiny_zombie', 'big_demon']
animation_types = ['idle', 'run']
for mob_type in mob_types:    
    animation_list = []
    for animation_type in animation_types:
        temp_list = []    
        for i in range(4):

            img = pg.image.load(join('assets', 'images', 'characters', f'{mob_type}', f'{animation_type}', f'{i}.png')).convert_alpha()
            img = scale_img(img, SCALE)

            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# define font
font = pg.font.Font(join('assets', 'fonts', 'AtariClassic.ttf'), 20)

# displaying damage
class DamageText(pg.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        super().__init__()
        self.image = font.render(str(damage), True, color)
        self.rect= self.image.get_rect(center=(x,y))

# player control vars
moving_l = False
moving_r = False
moving_u = False
moving_d = False


# create player
player = Character(100, 100, 100, mob_animations, 0)

# create weapon
bow = Weapon(bow_image, arrow_image)

# create sprite groups
damage_text_group = pg.sprite.Group()
arrow_group = pg.sprite.Group()

# create enemy
enemy = Character(200, 300, 100, mob_animations, 1)
enemy_list = []
enemy_list.append(enemy)

# game loop
running = True
while running:
    
    # control the framerate
    clock.tick(FPS)

    # bg
    WIN.fill(BG)

    # player movement
    direction_vect = pg.math.Vector2(0,0)

    if moving_r:
        direction_vect[0] = SPEED
    if moving_l:
        direction_vect[0] = -SPEED
    if moving_d:
        direction_vect[1] = SPEED
    if moving_u:
        direction_vect[1] = -SPEED
    
    # move the player
    player.move(direction_vect)

    # update player
    player.update()

    # update the enemies
    for enemy in enemy_list:
        enemy.update()

    # update bow and arrow
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group.sprites():
        arrow.update(enemy_list)
    damage_text_group.update()
    
    player.draw(WIN)
    bow.draw(WIN)
    for arrow in arrow_group.sprites():
        arrow.draw(WIN)
    for enemy in enemy_list:
        enemy.draw(WIN)
    damage_text_group.draw(WIN)
    
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

            
    # update the screen
    pg.display.update()

pg.quit()
sys.exit()