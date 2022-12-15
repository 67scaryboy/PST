import pygame, sys, math
from pygame.locals import *
import random, personnages, menu, bonus, fight
import constantes as const
from copy import deepcopy

class ModularBoss_main_body(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites_boss/boss_damaged.png")
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2,80)
        self.cooldown = 100
        self.id = "body"
        self.destination = const.SCREEN_WIDTH//2
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def move(self):# peut être modifier pour contrôle total sur mouvements boss
        position = self.rect.center[0]
        if position < self.destination:
            self.rect.move_ip(1,0)
        elif position > self.destination:
            self.rect.move_ip(-1,0)
        else:
            self.destination = random.randint(70,const.SCREEN_WIDTH-70)

class ModularBoss_destructible(pygame.sprite.Sprite):
    def __init__(self,mainbody,adresse,id):
        super().__init__()#bras gauche
        self.image = pygame.image.load(adresse)
        self.rect = self.image.get_rect()
        self.id = id
        self.PVMAX = 1000
        self.PV = self.PVMAX
        self.ATK = 100
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
    Piece_a_d = ModularBoss_destructible(Body,"sprites_boss/boss_aile_d.png","boss_a_d")
    Piece_a_g = ModularBoss_destructible(Body,"sprites_boss/boss_aile_g.png","boss_a_g")
    Piece_g = ModularBoss_destructible(Body,"sprites_boss/boss_g.png","boss_g")
    Piece_d = ModularBoss_destructible(Body,"sprites_boss/boss_d.png","boss_d")

    cooldown = P1.cooldown
    cooldown_boss = Body.cooldown

    MorceauxBoss = [Piece_g,Piece_d,Piece_a_g,Piece_a_d] 
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
                
        if Body.cooldown == 0:
            for Morceau in MorceauxBoss:
                shoot = fight.Projectile(Morceau,0,"sprites/tir2.png")
                tirs.append(shoot)
            Body.cooldown = cooldown_boss
        else:
            Body.cooldown += -1
                

        #tir automatique du joueur
        if P1.cooldown == 0:
            shoot = fight.Projectile(P1,0,"sprites/tira.png")
            tirs.append(shoot)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1

        #faire avancer les tirs
        for shoot in tirs:
            shoot.move()
            if shoot.rect.bottom > const.SCREEN_HEIGHT:
                    tirs.remove(shoot)
    
        AP3.move(3)#vitesse de déplacement des couches
        AP2.move(2)
        AP.move(1)#laisser 1 pour le fond, sinon ca file la gerbe

        ScoreBoss,alive=BossColision(tirs,P1,MorceauxBoss,explo,ScoreBoss,alive) #Colisions

        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)

        Body.draw(personnages.DISPLAYSURF)
        
        P1.souris(personnages.DISPLAYSURF)#Affichage joueur
        P1.draw_health(personnages.DISPLAYSURF)
        MB.draw(personnages.DISPLAYSURF)#Affichage menu gauche
        menu.AfficheScore(ScoreBoss) #Affichage score

        for shoot in tirs:#ici pour les animations des tirs animées
            shoot.draw(personnages.DISPLAYSURF)

        for Morceau in MorceauxBoss:
            if Morceau.PV > 0:
                Morceau.draw(personnages.DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(const.FPS)
        if not MorceauxBoss:
            alive = fight.Mort(tirs,P1,MorceauxBoss) #met fin au jeu si le boss est mort (ajouter différences par raport à si joueur meurt)
    return (ScoreBoss)

def BossColision(p_tirs,p_P1,p_morceaux,p_explo,tempscore,p_alive):
    for shoot in p_tirs:
        if shoot.team == 0:#si tir enemi
            if pygame.sprite.collide_mask(shoot,p_P1):
                p_P1.PV -= shoot.damage
                if shoot in p_tirs:
                    p_tirs.remove(shoot)
                if p_P1.PV <= 0:
                    p_alive = fight.Mort(p_tirs,p_P1,p_morceaux)
        else:    
            for morceaux in p_morceaux:
                if pygame.sprite.collide_mask(shoot,morceaux):
                    morceaux.PV -=  shoot.damage
                    if shoot in p_tirs:
                        p_explo.append(menu.explosion(shoot))
                        p_tirs.remove(shoot)
                    if morceaux.PV <= 0:
                        tempscore+=0
                        p_explo.append(menu.explosion(morceaux))
                        p_morceaux.remove(morceaux)
    for morceaux in p_morceaux:
        if pygame.sprite.collide_mask(p_P1,morceaux):
            p_P1.PV = 0
            p_alive = fight.Mort(p_tirs,p_P1,p_morceaux)
                
    return (tempscore,p_alive)

def temp(joueur, score, coord_AP3,coord_AP2,coord_AP):
    FramePerSec = pygame.time.Clock()
    ScoreBoss = score
    alive = True

    AP = menu.Arrièreplan(3)# 1 a 3 pour le fond
    AP.rect.center = coord_AP
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP2.rect.center = coord_AP2
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    AP3.rect.center = coord_AP3
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)#menu bas
    TEST = joueur
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)

    Body = ModularBoss_main_body()
    Piece_a_d = ModularBoss_destructible(Body,"sprites_boss/boss_aile_d.png","boss_a_d")
    Piece_a_g = ModularBoss_destructible(Body,"sprites_boss/boss_aile_g.png","boss_a_g")
    Piece_g = ModularBoss_destructible(Body,"sprites_boss/boss_g.png","boss_g")
    Piece_d = ModularBoss_destructible(Body,"sprites_boss/boss_d.png","boss_d")

    cooldown = TEST.cooldown
    cooldown_boss = Body.cooldown

    MorceauxBoss = [Piece_g,Piece_d,Piece_a_g,Piece_a_d] 
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
                
        if Body.cooldown == 0:
            for Morceau in MorceauxBoss:
                shoot = fight.Projectile(Morceau,0,"sprites/tir2.png")
                tirs.append(shoot)
            Body.cooldown = cooldown_boss
        else:
            Body.cooldown += -1
                

        #tir automatique du joueur
        if TEST.cooldown == 0:
            shoot = fight.Projectile(TEST,0,"sprites/tira.png")
            tirs.append(shoot)
            TEST.cooldown = cooldown
        else:
            TEST.cooldown += -1

        #faire avancer les tirs
        for shoot in tirs:
            shoot.move()
            if shoot.rect.bottom > const.SCREEN_HEIGHT:
                    tirs.remove(shoot)
    
        AP3.move(3)#vitesse de déplacement des couches
        AP2.move(2)
        AP.move(1)#laisser 1 pour le fond, sinon ca file la gerbe

        ScoreBoss,alive=BossColision(tirs,TEST,MorceauxBoss,explo,ScoreBoss,alive) #Colisions

        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)

        Body.draw(personnages.DISPLAYSURF)
        
        TEST.souris(personnages.DISPLAYSURF)#Affichage joueur
        TEST.draw_health(personnages.DISPLAYSURF)
        MB.draw(personnages.DISPLAYSURF)#Affichage menu gauche
        menu.AfficheScore(ScoreBoss) #Affichage score

        for shoot in tirs:#ici pour les animations des tirs animées
            shoot.draw(personnages.DISPLAYSURF)

        for Morceau in MorceauxBoss:
            if Morceau.PV > 0:
                Morceau.draw(personnages.DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(const.FPS)
        if not MorceauxBoss:
            return [(ScoreBoss+500),AP.rect.center,AP2.rect.center,AP3.rect.center] #L'ajout de score doit etre supérieur ou egal à la différence entre le modulo choisi et le seuil de controle
            alive = fight.Mort(tirs,P1,MorceauxBoss) #met fin au jeu si le boss est mort (ajouter différences par raport à si joueur meurt)
    return [0,AP.rect.center,AP2.rect.center,AP3.rect.cente]
