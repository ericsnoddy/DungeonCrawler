import pygame as pg

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft = (x,y))

    def draw (self, surf):
        action = False

        # get mouse position, check mouseover
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                action = True

        surf.blit(self.image, self.rect)

        return action