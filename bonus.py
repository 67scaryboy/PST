import pygame, sys, math
from pygame.locals import *
import random, personnages, menu, fight
import constantes as const

class booster(pygame.sprite.Sprite):
    def __init__(self,origine,value,catégorie):
        super().__init__()
        self.boost = value
        self.type = catégorie
        if catégorie == 0:#boost ATK
            self.image = pygame.image.load("sprites/bonusatk.png").convert_alpha()
        elif catégorie == 1:#boost PV
            self.image = pygame.image.load("sprites/bonusvie.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = origine.rect.center
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        self.rect.move_ip(0,3)
        if (self.rect.bottom > const.SCREEN_HEIGHT):
            self.kill()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def useBooster(self,p_P1):
        if self.type == 0: 
            p_P1.ATK += self.boost
        elif self.type == 1:
            p_P1.PV += self.boost
            if p_P1.PV > p_P1.MAXPV:
                p_P1.PV = p_P1.MAXPV


def dropBooster(liste_boosts,origine):#faire l'équilibrage plus tard
    p = random.randint(0, 100)
    if p <= 5:
        q = random.randint(0, 100)
        if q < 50:
            liste_boosts.append(booster(origine,50,1))  #rend 50 PV
        else:
            liste_boosts.append(booster(origine,10,0)) #donne +10 attaque

def AttraperBoost(liste_boosts,p_P1):
    for boost in liste_boosts:
        if pygame.sprite.collide_mask(p_P1,boost):
            boost.useBooster(p_P1)
            liste_boosts.remove(boost)

 