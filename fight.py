import pygame, sys
from pygame.locals import *
import random, personnages, menu
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

def Arcade():
    FramePerSec = pygame.time.Clock()

    AP = menu.Arrièreplan()
    MG = menu.MenuGauche()
    P1 = personnages.Player(1)
    E1 = personnages.Enemy(1)
    CP = personnages.Compagon(P1)

    enemies = [] 
    enemies.append(E1)
    tirs = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        P1.update()
        CP.update(P1)
        for entity in enemies:
            if entity.active == 1:
                entity.move()
                #ici pour décider si il tire
                p = random.randint(0,100)
                if p < 1:
                    shoot = Projectile(entity)
                    tirs.append(shoot)
                if entity.rect.bottom > const.SCREEN_HEIGHT:
                    enemies.remove(entity)
    
        if P1.cooldown == 0:
            shoot = Projectile(P1)
            tirs.append(shoot)
            P1.cooldown = 60 #trouver un moyen pour récupérer la valeur initiale
        else:
            P1.cooldown += -1
    
        for shoot in tirs:
            shoot.move()
            if shoot.rect.bottom > const.SCREEN_HEIGHT:
                    tirs.remove(shoot)
    
        AP.move()

        Spawn(enemies,2)

        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)

        for shoot in tirs:
            personnages.DISPLAYSURF.blit(entity.image, entity.rect)
            shoot.draw(personnages.DISPLAYSURF)

        for entity in enemies:
            if entity.active == 1:
                personnages.DISPLAYSURF.blit(entity.image, entity.rect)
                entity.draw(personnages.DISPLAYSURF)
        P1.draw(personnages.DISPLAYSURF)
        CP.draw(personnages.DISPLAYSURF)
        MG.draw(personnages.DISPLAYSURF)


        pygame.display.update()
        FramePerSec.tick(const.FPS)


class Projectile(pygame.sprite.Sprite):
      def __init__(self, tireur):
        super().__init__()
        self.damage = tireur.ATK
        if tireur.id == 'e1':
            self.direction = [0,3]
            self.team = 0# 0 pour les tirs enemis et 1 pour les aliés
        elif tireur.id == 'e2':
            self.direction = [0,3]
            self.team = 0
        elif tireur.id == 'e3':
            self.direction = [0,3]
            self.team = 0
        elif tireur.id == 'p1':
            self.direction = [0,-3]
            self.team = 1
        elif tireur.id == 'p2':
            self.direction = [0,-3]
            self.team = 1
        elif tireur.id == 'p3':
            self.direction = [0,-3]
            self.team = 1
        elif tireur.id == 'c1':
            self.direction = [0,-3]
            self.team = 1
        self.image = pygame.image.load("tir.png")#à modifier en fonction du perso/ATK
        self.rect = self.image.get_rect()
        self.rect.center = tireur.rect.center

      def move(self):
        self.rect.move_ip(self.direction[0],self.direction[1])
        if ((self.rect.bottom > const.SCREEN_HEIGHT) or (self.rect.top < 0)):
            self.kill()

      def draw(self, surface):
        surface.blit(self.image, self.rect)