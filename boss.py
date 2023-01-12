import pygame, sys, math, pickle
from pygame.locals import *
import random, personnages, menu, bonus, fight, cinematiques
import constantes as const
from copy import deepcopy

class ModularBoss_main_body(pygame.sprite.Sprite):         #Boss modulaire
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites_boss/boss_damaged.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2,80)
        self.cooldown = 60                                 #permet de définir la cadence de tir
        self.id = "body"
        self.destination = const.SCREEN_WIDTH//2           #sert à faire des petits mouvements au boss
    
    def draw(self, surface):                 #sert à afficher le boss
        surface.blit(self.image, self.rect)
    
    def move(self):                                                     #sert à faire des petits mouvements au boss
        position = self.rect.center[0]
        if position < self.destination:
            self.rect.move_ip(1,0)
        elif position > self.destination:
            self.rect.move_ip(-1,0)                                     #le boss se déplace vers sa destination
        else:
            self.destination = random.randint(70,const.SCREEN_WIDTH-70) #lorsque la destination est atteinte, une autre est définie

class ModularBoss_destructible(pygame.sprite.Sprite):
    def __init__(self,mainbody,adresse,id):
        super().__init__()
        self.image = pygame.image.load(adresse).convert_alpha()
        self.rect = self.image.get_rect()
        self.id = id                                               #id du module
        self.PVMAX = 10000                                         #
        self.PV = self.PVMAX                                       #statistiques du module du boss
        self.ATK = 100                                             #
        self.rect.center = mainbody.rect.center
        self.mask = pygame.mask.from_surface(self.image)           #sert au colisions
    
    def draw(self, surface):                                       #affichage du module
        surface.blit(self.image, self.rect)
    
    def move(self,mainbody):                                       #permet aux modules de rester juste au dessus du corps principal
        self.rect.center = mainbody.rect.center


def BossColision(p_tirs,p_P1,p_morceaux,p_explo,tempscore,p_alive): #Colisions durant le combat contre le Boss modulaire
    for shoot in p_tirs:
        if shoot.team == 0:                                     #si un tir enemi touche le joueur
            if pygame.sprite.collide_mask(shoot,p_P1):
                p_P1.PV -= shoot.damage
                if shoot in p_tirs:
                    p_tirs.remove(shoot)
                if p_P1.PV <= 0:
                    p_alive = fight.Mort(p_tirs,p_P1,[])
        else:                                                  #si un tir alié touche le Boss
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
    for morceaux in p_morceaux:                                #si le joueur touche le boss
        if pygame.sprite.collide_mask(p_P1,morceaux):
            p_P1.PV = 0
            p_alive = fight.Mort(p_tirs,p_P1,[])
                
    return (tempscore,p_alive)

