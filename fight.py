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
    scoreArcade = 0

    AP = menu.Arrièreplan()
    MG = menu.MenuGauche()
    P1 = personnages.Player(menu.ChoixPerso())
    E1 = personnages.Enemy(1)
    CP = personnages.Compagon(P1)

    cooldown = P1.cooldown

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
        #mouvements ennemis
        for entity in enemies:
            if entity.active == 1:
                entity.move()
                #ici pour décider si il tire
                p = random.randint(0,100)
                if p < 1:
                    shoot = Projectile(entity)
                    tirs.append(shoot)
                #supprimer les tirs qui sortent de l'écrant
                if entity.rect.bottom > const.SCREEN_HEIGHT:
                    enemies.remove(entity)

        #tir automatique
        if P1.cooldown == 0:
            shoot = Projectile(P1)
            tirs.append(shoot)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1

        #faire avance les tirs
        for shoot in tirs:
            shoot.move()
            if shoot.rect.bottom > const.SCREEN_HEIGHT:
                    tirs.remove(shoot)
    
        AP.move()

        scoreArcade=Colision(tirs,P1,enemies,scoreArcade)

        Spawn(enemies,2)

        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)

        
        for shoot in tirs:
            shoot.draw(personnages.DISPLAYSURF)

        for entity in enemies:
            if entity.active == 1:
                entity.draw(personnages.DISPLAYSURF)
        P1.draw(personnages.DISPLAYSURF)
        CP.draw(personnages.DISPLAYSURF)
        MG.draw(personnages.DISPLAYSURF)
        menu.AfficheScore(scoreArcade) #Affichage score


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
        self.image = pygame.image.load("sprites/tir.png")#à modifier en fonction du perso/ATK
        self.rect = self.image.get_rect()
        self.rect.center = tireur.rect.center

      def move(self):
        self.rect.move_ip(self.direction[0],self.direction[1])
        if ((self.rect.bottom > const.SCREEN_HEIGHT) or (self.rect.top < 0)):
            self.kill()

      def draw(self, surface):
        surface.blit(self.image, self.rect)

def Colision(p_tirs,p_P1,p_enemies,tempscore):#problème, on retire des élements d'une liste que l'on parcours
    for shoot in p_tirs:
        if shoot.team == 0:#si tir enemi
            if pygame.sprite.collide_rect(shoot,p_P1):
                #ajouter subir dégats, test mort et fonction pour gerer mort
                p_tirs.remove(shoot)
        else:    
            for enemy in p_enemies:
                if pygame.sprite.collide_rect(shoot,enemy):
                    enemy.PV -=  shoot.damage
                    p_tirs.remove(shoot)
                    if enemy.PV <= 0:
                        tempscore+=enemy.score
                        p_enemies.remove(enemy)#creer fonction pour les drop, score...
    return (tempscore)
    
                    