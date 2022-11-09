import pygame, sys
from pygame.locals import *
import random, personnages
import constantes as const

def Spawn(enemies,q):#random, pour le mode arcade
    p = random.randint(0,100)
    if p < q:
        p2 = random.randint(1,3)#a modifier pour avoir une proba dépendant de la difficulté
        if p2 == 1:
            enemy  = personnages.Enemy(1)
        elif p2 == 2:
            enemy  = personnages.Enemy(2)
        elif p2 == 3:
            enemy  = personnages.Enemy(3)
        enemies.append(enemy)

class Projectile(pygame.sprite.Sprite):
      def __init__(self, tireur):
        super().__init__()
        self.damage = tireur.ATK
        self.direction = [0,1,0,0]#a modifier pour adapter en fonction de tireur
        self.image = pygame.image.load("tir.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(const.ZONE_MORTE + 50,const.SCREEN_WIDTH-50),0)

      def move(self):
        self.rect.move_ip(0,3)
        if (self.rect.bottom > const.SCREEN_HEIGHT):
            self.kill()

      def draw(self, surface):
        surface.blit(self.image, self.rect)