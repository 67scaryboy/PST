import pygame, sys
from pygame.locals import *
import random
import constantes as const
import personnages


DISPLAYSURF = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
DISPLAYSURF.fill(const.WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.active = 1
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(const.ZONE_MORTE + 50,const.SCREEN_WIDTH-50),0)

      def move(self):#au lieu de le faire repasser en haut si il touche le bas, le faire disparaitre.
        self.rect.move_ip(0,3)
        if (self.rect.bottom > const.SCREEN_HEIGHT):
            self.kill()

      def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT - 50))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -7.5)

        if (self.rect.bottom < const.SCREEN_HEIGHT):
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,7.5)

        if self.rect.left > const.ZONE_MORTE:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-7.5, 0)
        if self.rect.right < const.SCREEN_WIDTH:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(7.5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Compagon(pygame.sprite.Sprite):
    def __init__(self,perso):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = perso.rect.center
        self.rect.right = perso.rect.left-10

    def update(self,perso):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -7.5)

        if (self.rect.bottom < const.SCREEN_HEIGHT):
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,7.5)

        if self.rect.left > const.ZONE_MORTE:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-7.5, 0)
        if self.rect.right < const.SCREEN_WIDTH:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(7.5, 0)

        if (random.randint(0,1)==1):
            deplacementX= random.randint(-2,2)
            if ((self.rect.right+deplacementX-perso.rect.right<20 or perso.rect.right-self.rect.right<20) and self.rect.right<const.SCREEN_WIDTH and self.rect.left >0):
                self.rect.right = self.rect.right+deplacementX
        else:
            deplacementY= random.randint(-2,2)
            if ((self.rect.top+deplacementY-perso.rect.top<20 or perso.rect.top-self.rect.top<20) and self.rect.bottom<const.SCREEN_HEIGHT and self.rect.bottom >0):
                self.rect.top = self.rect.top+deplacementY
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
