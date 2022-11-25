import pygame, sys, math
from pygame.locals import *
import random, personnages, menu, bonus, fight
import constantes as const

class ModularBoss_main_body(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/e2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2,50)
        self.id = "body"
        self.destination = const.SCREEN_WIDTH//2
        self.PVMAX = 1000
        self.PV = self.PVMAX
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def move(self):
        position = self.rect.right - (self.rect.right-self.rect.left)
        if position < self.destination:
            self.rect.move_ip(1,0)
        elif position > self.destination:
            self.rect.move_ip(-1,0)
        else:
            self.destination = random.randint(0,const.SCREEN_WIDTH)

class ModularBoss_destructible(pygame.sprite.Sprite):
    def __init__(self,mainbody):
        super().__init__()#bras gauche
        self.image = pygame.image.load("sprites/e2.png")
        self.rect = self.image.get_rect()
        self.id = 'bossd'
        self.PVMAX = 1000
        self.PV = self.PVMAX
        self.rect.center = mainbody.rect.center
        self.mask = pygame.mask.from_surface(self.image)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def move(self,mainbody):
        self.rect.center = mainbody.rect.center

def Bossfight():
    FramePerSec = pygame.time.Clock()
    ScoreBoss = 0
    alive = True

    AP = menu.Arrièreplan(2)# 1 a 3 pour le fond
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)#menu bas
    P1 = personnages.Player(menu.ChoixPerso())
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)

    Body = ModularBoss_main_body()
    Piece1 = ModularBoss_destructible(Body)

    cooldown = P1.cooldown

    MorceauxBoss = [Piece1] 
    tirs = []
    explo = []

    while alive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #mouvements ennemis
        Body.move()
        for Morceau in MorceauxBoss:
                if Morceau.PV > 0:
                    Morceau.move(Body)
                #ici pour décider si il tire

        #tir automatique
        if P1.cooldown == 0:
            shoot = fight.Projectile(P1,0)
            tirs.append(shoot)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1

        #faire avance les tirs
        for shoot in tirs:
            shoot.move()
            if shoot.rect.bottom > const.SCREEN_HEIGHT:
                    tirs.remove(shoot)
    
        AP3.move(3)#vitesse de déplacement des couches
        AP2.move(2)
        AP.move(1)#laisser 1 pour le fond, sinon ca file la gerbe

        ScoreBoss,alive=BossColision(tirs,P1,MorceauxBoss,explo,ScoreBoss,alive)#surement devoir faire colision boss

        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        
        for shoot in tirs:#ici pour les animations des tirs animées
            shoot.draw(personnages.DISPLAYSURF)

        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)

        Body.draw(personnages.DISPLAYSURF)
        for Morceau in MorceauxBoss:
            if Morceau.PV > 0:
                Morceau.draw(personnages.DISPLAYSURF)
        P1.souris(personnages.DISPLAYSURF)#Affichage joueur
        P1.draw_health(personnages.DISPLAYSURF)
        MB.draw(personnages.DISPLAYSURF)#Affichage menu gauche
        menu.AfficheScore(ScoreBoss) #Affichage score


        pygame.display.update()
        FramePerSec.tick(const.FPS)
    return (ScoreBoss)

def BossColision(p_tirs,p_P1,p_morceaux,p_explo,tempscore,p_alive):
    for shoot in p_tirs:
        if shoot.team == 0:#si tir enemi
            if pygame.sprite.collide_mask(shoot,p_P1):
                p_P1.PV -= shoot.damage
                if shoot in p_tirs:
                    p_tirs.remove(shoot)
                if p_P1.PV <= 0:
                    p_alive = fight.Mort(tempscore,p_tirs,p_P1,p_morceaux)
        else:    
            for morceaux in p_morceaux:
                if pygame.sprite.collide_mask(shoot,morceaux):
                    morceaux.PV -=  shoot.damage
                    if shoot in p_tirs:
                        p_tirs.remove(shoot)
                    if morceaux.PV <= 0:
                        tempscore+=0
                        p_explo.append(menu.explosion(morceaux))
                        p_morceaux.remove(morceaux)
                
    return (tempscore,p_alive)
