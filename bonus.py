import pygame, sys, math
from pygame.locals import *
import random, personnages, menu, fight
import constantes as const

class boost_ATK():
    def __init__(self,origine,value,catégorie):
        super().__init__()
        self.boost = value
        self.type = catégorie
        self.image = pygame.image.load("sprites/tir.png")#modifier l'image
        self.rect = self.image.get_rect()
        self.rect.center = origine.rect.center
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        self.rect.move_ip(0,3)
        if ((self.rect.bottom > const.SCREEN_HEIGHT) or (self.rect.top < 0)):
            self.kill()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def boost(self,p_P1):
        p_P1.ATK += self.boost
    
    def heal(self,p_P1):
        p_P1.PV += self.boost