import pygame, sys
from pygame.locals import *
import constantes as const


class MenuGauche(pygame.sprite.Sprite): #Pas terminé, faut créer le sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Menu_Gauche.png") #Faire image menu
        self.rect = self.image.get_rect()
        self.rect.center = (const.ZONE_MORTE//2, (const.SCREEN_HEIGHT//2))

    def draw(self, surface):
        surface.blit(self.image, self.rect)