# std lib
import sys
from csv import reader
from os.path import join

# installed
import pygame as pg
from pygame.locals import *

# local
from weapon import Weapon
from items import Item
from world import World
from button import Button
from constants import (
    FIREBALL_SCALE, WIDTH, HEIGHT, FPS, 
    TILESIZE, TILE_TYPES, MAP_ROWS, MAP_COLS,
    SCALE, BUTTON_SCALE, WEAP_SCALE, ITEM_SCALE, POTION_SCALE, FIREBALL_SCALE, SPEED,
    BG, RED, PINK, WHITE, BLACK, PANEL
)



# init display
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Diamblo')

clock = pg.time.Clock()

# define font
font = pg.font.Font(join('assets', 'fonts', 'AtariClassic.ttf'), 20)

# define game variables
level = 1
start_intro = True
screen_scroll = [0, 0]



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

    # show level
    draw_text('Level: ' + str(level), font, WHITE, WIDTH // 2, 15)
    # show score
    draw_text(f'x{player.score}', font, WHITE, WIDTH - 100, 15)

# function to reset level
def reset_level():
    
    # empty groups
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    # create empty tile list
    # create a list of a list of '-1's populating entire map ROWS*COLS
    data = []
    for _ in range(MAP_ROWS):
        r = [-1] * MAP_COLS  # '*' operator acts to create a list with MAP_COLS number of values
        data.append(r)
    
    return data



# displaying damage
class DamageText(pg.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        super().__init__()
        self.image = font.render(str(damage), True, color)
        self.rect= self.image.get_rect(center=(x,y))
        self.counter = 0

    def update(self):
        
        # reposition based on screen_scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # float the damage text
        self.rect.y -= 1

        # delete the counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


class ScreenWipe():
    def __init__(self, wipe_type, color, speed):
        self.wipe_type = wipe_type
        self.color = color
        self.speed = speed
        self.wipe_counter = 0
        
    def wipe(self):
        wipe_complete = False
        self.wipe_counter += self.speed
        if self.wipe_type == 'shutter':
            # shutter open wipe
            pg.draw.rect(WIN, self.color, (0 - self.wipe_counter, 0, WIDTH // 2, HEIGHT))
            pg.draw.rect(WIN, self.color, (WIDTH // 2 + self.wipe_counter, 0, WIDTH, HEIGHT))
            pg.draw.rect(WIN, self.color, (0, 0 - self.wipe_counter, WIDTH, HEIGHT // 2))
            pg.draw.rect(WIN, self.color, (0, HEIGHT // 2 + self.wipe_counter, WIDTH, HEIGHT))

            if self.wipe_counter >= WIDTH:
                wipe_complete = True

        elif self.wipe_type == 'curtain':
            # curtain wipe
            pg.draw.rect(WIN, self.color, (0, 0, WIDTH, 0 + self.wipe_counter))

            if self.wipe_counter >= HEIGHT:
                wipe_complete = True
        
        return wipe_complete

### GAME SETUP ###

# load button images
restart_img = scale_img(pg.image.load(join('assets', 'images', 'buttons', 'button_restart.png')).convert_alpha(), BUTTON_SCALE)

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
arrow_image = scale_img(pg.image.load(join('assets', 'images', 'weapons', 'arrow.png')).convert_alpha(), WEAP_SCALE)
fireball_image = scale_img(pg.image.load(join('assets', 'images', 'weapons', 'fireball.png')).convert_alpha(), FIREBALL_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)


# load tile map images
tile_list = []
for x in range(TILE_TYPES):
    tile_image = pg.image.load(join('assets', 'images', 'tiles', f'{x}.png'))
    tile_image = pg.transform.scale(tile_image, (TILESIZE, TILESIZE))
    tile_list.append(tile_image)


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


# create a list of a list of '-1's populating entire map ROWS*COLS
world_data = []
for row in range(MAP_ROWS):
    r = [-1] * MAP_COLS  # '*' operator acts to create a list with MAP_COLS number of values
    world_data.append(r)

# overwrite the -1s in world_data list where applicable
with open(join('levels', f'level{level}_data.csv'), newline='') as csv_file:
    csv_reader = reader(csv_file, delimiter=',')
    for x, row in enumerate(csv_reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

# create world
world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)






# create entities
player = world.player
enemy_list = world.enemies

# create weapon
bow = Weapon(bow_image, arrow_image)

# create sprite groups
damage_text_group = pg.sprite.Group()
arrow_group = pg.sprite.Group()
item_group = pg.sprite.Group()
fireball_group = pg.sprite.Group()

score_coin = Item(WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)
# add items from level data
for item in world.item_list:
    item_group.add(item)

# player control vars
moving_l = False
moving_r = False
moving_u = False
moving_d = False


# create screen wipes
intro_wipe = ScreenWipe('shutter', BLACK, 4)
death_wipe = ScreenWipe('curtain', PINK, 4)

# buttons
restart_btn = Button((WIDTH - restart_img.get_width()) // 2, (HEIGHT - restart_img.get_height()) // 2, restart_img)

### GAME LOOP ###

running = True
while running:
    
    # control the framerate
    clock.tick(FPS)

    # bg
    WIN.fill(BG)

    # do while alive
    if player.alive:

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
        screen_scroll, level_complete = player.move(direction_vect, world.obstacle_tiles, world.exit_tile)

        # update all objects
        world.update(screen_scroll)
        player.update()
        for enemy in enemy_list:
            fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
            if fireball:
                fireball_group.add(fireball)
            if enemy.alive:
                enemy.update()
        arrow = bow.update(player)
        if arrow:
            arrow_group.add(arrow)
        for arrow in arrow_group.sprites():
            damage, damage_pos = arrow.update(world.obstacle_tiles, enemy_list, screen_scroll)
            if damage:
                damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
                damage_text_group.add(damage_text)
        damage_text_group.update()
        fireball_group.update(screen_scroll, player)
        item_group.update(screen_scroll, player)
    


    # draw all objects
    world.draw(WIN)
    player.draw(WIN)
    bow.draw(WIN)
    for arrow in arrow_group.sprites():
        arrow.draw(WIN)
    for enemy in enemy_list:
        enemy.draw(WIN)
    for fireball in fireball_group.sprites():
        fireball.draw(WIN)
    damage_text_group.draw(WIN)
    item_group.draw(WIN)
    draw_info_panel()
    score_coin.draw(WIN)

    # check for level complete
    if level_complete:
        start_intro = True
        level += 1
        world_data = reset_level()

        # overwrite the -1s in world_data list where applicable
        with open(join('levels', f'level{level}_data.csv'), newline='') as csv_file:
            csv_reader = reader(csv_file, delimiter=',')
            for x, row in enumerate(csv_reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

        # create next world (copy/paste job from above)
        world = World()
        world.process_data(world_data, tile_list, item_images, mob_animations)

        # save variables / create player / restore variables
        temp_hp = player.health
        temp_score = player.score
        player = world.player
        player.health = temp_hp
        player.score = temp_score

        # populate level
        enemy_list = world.enemies
        score_coin = Item(WIDTH - 115, 23, 0, coin_images, True)
        item_group.add(score_coin)
        for item in world.item_list:
            item_group.add(item)

    # show intro
    if start_intro:
        done = intro_wipe.wipe()
        if done:
            start_intro = False
            intro_wipe.wipe_counter = 0

    # show death screen
    if not player.alive:
        done = death_wipe.wipe()
        if done:
            is_clicked = restart_btn.draw(WIN)
            if is_clicked:
                death_wipe.wipe_counter = 0
                # back to intro wipe
                start_intro = True

                # copy/paste job to reset level - shitty redundancy
                world_data = reset_level()
                with open(join('levels', f'level{level}_data.csv'), newline='') as csv_file:
                    csv_reader = reader(csv_file, delimiter=',')
                    for x, row in enumerate(csv_reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                world.process_data(world_data, tile_list, item_images, mob_animations)
                player = world.player
                enemy_list = world.enemies
                score_coin = Item(WIDTH - 115, 23, 0, coin_images, True)
                item_group.add(score_coin)
                for item in world.item_list:
                    item_group.add(item)

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