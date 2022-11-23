import pygame, sys, math
from pygame.locals import *
import random, personnages, menu, bonus
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
    alive = True

    AP = menu.Arrièreplan(3)# 1 a 3 pour le fond
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(menu.ChoixPerso())
    E1 = personnages.Enemy(1)
    CP = personnages.Compagon(P1)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)

    cooldown = P1.cooldown

    enemies = [] 
    enemies.append(E1)
    tirs = []
    explo = []
    boosts = []

    while alive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        CP.update(P1)
        #mouvements ennemis
        for entity in enemies:
            if entity.active == 1:
                entity.move()
                #ici pour décider si il tire
                p = random.randint(0,100)
                if p < 1:
                    shoot = Projectile(entity,3)# remettre 0
                    tirs.append(shoot)
                #supprimer les tirs qui sortent de l'écrant
                if entity.rect.bottom > const.SCREEN_HEIGHT:
                    enemies.remove(entity)

        #tir automatique
        if P1.cooldown == 0:
            shoot = Projectile(P1,0)
            shootf= Projectile(CP,0)
            tirs.append(shoot)
            tirs.append(shootf)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1

        #faire avance les tirs
        for shoot in tirs:
            shoot.move()
            if shoot.rect.bottom > const.SCREEN_HEIGHT:
                    tirs.remove(shoot)
        
        for boost in boosts:
            boost.move()
            if boost.rect.bottom > const.SCREEN_HEIGHT:
                    boosts.remove(boost)
    
        AP3.move(3)#vitesse de déplacement des couches
        AP2.move(2)
        AP.move(1)#laisser 1 pour le fond, sinon ca file la gerbe

        scoreArcade,alive=Colision(tirs,P1,enemies,explo,boosts,scoreArcade,alive)

        bonus.AttraperBoost(boosts,P1)

        Spawn(enemies,2)

        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        
        for shoot in tirs:
            if shoot.trajectoire == 3:
                menu.Animation(const.boules,shoot)
            shoot.draw(personnages.DISPLAYSURF)
        
        for boost in boosts:
            boost.draw(personnages.DISPLAYSURF)

        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)

        for entity in enemies:
            if entity.active == 1:
                entity.draw(personnages.DISPLAYSURF)
        P1.souris(personnages.DISPLAYSURF)#Affichage joueur
        P1.draw_health(personnages.DISPLAYSURF)
        CP.draw(personnages.DISPLAYSURF)#Affichage Compagnon
        MB.draw(personnages.DISPLAYSURF)#Affichage menu gauche
        menu.AfficheScore(scoreArcade) #Affichage score


        pygame.display.update()
        FramePerSec.tick(const.FPS)
    return (scoreArcade)


class Projectile(pygame.sprite.Sprite):
      def __init__(self, tireur,traj):
        super().__init__()
        self.damage = tireur.ATK
        if tireur.id == 'e1': #Affiche differents tir en fonction de l'id tireur (e=ennemis, p=player, c=compagnon)
            self.direction = [0,4]
            self.image = pygame.image.load("sprites/tir.png")
            self.team = 0# 0 pour les tirs enemis et 1 pour les aliés

        elif tireur.id == 'e2':
            self.direction = [0,4]
            self.image = pygame.image.load("sprites/tir.png")
            self.team = 0
            
        elif tireur.id == 'e3':
            self.direction = [0,4]
            self.image = pygame.image.load("sprites/tir.png")
            self.team = 0
            
        elif tireur.id == 'p1':
            self.direction = [0,-3]
            self.image = pygame.image.load("sprites/tira.png")
            self.team = 1
            
        elif tireur.id == 'p2':
            self.direction = [0,-3]
            self.image = pygame.image.load("sprites/tira.png")
            self.team = 1
            
        elif tireur.id == 'p3':
            self.direction = [0,-3]
            self.image = pygame.image.load("sprites/tira.png")
            self.team = 1

        elif tireur.id == 'c1':
            self.direction = [0,-3]
            self.image = pygame.image.load("sprites/tira.png")
            self.team = 1
        self.trajectoire = traj 
        self.time = 0
        self.rect = self.image.get_rect()
        self.rect.center = tireur.rect.center
        self.mask = pygame.mask.from_surface(self.image)

      def move(self):
        self.rect.move_ip(self.direction[0],self.direction[1])

        if self.trajectoire == 1:#logarithme droite
            temp = 2*(math.log(self.time+61/2)-math.log(self.time+1/2))
            self.direction = [temp,math.sqrt(9-temp)+2]
        elif self.trajectoire == 2:#logarithme gauche
            temp = 2*(math.log(self.time+61/2)-math.log(self.time+1/2))
            self.direction = [-temp,math.sqrt(9-temp)+2]
        elif self.trajectoire == 3:#cosinus
            temp = 3* math.cos(self.time/20)
            self.direction = [temp,math.sqrt(9-temp*temp)+2]
        elif self.trajectoire == 3:#diagonale droite
            self.direction = [1,2]
        elif self.trajectoire == 3:#diagonale gauche
            self.direction = [-1,2]

        self.time += 1
        if ((self.rect.bottom > const.SCREEN_HEIGHT) or (self.rect.top < 0)):
            self.kill()

      def draw(self, surface):
        surface.blit(self.image, self.rect)

def Colision(p_tirs,p_P1,p_enemies,p_explo,boosts,tempscore,p_alive):
    for shoot in p_tirs:
        if shoot.team == 0:#si tir enemi
            if pygame.sprite.collide_mask(shoot,p_P1):
                p_P1.PV -= shoot.damage
                if shoot in p_tirs:
                    p_tirs.remove(shoot)
                if p_P1.PV <= 0:
                    p_alive = Mort(tempscore,p_tirs,p_P1,p_enemies)
        else:    
            for enemy in p_enemies:
                if pygame.sprite.collide_mask(p_P1,enemy):#Attention ici, a modif, si on collide un boss, on le tue direct du coup !
                    p_P1.PV -= enemy.ATK
                    tempscore+=enemy.score
                    p_explo.append(menu.explosion(enemy))
                    bonus.dropBooster(boosts,enemy)
                    p_enemies.remove(enemy)
                    if p_P1.PV <= 0:
                        p_alive = Mort(tempscore,p_tirs,p_P1,p_enemies)
                elif pygame.sprite.collide_mask(shoot,enemy):
                    enemy.PV -=  shoot.damage
                    if shoot in p_tirs:
                        p_tirs.remove(shoot)
                    if enemy.PV <= 0:
                        tempscore+=enemy.score
                        p_explo.append(menu.explosion(enemy))
                        bonus.dropBooster(boosts,enemy)
                        p_enemies.remove(enemy)
                
    return (tempscore,p_alive)
    
def Mort(p_score,p_tirs,p_P1,p_enemies):
    for shoot in p_tirs:
        p_tirs.remove(shoot)
    for enemy in p_enemies:
        p_enemies.remove(enemy)
    return False