def Boss1(joueur, score,AP3,AP2,AP,VaisseauChoisis): #Boss Modulaire
    FramePerSec = pygame.time.Clock()
    ScoreBoss = score
    alive = True

    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = joueur

    coord_AP, coord_AP2, coord_AP3 = cinematiques.ArriveBoss1(P1,AP,AP2,AP3)  #cinématique d'arrivée du boss 

    AP.rect.center = coord_AP         #
    AP2.rect.center = coord_AP2       #permet de garder une continuitée dans le défillement du fond
    AP3.rect.center = coord_AP3       #

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

    backup = cooldown           #sert à la gestion des ultis 
    with open('sauvegarde.pkl', 'rb') as f:
        temp = pickle.load(f)
    if VaisseauChoisis == 1:
        Ulti = temp['V1'][7]
    elif VaisseauChoisis == 2:
        Ulti = temp['V2'][7]
    elif VaisseauChoisis == 3:
        Ulti = temp['V3'][7]

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
                
        if Body.cooldown == 0:                  #tir ennemis
            if len(MorceauxBoss)==4:            #le patern de tir dépends du nombre de morceaux encore fonctionels
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
            with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir le niveau d'amélioration
                temp = pickle.load(f)
            if VaisseauChoisis==1:                  #Permet de changer le sprite des tirs en fonction du nombre d'amélioration d'attaque
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
            if shoot.trajectoire == 10:
                shoot.suivre(P1)                               #permet au laser de suivre le vaisseau durant l'ulti
                menu.Animation(const.laserboss, shoot)         #permet d'annimer le laser de l'ulti
            if (((shoot.rect.bottom > const.SCREEN_HEIGHT) or (shoot.rect.top < 0)) and (shoot.trajectoire != 10)): #permet d'éviter que le laser ne soit supprimé avant la fin de l'ulti
                tirs.remove(shoot)                             #supprime les tirs qui sortent de l'écrant
    
        AP3.move(3)   #
        AP2.move(2)   #défilement du fond (paralax)
        AP.move(1)    #

        ScoreBoss,alive=BossColision(tirs,P1,MorceauxBoss,explo,ScoreBoss,alive) #détection des colisions


        #Affichage
        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)           #
        AP2.draw(personnages.DISPLAYSURF)          #Affichage du fond
        AP3.draw(personnages.DISPLAYSURF)          #

        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)  #Affichage des explosions animées

        Body.draw(personnages.DISPLAYSURF)         #Affichage du corps principal du boss (abimé)
        
        P1.souris(personnages.DISPLAYSURF)         #Affichage du joueur
        P1.draw_health(personnages.DISPLAYSURF)    #Affichage de la barre de vie
        if Ulti:                             #gestion des ultis:
            if P1.DureeUlti == -1:           #si l'ulti n'est pas en cours
                P1.ulti(enemies,tirs,explo)  #charge l'ulti
                pass 
            elif P1.DureeUlti > 0:           #si l'ulti est en cours
                P1.DureeUlti -= 1            #réduit son temps d'utilisation
                cooldown = P1.cooldown
            elif P1.DureeUlti == 0:          #lorsque l'ulti se termine
                for shoot in tirs:
                    if shoot.trajectoire == 10:
                        tirs.remove(shoot)  #supprime un éventuel laser de tirs  
                cooldown = backup           #réinitialise le cooldown
                P1.DureeUlti -= 1           #termine l'ulti
            P1.draw_ulti(personnages.DISPLAYSURF)  #Affichage de la barre de chargement des ultis
        
        for shoot in tirs:                         #Affiche les tirs
            shoot.draw(personnages.DISPLAYSURF)

        for Morceau in MorceauxBoss:               #Affiche les modules du Boss
            if Morceau.PV > 0:
                Morceau.draw(personnages.DISPLAYSURF)

        MB.draw(personnages.DISPLAYSURF)          #Affiche le menu en bas
        menu.AfficheScore(ScoreBoss)              #Affiche score

        pygame.display.update()
        FramePerSec.tick(const.FPS)

        if not MorceauxBoss:                      #si le boss n'a plus de modules en fonctionnement
            pos_AP,pos_AP2,pos_AP3 = cinematiques.MortBoss(P1,Body,AP,AP2,AP3)
            return [(ScoreBoss+1000),pos_AP,pos_AP2,pos_AP3]  #renvoie le score et la position des arière plans
    return [0,AP.rect.center,AP2.rect.center,AP3.rect.center] #si le joueur est mort met fin au combat

#---------------------------------------------------------------------------------------------------------------------------------------

