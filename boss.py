import pygame, sys, math
from pygame.locals import *
import random, personnages, menu, bonus, fight
import constantes as const

class ModularBoss_main_body(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()#pas de hitbox, ni d'id de tir, sert juste de jointure entre les deux bras
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2,50)

class ModularBoss_left_arm(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()#bras gauche
        self.rect = self.image.get_rect()
        self.id = 'bossg'
        self.rect.center = (const.SCREEN_WIDTH//2 + 50,50)
        self.mask = pygame.mask.from_surface(self.image)

class ModularBoss_right_arm(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()#bras droite
        self.rect = self.image.get_rect()
        self.id = 'bossd'
        self.rect.center = (const.SCREEN_WIDTH//2 - 50,50)
        self.mask = pygame.mask.from_surface(self.image)