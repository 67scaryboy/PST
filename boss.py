import pygame, sys, math, pickle
from pygame.locals import *
import random, personnages, menu, bonus, fight, cinematiques
import constantes as const
from copy import deepcopy

class ModularBoss_main_body(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites_boss/boss_damaged.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2,80)
        self.cooldown = 60
        self.id = "body"
        self.destination = const.SCREEN_WIDTH//2
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def move(self):
        position = self.rect.center[0]
        if position < self.destination:
            self.rect.move_ip(1,0)
        elif position > self.destination:
            self.rect.move_ip(-1,0)
        else:
            self.destination = random.randint(70,const.SCREEN_WIDTH-70)

class ModularBoss_destructible(pygame.sprite.Sprite):
    def __init__(self,mainbody,adresse,id):
        super().__init__()
        self.image = pygame.image.load(adresse).convert_alpha()
        self.rect = self.image.get_rect()
        self.id = id
        self.PVMAX = 10000
        self.PV = self.PVMAX
        self.ATK = 100
        self.rect.center = mainbody.rect.center
        self.mask = pygame.mask.from_surface(self.image)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def move(self,mainbody):
        self.rect.center = mainbody.rect.center


def BossColision(p_tirs,p_P1,p_morceaux,p_explo,tempscore,p_alive):
    for shoot in p_tirs:
        if shoot.team == 0:#si tir enemi
            if pygame.sprite.collide_mask(shoot,p_P1):
                p_P1.PV -= shoot.damage
                if shoot in p_tirs:
                    p_tirs.remove(shoot)
                if p_P1.PV <= 0:
                    p_alive = fight.Mort(p_tirs,p_P1,[])
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
            p_alive = fight.Mort(p_tirs,p_P1,[])
                
    return (tempscore,p_alive)

