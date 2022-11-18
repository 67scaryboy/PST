import pygame, sys
from pygame.locals import *
import random
import constantes as const


DISPLAYSURF = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
DISPLAYSURF.fill(const.WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
      def __init__(self, id):
        super().__init__()
        self.active = 1
        if id == 1:
            self.image = pygame.image.load("sprites/e1.png")
            self.PV = 100 #PV de ce type d'adversaire
            self.ATK = 10 #Attaque de ce type d'adversaire
            self.score = 10 #Score crédité en cas de kill
            self.id = 'e1' #ID de ce type
        elif id == 2:
            self.image = pygame.image.load("sprites/e2.png")
            self.PV = 150
            self.ATK = 30
            self.score = 50
            self.id = 'e2'
        elif id == 3:
            self.image = pygame.image.load("sprites/e3.png")
            self.PV = 200
            self.ATK = 50
            self.score = 100
            self.id = 'e3'
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(const.ZONE_MORTE + 50,const.SCREEN_WIDTH-50),0)

      def move(self):
        self.rect.move_ip(0,2)
        if (self.rect.bottom > const.SCREEN_HEIGHT):
            self.kill()

      def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        if id == 0:#selecteur de perso
            self.image = pygame.image.load("sprites/souris.png")
            self.id = 'N/A'
            self.PV = 10
            self.ATK = 0
            self.cooldown = 100
        if id == 1:
            self.image = pygame.image.load("sprites/p1.png")
            self.id = 'p1'
            self.PV = 100 #a modifier en fonction de perso
            self.ATK = 70
            self.cooldown = 10
        elif id == 2:
            self.image = pygame.image.load("sprites/p2.png")
            self.id = 'p2'
            self.PV = 130 #a modifier en fonction de perso
            self.ATK = 100
            self.cooldown = 20
        elif id == 3:
            self.image = pygame.image.load("sprites/p3.png")
            self.id = 'p3'
            self.PV = 150 #a modifier en fonction de perso
            self.ATK = 150
            self.cooldown = 30

        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT - 50))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -7)

        if (self.rect.bottom < const.SCREEN_HEIGHT):
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,7)

        if self.rect.left > const.ZONE_MORTE:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-7, 0)
        if self.rect.right < const.SCREEN_WIDTH:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(7, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def souris(self,surface):
        self.rect.center = pygame.mouse.get_pos()
        self.draw(surface)

class Compagon(pygame.sprite.Sprite):
    def __init__(self,perso):
        super().__init__()
        self.image = pygame.image.load("sprites/e3.png")
        self.ATK = 10
        self.rect = self.image.get_rect()
        self.rect.center = perso.rect.center
        self.rect.right = perso.rect.left-10
        self.deplacementX =0
        self.deplacementY =0
        self.id = 'c1'

    def update(self,perso):
        
        self.rect.center= (perso.rect.right+self.deplacementX,perso.rect.top+ self.deplacementY)
        #if (random.randint(0,1)==1): #Léger déplacement aléatoire du compagnon, a modif pr eviter l'épilepsie
        self.deplacementX+=random.randint(-1,1)
        if ((self.rect.right+self.deplacementX-perso.rect.right<20 or perso.rect.right-self.rect.right<20) and self.rect.right<const.SCREEN_WIDTH and self.rect.left >0):
            self.rect.right = self.rect.right+self.deplacementX
        #else:
        self.deplacementY+= random.randint(-1,1)
        if ((self.rect.top+self.deplacementY-perso.rect.top<10 or perso.rect.top-self.rect.top<10) and self.rect.bottom<const.SCREEN_HEIGHT and self.rect.bottom >0):
            self.rect.bottom = self.rect.top+self.deplacementY
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
