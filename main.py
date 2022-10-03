# std lib
import sys
from os.path import join
from numpy import str0

# installed
import pygame as pg
from pygame.locals import *

# local
from constants import WIDTH, HEIGHT, FPS, SCALE, WEAP_SCALE, ITEM_SCALE, POTION_SCALE, SPEED, ELF_HEALTH, BG, RED, WHITE, PANEL
from character import Character
from weapon import Weapon
from items import Item



# init display
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Diamblo')

clock = pg.time.Clock()

# define font
font = pg.font.Font(join('assets', 'fonts', 'AtariClassic.ttf'), 20)

### HELPER FUNCTIONS ###
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pg.transform.scale(image, (w * scale, h * scale))

def draw_text(text_string, font, color, x, y):
    img = font.render(text_string, True, color)
    WIN.blit(img, (x, y))

def draw_info_panel():

    # separate info panel from the play field
    pg.draw.rect(WIN, PANEL, (0, 0, WIDTH, 50))
    pg.draw.line(WIN, WHITE, (0, 50), (WIDTH, 50))

    half_heart_drawn = False
    # draw lives
    for i in range(5):

        # convert 100HP into hearts: full = 20 hp, half = 10hp
        if player.health >= ((i + 1) * 20):
            WIN.blit(heart_full, (10 + i * 50, 0))
        # remainder gets converted to half heart, but we want no more than 1 half heart
        elif player.health % 20 > 0 and not half_heart_drawn:
            WIN.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            WIN.blit(heart_empty, (10 + i * 50, 0))

    # show score
    draw_text(f'Score: {player.score}', font, WHITE, WIDTH - 100, 50)

# displaying damage
class DamageText(pg.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        super().__init__()
        self.image = font.render(str(damage), True, color)
        self.rect= self.image.get_rect(center=(x,y))
        self.counter = 0

    def update(self):
        
        # float the damage text
        self.rect.y -= 1

        # delete the counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()

### GAME SETUP ###

# load heart images
heart_empty = scale_img(pg.image.load(join('assets', 'images', 'items', 'heart_empty.png')).convert_alpha(), ITEM_SCALE)
heart_half = scale_img(pg.image.load(join('assets', 'images', 'items', 'heart_half.png')).convert_alpha(), ITEM_SCALE)
heart_full = scale_img(pg.image.load(join('assets', 'images', 'items', 'heart_full.png')).convert_alpha(), ITEM_SCALE)

# load item images
coin_images = []
for i in range(4):
    img = scale_img(pg.image.load(join('assets', 'images', 'items', f'coin_f{i}.png')).convert_alpha(), ITEM_SCALE)
    coin_images.append(img)
red_potion = scale_img(pg.image.load(join('assets', 'images', 'items', 'potion_red.png')).convert_alpha(), POTION_SCALE)

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


# create player
# player = Character(100, 100, ELF_HEALTH, mob_animations, 0)
player = Character(100, 100, 70, mob_animations, 0)

# create weapon
bow = Weapon(bow_image, arrow_image)

# create sprite groups
damage_text_group = pg.sprite.Group()
arrow_group = pg.sprite.Group()
item_group = pg.sprite.Group()

potion = Item(200, 200, 1, [red_potion])
item_group.add(potion)

coin = Item(300, 300, 0, coin_images)
item_group.add(coin)

# create enemy
enemy = Character(200, 300, 100, mob_animations, 1)
enemy_list = []
enemy_list.append(enemy)

# player control vars
moving_l = False
moving_r = False
moving_u = False
moving_d = False


### GAME LOOP ###
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
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(player)
    
    player.draw(WIN)
    bow.draw(WIN)
    for arrow in arrow_group.sprites():
        arrow.draw(WIN)
    for enemy in enemy_list:
        enemy.draw(WIN)
    damage_text_group.draw(WIN)
    item_group.draw(WIN)
    draw_info_panel()
    
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