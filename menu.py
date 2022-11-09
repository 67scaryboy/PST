import pygame, sys, personnages
from pygame.locals import *
import constantes as const

FramePerSec = pygame.time.Clock()

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
        self.rect.bottom = const.SCREEN_HEIGHT

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self):
        self.rect.move_ip(0,1)
        if (self.rect.bottom > const.SCREEN_HEIGHT+512):
            self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT//2))
            self.rect.bottom = const.SCREEN_HEIGHT
            

def ChoixPerso():
    #Choix perso
    E1 = personnages.Player(1)
    personnages.DISPLAYSURF.fill(const.WHITE)
    E1.rect.center = ((const.SCREEN_WIDTH//2)-200,const.SCREEN_HEIGHT//2)
    E1.draw(personnages.DISPLAYSURF)
    E1 = personnages.Player(2)
    E1.rect.center = (const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT//2)
    E1.draw(personnages.DISPLAYSURF)
    E1 = personnages.Player(3)
    E1.rect.center = ((const.SCREEN_WIDTH//2)+200,const.SCREEN_HEIGHT//2)
    E1.draw(personnages.DISPLAYSURF)
    pygame.display.update()
    while True:
        FramePerSec.tick(const.FPS)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a]:
            personnages.DISPLAYSURF.fill(const.WHITE)
            return 1
        if pressed_keys[K_b]:
            personnages.DISPLAYSURF.fill(const.WHITE)
            return 2
        if pressed_keys[K_c]:
            personnages.DISPLAYSURF.fill(const.WHITE)
            return 3
        pygame.display.update()
        FramePerSec.tick(const.FPS)