def Boss1(joueur, score,AP3,AP2,AP,VaisseauChoisis):
    FramePerSec = pygame.time.Clock()
    ScoreBoss = score
    alive = True

    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)#menu bas
    P1 = joueur
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)

    coord_AP, coord_AP2, coord_AP3 = cinematiques.ArriveBoss1(P1,AP,AP2,AP3)

    AP.rect.center = coord_AP
    AP2.rect.center = coord_AP2
    AP3.rect.center = coord_AP3

    Body = ModularBoss_main_body()
    Piece_a_d = ModularBoss_destructible(Body,"sprites_boss/boss_aile_d.png","boss_a_d")
    Piece_a_g = ModularBoss_destructible(Body,"sprites_boss/boss_aile_g.png","boss_a_g")
    Piece_g = ModularBoss_destructible(Body,"sprites_boss/boss_g.png","boss_g")
    Piece_d = ModularBoss_destructible(Body,"sprites_boss/boss_d.png","boss_d")

    with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour récupérer le cooldown
        temp = pickle.load(f)
    if VaisseauChoisis==1:
        cooldown = temp['V1'][5]
    elif VaisseauChoisis==2:
        cooldown = temp['V2'][5]
    elif VaisseauChoisis==3:
        cooldown = temp['V3'][5]
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
            if len(MorceauxBoss)==4:
                for Morceau in MorceauxBoss:
                    shoot = fight.Projectile(Morceau,0,"sprites/tir2.png")
                    tirs.append(shoot)
                Body.cooldown = cooldown_boss
            elif len(MorceauxBoss)==3:
                for Morceau in MorceauxBoss:
                    shoot = fight.Projectile(Morceau,0,"sprites/tir2.png")
                    tirs.append(shoot)
                Body.cooldown = cooldown_boss//2
            elif len(MorceauxBoss)==2:
                for Morceau in MorceauxBoss:
                    shoot = fight.Projectile(Morceau,0,"sprites/tir2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(Morceau,4,"sprites_animation/boule1.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(Morceau,5,"sprites_animation/boule1.png")
                    tirs.append(shoot)
                Body.cooldown = cooldown_boss
            else:
                for Morceau in MorceauxBoss:
                    shoot = fight.Projectile(Morceau,0,"sprites/tir2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(Morceau,4,"sprites_animation/boule1.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(Morceau,5,"sprites_animation/boule1.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(Morceau,1,"sprites/tir2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(Morceau,2,"sprites/tir2.png")
                    tirs.append(shoot)
                Body.cooldown = cooldown_boss

        else:
            Body.cooldown += -1
                

        #tir automatique du joueur
        if P1.cooldown == 0:
            with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir si on à débloqué ou pas les vaisseaux
                temp = pickle.load(f)
            if VaisseauChoisis==1: #Permet de changer le sprite des tirs en fonction du nombre d'amélioration d'attaque
                if temp['V1'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira.png")
                    
                elif temp['V1'][4]==1:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    
                elif temp['V1'][4]==2:
                    shoot = fight.Projectile(P1,0,"sprites/tira3.png")
                    
            elif VaisseauChoisis==2: 
                if temp['V2'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    
                elif temp['V2'][4]==1:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
                elif temp['V2'][4]==2:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
            elif VaisseauChoisis==3:
                if temp['V3'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
                elif temp['V3'][4]==1:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
                elif temp['V3'][4]==2:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,8,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,9,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.right
            tirs.append(shoot)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1

        #faire avancer les tirs
        for shoot in tirs:
            shoot.move()
            if ((shoot.rect.bottom > const.SCREEN_HEIGHT) or (shoot.rect.top < 0)):
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
        
        for shoot in tirs:#ici pour les animations des tirs animées
            shoot.draw(personnages.DISPLAYSURF)

        for Morceau in MorceauxBoss:
            if Morceau.PV > 0:
                Morceau.draw(personnages.DISPLAYSURF)

        MB.draw(personnages.DISPLAYSURF)#Affichage menu gauche
        menu.AfficheScore(ScoreBoss) #Affichage score

        pygame.display.update()
        FramePerSec.tick(const.FPS)

        if not MorceauxBoss:
            pos_AP,pos_AP2,pos_AP3 = cinematiques.MortBoss(P1,Body,AP,AP2,AP3)
            return [(ScoreBoss+1000),pos_AP,pos_AP2,pos_AP3] #L'ajout de score doit etre supérieur ou egal à la différence entre le modulo choisi et le seuil de controle
    return [0,AP.rect.center,AP2.rect.center,AP3.rect.center] #si le joueur est mort met fin au jeu

def Boss2(joueur, score,AP3,AP2,AP,VaisseauChoisis):
    FramePerSec = pygame.time.Clock()
    ScoreBoss = score
    alive = True

    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)#menu bas
    P1 = joueur
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)

    with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour récupérer le cooldown
        temp = pickle.load(f)
    if VaisseauChoisis==1:
        cooldown = temp['V1'][5]
    elif VaisseauChoisis==2:
        cooldown = temp['V2'][5]
    elif VaisseauChoisis==3:
        cooldown = temp['V3'][5]

    enemies = [] #Le boss sera toujours en position 0
    tirs = []
    explo = []
    boosts = []
    
    fight.SpawHistoire(enemies,-1,const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT//2-100)

    while alive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # Gestion collision tirs
        score,alive=fight.Colision(tirs,P1,enemies,explo,boosts,score,alive)
        
        #tir automatique du joueur
        if P1.cooldown == 0:
            with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir si on à débloqué ou pas les vaisseaux
                temp = pickle.load(f)
            if VaisseauChoisis==1: #Permet de changer le sprite des tirs en fonction du nombre d'amélioration d'attaque
                if temp['V1'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira.png")
                    
                elif temp['V1'][4]==1:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    
                elif temp['V1'][4]==2:
                    shoot = fight.Projectile(P1,0,"sprites/tira3.png")
                    
            elif VaisseauChoisis==2: 
                if temp['V2'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    
                elif temp['V2'][4]==1:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
                elif temp['V2'][4]==2:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
            elif VaisseauChoisis==3:
                if temp['V3'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
                elif temp['V3'][4]==1:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
                elif temp['V3'][4]==2:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,8,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,9,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.right
            tirs.append(shoot)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1

        for entity in enemies:
            p = random.randint(0,300)
            if p < 1:
                if (entity.id == "b2"):
                    pass
                    shoot = fight.Projectile(entity,2,"sprites/tir3.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(entity,1,"sprites/tir3.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(entity,0,"sprites/tir3.png")
                elif (entity.id == "s1"):
                    shoot = fight.Projectile(entity,3,"sprites_animation/boule1.png")
                tirs.append(shoot)
            if entity.rect.top > const.SCREEN_HEIGHT:
                    enemies.remove(entity)

        #faire avancer les tirs
        for shoot in tirs:
            shoot.move()
            if ((shoot.rect.bottom > const.SCREEN_HEIGHT) or (shoot.rect.top < 0)):
                tirs.remove(shoot)
    
        AP3.move(3)#vitesse de déplacement des couches
        AP2.move(2)
        AP.move(1)#laisser 1 pour le fond, sinon ca file la gerbe

        #Affichage des bonus
        for boost in boosts:
            boost.draw(personnages.DISPLAYSURF)

        #Affichage des explosions
        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)

        if len(enemies)==1:
            if enemies[0].id=='b2':
                MouvementFormation=True
                Nbadversaire=random.randint(5,20) #Nombre d'adversaire qui apparait
                for i in range (0,Nbadversaire,1):
                    fight.SpawHistoire(enemies,-2,random.randint(0,const.SCREEN_WIDTH),random.randint(-400,-50))
                pass
        if MouvementFormation==True:
            Coordbasse=-200
            for Vaisseau in enemies:
                if Vaisseau.id == 'b2':
                    pass
                elif Vaisseau.rect.bottom > Coordbasse:
                    Coordbasse=Vaisseau.rect.bottom
            for Vaisseau in enemies:
                if Vaisseau.id=='b2':
                    pass
                elif Coordbasse<250:
                    Vaisseau.moveVitesse(0,6)
                elif Coordbasse<300:
                    Vaisseau.moveVitesse(0,5)
                elif Coordbasse<350:
                    Vaisseau.moveVitesse(0,4)
                elif Coordbasse<400:
                    Vaisseau.moveVitesse(0,2)
                elif Coordbasse<450:
                    Vaisseau.moveVitesse(0,1)
            if Coordbasse>449:
                MouvementFormation=False

        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        #Afficher les ennemis
        for Vaisseau in enemies:
            Vaisseau.draw(personnages.DISPLAYSURF)

        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)
        
        P1.souris(personnages.DISPLAYSURF)#Affichage joueur
        P1.draw_health(personnages.DISPLAYSURF)
        
        #Affichage/Animation des tirs
        for shoot in tirs:
            if shoot.trajectoire == 3 and shoot.tireur_id == "e1" or shoot.tireur_id == "e5":
                menu.Animation(const.boules,shoot)
            shoot.draw(personnages.DISPLAYSURF)

        MB.draw(personnages.DISPLAYSURF)#Affichage menu gauche
        menu.AfficheScore(ScoreBoss) #Affichage score

        pygame.display.update()
        FramePerSec.tick(const.FPS)
    
    return 
