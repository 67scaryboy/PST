import pygame, sys, math
from pygame.locals import *
import random, personnages, menu, fight
import constantes as const

class booster(pygame.sprite.Sprite): #les objets qui peuvent être drop par les ennemis lorsque ces derniers sont tuées
    def __init__(self,origine,value,catégorie):
        super().__init__()
        self.boost = value       #La valeur du boost
        self.type = catégorie    #le type de boost :
        if catégorie == 0:          #boost ATK
            self.image = pygame.image.load("sprites/bonusatk.png").convert_alpha()
        elif catégorie == 1:        #boost PV
            self.image = pygame.image.load("sprites/bonusvie.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = origine.rect.center             #place le booster aux coordonées de l'ennemi qui l'a drop
        self.mask = pygame.mask.from_surface(self.image)   #pour des colisions précises
    
    def move(self):               #faire se déplacer le booster
        self.rect.move_ip(0,3)
    
    def draw(self, surface):     #afficher le booster
        surface.blit(self.image, self.rect)
    
    def useBooster(self,p_P1):   #appliquer l'effet du booster
        if self.type == 0:         
            p_P1.ATK += self.boost    
        elif self.type == 1:
            p_P1.PV += self.boost
            if p_P1.PV > p_P1.MAXPV:
                p_P1.PV = p_P1.MAXPV


def dropBooster(liste_boosts,origine): #donne une chance de faire drop des boosters
    p = random.randint(0, 100)                          #5% de chance de drop
    if p <= 5:
        q = random.randint(0, 100)
        if q < 50:
            liste_boosts.append(booster(origine,50,1))  #50% de chances que ce soit un booster de type PV (+50 PV)
        else:
            liste_boosts.append(booster(origine,10,0))  #50% de chances que ce soit un booster de type ATK (+10 ATK)

def AttraperBoost(liste_boosts,p_P1):                  #permet au joueur d'attraper le boost 
    for boost in liste_boosts:
        if pygame.sprite.collide_rect(p_P1,boost):
            if pygame.sprite.collide_mask(p_P1,boost): #si le boost touche le joueur 
                boost.useBooster(p_P1)
                liste_boosts.remove(boost)             #l'utillise et le supprime

 