def Boss2(joueur, score,AP3,AP2,AP,VaisseauChoisis):    #Boss Essaim
    FramePerSec = pygame.time.Clock()
    ScoreBoss = score
    alive = True
    Bossenvie = True

    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = joueur

    with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour récupérer le cooldown
        temp = pickle.load(f)
    if VaisseauChoisis==1:
        cooldown = temp['V1'][5]
    elif VaisseauChoisis==2:
        cooldown = temp['V2'][5]
    elif VaisseauChoisis==3:
        cooldown = temp['V3'][5]

    #Barre de cooldown pour la charge des sbires
    rect_capacite = pygame.Rect(0, 0, 750, 5)
    rect_capacite.midbottom = const.SCREEN_WIDTH//2, 20
    
    Cooldownchargemax=500
    Cooldowncharge=Cooldownchargemax

    backup = cooldown #sert à la gestion des ultis 
    with open('sauvegarde.pkl', 'rb') as f:
        temp = pickle.load(f)
    if VaisseauChoisis == 1:
        Ulti = temp['V1'][7]
    elif VaisseauChoisis == 2:
        Ulti = temp['V2'][7]
    elif VaisseauChoisis == 3:
        Ulti = temp['V3'][7]

    enemies = [] #Le boss sera toujours en position 0
    tirs = []
    explo = []
    boosts = []
    
    fight.SpawHistoire(enemies,-1,const.SCREEN_WIDTH//2,-200) #place le boss dans la liste
    while enemies[0].rect.bottom < const.SCREEN_HEIGHT//2-50: #cinématique d'entrée du boss
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        AP3.move(3)   #
        AP2.move(2)   #déplacement de l'arrière plan
        AP.move(1)    #
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        enemies[0].moveVitesse(0, 2)
        enemies[0].draw(personnages.DISPLAYSURF)
        P1.souris(personnages.DISPLAYSURF)
        pygame.display.update()
        FramePerSec.tick(const.FPS)

    while alive: #combat contre le Boss
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if Cooldowncharge>-1:    #Charge la capacité du Boss
            Cooldowncharge-=1
        

        
        temp = len(enemies)
        ScoreBoss,alive=fight.Colision(tirs,P1,enemies,explo,boosts,ScoreBoss,alive) #gestion des colisions et des drops
        if enemies:                                                                  #en cas de mort du joueur, enemies est vidé donc vérification
            enemies[0].PV -= (temp-len(enemies))*50                                  #les dégats sont infligés au boss


        #tir automatique du joueur
        if P1.cooldown == 0:
            with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir le nombre d'améliorations
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
        
        #tirs ennemis
        for entity in enemies:
            p = random.randint(0,200)
            if p < 1:
                if (entity.id == "s1"):
                    shoot = fight.Projectile(entity,3,"sprites_animation/boule1.png")
                    tirs.append(shoot)
                elif (entity.id == "s2"):
                    shoot = fight.Projectile(entity,2,"sprites/tir3.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(entity,1,"sprites/tir3.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(entity,0,"sprites/tir3.png")
                    tirs.append(shoot)
            if entity.rect.top > const.SCREEN_HEIGHT:
                    enemies.remove(entity)

        #faire avancer les tirs
        for shoot in tirs:
            shoot.move()
            if shoot.trajectoire == 10:
                shoot.suivre(P1)                               #permet au laser de suivre le vaisseau durant l'ulti
                menu.Animation(const.laserboss, shoot)         #permet d'annimer le laser de l'ulti
            if (((shoot.rect.bottom > const.SCREEN_HEIGHT) or (shoot.rect.top < 0)) and (shoot.trajectoire != 10)): #permet d'éviter que le laser ne soit supprimé avant la fin de l'ulti
                tirs.remove(shoot)                             #supprime les tirs qui sortent de l'écrant
    
        AP3.move(3)   #
        AP2.move(2)   #défilement de l'arrière plan
        AP.move(1)    #

        #Affichage des bonus
        for boost in boosts:
            boost.draw(personnages.DISPLAYSURF)

        #Affichage des explosions
        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)

        if len(enemies)==1 and Bossenvie:
            if enemies[0].id=='b2':
                Cooldowncharge=Cooldownchargemax
                MouvementFormation=True
                Nbadversaire=random.randint(5,30) #Nombre d'adversaire qui apparait
                if enemies[0].PV > enemies[0].MAXPV//2:
                    for i in range (0,Nbadversaire,1):
                        fight.SpawHistoire(enemies,-2,random.randint(0,const.SCREEN_WIDTH),random.randint(-400,-50))
                else:
                    for i in range (0,Nbadversaire,1):
                        fight.SpawHistoire(enemies,random.randint(-3,-2),random.randint(0,const.SCREEN_WIDTH),random.randint(-400,-50))
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
        if Cooldowncharge<0:
            for Vaisseau in enemies:
                if Vaisseau.id=='b2':
                    pass
                else:
                    Vaisseau.moveVitesse(0,6)


        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        #Afficher les ennemis
        for Vaisseau in enemies:
            Vaisseau.draw(personnages.DISPLAYSURF)

        #Affichage des barres stats du boss
        if enemies:
            enemies[0].draw_health(personnages.DISPLAYSURF)
            menu.draw_health_bar(personnages.DISPLAYSURF, rect_capacite.bottomleft, rect_capacite.size, (0, 0, 0), (206, 206, 206), (0, 128, 255), Cooldowncharge/Cooldownchargemax)

        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)
        
        P1.souris(personnages.DISPLAYSURF)#Affichage joueur
        P1.draw_health(personnages.DISPLAYSURF)
        if Ulti: #gestion des ultis
            if P1.DureeUlti == -1:
                P1.ulti(enemies,tirs,explo,ScoreBoss)
            elif P1.DureeUlti > 0:
                P1.DureeUlti -= 1
                cooldown = P1.cooldown
            elif P1.DureeUlti == 0:
                for shoot in tirs:
                    if shoot.trajectoire == 10:
                        tirs.remove(shoot)
                cooldown = backup
                P1.DureeUlti -= 1
            P1.draw_ulti(personnages.DISPLAYSURF)
        
        #Affichage/Animation des tirs
        for shoot in tirs:
            if shoot.trajectoire == 3 and shoot.tireur_id == "e1" or shoot.tireur_id == "e5":
                menu.Animation(const.boules,shoot)
            shoot.draw(personnages.DISPLAYSURF)

        MB.draw(personnages.DISPLAYSURF)#Affichage menu gauche
        menu.AfficheScore(ScoreBoss) #Affichage score

        pygame.display.update()
        FramePerSec.tick(const.FPS)
        if enemies:
            if enemies[0].PV <0:
                enemies[0].moveVitesse(0, -2)
                Bossenvie = False
        if len(enemies)==1 and Bossenvie==False:
            return alive,ScoreBoss
    return alive,ScoreBoss
