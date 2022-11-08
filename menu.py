import pygame, sys
from pygame.locals import *
import constantes as const


class MenuGauche(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Menu_Gauche.png") 
        self.rect = self.image.get_rect()
        self.rect.center = (const.ZONE_MORTE//2, (const.SCREEN_HEIGHT//2))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Arrièreplan(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("temp.png") 
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT//2))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self):#au lieu de le faire repasser en haut si il touche le bas, le faire disparaitre.
        self.rect.move_ip(0,5)
        if (self.rect.top > self.rect.top/3):
            self.rect.top = 0
            self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT//2))
            