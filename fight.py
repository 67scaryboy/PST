import pygame, sys, math, boss
from pygame.locals import *
import random, personnages, menu, bonus
import constantes as const
import pickle, os

def Spawn(enemies,q): #donne une propabilité d'apparition pour le mode arcade
    p = random.randint(0,100)
    if p < q:
        p2 = random.randint(1,3)
        if p2 == 1:
            enemy  = personnages.Enemy(1)
        elif p2 == 2:
            enemy  = personnages.Enemy(2)
        elif p2 == 3:
            enemy  = personnages.Enemy(3)
        enemies.append(enemy)

def SpawHistoire(listeennemis,idennemis,posX,posY):#Faire spawn un ennemis précis pour le mode histoire.
    enemy  = personnages.Enemy(idennemis)
    enemy.rect.center=(posX,posY)
    listeennemis.append(enemy)

def Arcade(): #Mode Arcade
    FramePerSec = pygame.time.Clock()
    scoreArcade = 0
    alive = True
    niveau=0
    VaisseauChoisis = menu.ChoixPerso()
    font = pygame.font.Font('freesansbold.ttf', 32)

    AP = menu.Arrièreplan(3) #
    AP2= menu.Arrièreplan(5) #Arrière plan
    AP3= menu.Arrièreplan(6) #
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(VaisseauChoisis)
    E1 = personnages.Enemy(1)
    CP = personnages.Compagon(P1)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200) #Positionement du joueur

    cooldown = P1.cooldown  #sert à réinitialiser le cooldown après chaque tir
    backup = cooldown       #sert à réinitialiser le cooldown après utilisation de l'ulti
    with open('sauvegarde.pkl', 'rb') as f: #verification des ultis débloqués 
        temp = pickle.load(f)
    if VaisseauChoisis == 1:
        Ulti = temp['V1'][7]
    elif VaisseauChoisis == 2:
        Ulti = temp['V2'][7]
    elif VaisseauChoisis == 3:
        Ulti = temp['V3'][7]

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

        CP.update(P1)  #oscillations du compagnon

        #mouvements ennemis
        for entity in enemies:
            if entity.active == 1:
                for i in range (0,niveau+1,1): #Accélération des ennemis en fonction du nombre de boss battus
                    entity.move()
                    entity.moveKamikaze(P1)
                #ici pour décider si il tire
                p = random.randint(0,100)
                if p < 1:
                    if (entity.id == "e1"):
                        shoot = Projectile(entity,3,"sprites_animation/boule1.png")
                    elif (entity.id == "e2"):
                        shoot = Projectile(entity,2,"sprites/tir3.png")
                        tirs.append(shoot)
                        shoot = Projectile(entity,1,"sprites/tir3.png")
                        tirs.append(shoot)
                        shoot = Projectile(entity,0,"sprites/tir3.png")
                    else:
                        shoot = Projectile(entity,0,"sprites/tir.png")
                    tirs.append(shoot)
                #supprimer les enemis qui sortent de l'écrant
                if entity.rect.top > const.SCREEN_HEIGHT:
                    enemies.remove(entity)

        #tir automatique
        if P1.cooldown == 0:
            with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir le niveau d'amélioration des tirs
                temp = pickle.load(f)
            if VaisseauChoisis==1: #Permet de changer le sprite des tirs en fonction du nombre d'amélioration d'attaque
                if temp['V1'][4]==0:
                    shoot = Projectile(P1,0,"sprites/tira.png")
                    shootf= Projectile(CP,0,"sprites/tira.png")
                elif temp['V1'][4]==1:
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shootf= Projectile(CP,0,"sprites/tira2.png")
                elif temp['V1'][4]==2:
                    shoot = Projectile(P1,0,"sprites/tira3.png")
                    shootf= Projectile(CP,0,"sprites/tira3.png")
            elif VaisseauChoisis==2: 
                if temp['V2'][4]==0:
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shootf= Projectile(CP,0,"sprites/tira2.png")
                elif temp['V2'][4]==1:
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    shootf= Projectile(CP,0,"sprites/tira2.png")
                elif temp['V2'][4]==2:
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    shootf= Projectile(CP,0,"sprites/tira2.png")
            elif VaisseauChoisis==3:
                if temp['V3'][4]==0:
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    shootf= Projectile(CP,0,"sprites/tira2.png")
                elif temp['V3'][4]==1:
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    shootf= Projectile(CP,0,"sprites/tira2.png")
                elif temp['V3'][4]==2:
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = Projectile(P1,6,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = Projectile(P1,7,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    shootf= Projectile(CP,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = Projectile(P1,8,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = Projectile(P1,9,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.right
            tirs.append(shoot)
            tirs.append(shootf)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1

        #faire avancer les tirs
        for shoot in tirs:
            for i in range (0,niveau+1,1):    #Les tirs plus rapides en fonction du nombre de boss battus
                shoot.move()
                if shoot.trajectoire == 10:
                    shoot.suivre(P1)                          #Le laser de l'ulti suis le joueur
                    menu.Animation(const.laserboss, shoot)    #et est animé 
            if (((shoot.rect.bottom > const.SCREEN_HEIGHT) or (shoot.rect.top < 0)) and (shoot.trajectoire != 10)): #empèche le laser de disparaitre avant la fin de l'ulti
                    tirs.remove(shoot) #supprime les tirs qui sortent de l'écrant
        
        #fait avancer les boosters
        for boost in boosts:
            boost.move()
            if boost.rect.bottom > const.SCREEN_HEIGHT:
                    boosts.remove(boost) #supprime les boosters qui sortent de l'écrant
    
        AP3.move(3) #
        AP2.move(2) #défillement du fond
        AP.move(1)  #

        scoreArcade,alive=Colision(tirs,P1,enemies,explo,boosts,scoreArcade,alive) #gestion des colisions

        bonus.AttraperBoost(boosts,P1) #gestion de la colision bonus-joueur

        if scoreArcade%11000<10000: #Verification du score (utile pour le spawn du boss de temps en temps) | 2000 correspond au modulo choisi et 1500 au seuil de controle
            #ATTENTION: Avant de modifier les valeurs au dessus, aller voir la fonction qui fait spawn le boss
            Spawn(enemies,2) #Apparition aléatoire d'adversaires.
        else:
            if len(enemies)==0:                                               #Si la limite de score a été atteinte et qu'il y a plus d'adversaires sur le terrain
                temp = boss.Boss1(P1,scoreArcade,AP3,AP2,AP,VaisseauChoisis)  #Lancer le combat de boss n°1
                AP.rect.center = temp[1]  #
                AP2.rect.center = temp[2] #Assure la continuité du fond
                AP3.rect.center = temp[3] #
                if temp[0]==0: #le joueur est mort
                    break
                else:
                    scoreArcade=temp[0] #le joueur à gagné le combat de boss
                    niveau+=1           #la difficultée augmente

        #Affichage
        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)  #
        AP2.draw(personnages.DISPLAYSURF) #Affichage du fond
        AP3.draw(personnages.DISPLAYSURF) #
        
        for shoot in tirs: #Affichage des tirs
            if shoot.trajectoire == 3 and shoot.tireur_id == "e1":
                menu.Animation(const.boules,shoot) #Animation des tirs
            shoot.draw(personnages.DISPLAYSURF)
        
        for boost in boosts: #Affichage des boosts
            boost.draw(personnages.DISPLAYSURF)

        menu.aff_explo(explo) #Affichge des explosions
        for boom in explo:
            menu.Animation(const.explosions,boom) #Animation des explosions

        for entity in enemies: #Affichage des enemis
            if entity.active == 1:
                entity.draw(personnages.DISPLAYSURF)
        P1.souris(personnages.DISPLAYSURF) #Affichage joueur
        P1.draw_health(personnages.DISPLAYSURF)

        if Ulti: #gestion des ultis
            if P1.DureeUlti == -1:                    #si l'ulti n'est pas en cours
                P1.ulti(enemies,tirs,explo,score)       #chargement de l'ulti
            elif P1.DureeUlti > 0:                    #si l'ulti est en cours
                P1.DureeUlti -= 1                       #reduit son temps d'utilisation
                cooldown = P1.cooldown                  #change le cooldown de tir
            elif P1.DureeUlti == 0:                   #si l'ulti se termine
                for shoot in tirs:                    #supprime un éventuel laser
                    if shoot.trajectoire == 10:
                        tirs.remove(shoot)            
                cooldown = backup                     #réinitialise le cooldown de tir
                P1.DureeUlti -= 1                     #termine l'ulti
            P1.draw_ulti(personnages.DISPLAYSURF)                        

        CP.draw(personnages.DISPLAYSURF) #Affichage Compagnon
        MB.draw(personnages.DISPLAYSURF) #Affichage menu gauche
        menu.AfficheScore(scoreArcade)   #Affichage score
        texte=font.render("Niveau: "+str(niveau), True, const.GREEN)
        texterect=texte.get_rect()
        texterect.center=(const.SCREEN_WIDTH-200,const.SCREEN_HEIGHT-12)
        personnages.DISPLAYSURF.blit(texte,texterect)


        pygame.display.update()
        FramePerSec.tick(const.FPS)
    
    if os.path.exists('topscorearcade.pkl'): #Calcul des meilleurs scores
        #Si le fichier existe
        with open('topscorearcade.pkl', 'rb') as f:
            temp = pickle.load(f)
            for i in range (1,6,1):
                if temp[i]<scoreArcade and i<5: #si le score est suffisement élevé pour être sur le leader board, l'ajoute
                    for a in range(5,i,-1):
                        temp[a]=temp[a-1]
                    temp[i]=scoreArcade 
                    break
                elif temp[i]<scoreArcade:
                    temp[i]=scoreArcade
        with open('topscorearcade.pkl', 'wb') as f:
            pickle.dump(temp, f)       
    else:
        #S'il n'existe pas (donc qu'il a été suprimé)
        topscore = {1: scoreArcade,
        2: 0,
        3: 0,
        4: 0,
        5:0}
        with open('topscorearcade.pkl', 'wb') as f:
            pickle.dump(topscore, f)  #créé le nouveau fichier

    menu.MenuFinPartieArcade(scoreArcade)
    return (scoreArcade)


class Projectile(pygame.sprite.Sprite):          #les tirs et le laser
      def __init__(self, tireur,traj,adresse):
        super().__init__()
        self.tireur_id = tireur.id                              #Affiche differents tir en fonction de l'id tireur (e=ennemis, p=player, c=compagnon)
        self.damage = tireur.ATK                                #Les dégats du tir
        self.image = pygame.image.load(adresse).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = tireur.rect.center                   #Se place à la position du vaisseau qui tire
        if tireur.id in ['e1','e2','e3','e5','b2','s1','s2']:   
            self.direction = [0,4]                              #déplacement de base d'un projectile
            self.team = 0                                       #0 pour les tirs ennemis et 1 pour les aliés
            
        elif tireur.id in ['p1','p2','p3','c1']:
            self.direction = [0,-10] #A modifier pour modifier la vitesse des tirs "normaux"
            self.team = 1
            
        elif tireur.id in ['boss_g', 'boss_d', 'boss_a_g', 'boss_a_d']:
            self.direction = [0,4]
            self.team = 0
            if tireur.id == 'boss_g':
                self.rect.center = (self.rect.center[0]-35,self.rect.center[1]) #décale les tirs puisque les morceaux font techniquement la même taille que le corp principal  
            elif tireur.id == 'boss_d':
                self.rect.center = (self.rect.center[0]+35,self.rect.center[1])
            elif tireur.id == 'boss_a_g':
                self.rect.center = (self.rect.center[0]-140,self.rect.center[1])
            elif tireur.id == 'boss_a_d':
                self.rect.center = (self.rect.center[0]+140,self.rect.center[1])

        self.trajectoire = traj                                 #permet de paramettrer des trajectoires (10 est réservé pour le laser)
        if traj == 10:
            self.direction = [0,0]                              #le laser ne bouge pas avec "move", mais avec "suivre"

        self.time = 0                                           #permet de modifier la trajectoire en fonction du temps
        self.mask = pygame.mask.from_surface(self.image)        #sert aux colisions

      def suivre(self,joueur): #Permet au laser de suivre le joueur
        self.rect.center = (joueur.rect.center[0],joueur.rect.center[1]-250)

      def move(self): #fait avancer les tirs
        self.rect.move_ip(self.direction[0],self.direction[1])            #fait avancer les tirs

        if self.trajectoire == 1:#logarithme droite                       #en fonction de la trajectoire définie du tir, défini le prochain mouvement 
            temp = 2*(math.log(self.time+81/2)-math.log(self.time+1/2))
            self.direction = [temp,math.sqrt(9-temp)+2]
        elif self.trajectoire == 2:#logarithme gauche
            temp = 2*(math.log(self.time+81/2)-math.log(self.time+1/2))
            self.direction = [-temp,math.sqrt(9-temp)+2]
        elif self.trajectoire == 3:#cosinus
            temp = 3* math.cos(self.time/20)
            self.direction = [temp,math.sqrt(9-temp*temp)+2]
        elif self.trajectoire == 4:#diagonale droite
            self.direction = [2,4]
        elif self.trajectoire == 5:#diagonale gauche
            self.direction = [-2,4]
        elif self.trajectoire == 6:#diagonale droite JOUEUR
            self.direction = [1,-10]
        elif self.trajectoire == 7:#diagonale gauche JOUEUR
            self.direction = [-1,-10]
        elif self.trajectoire == 8:#logarithme gauche JOUEUR
            temp = 2*(math.log(self.time+81/2)-math.log(self.time+1/2))
            self.direction = [-temp,math.sqrt(9-temp)-12]
        elif self.trajectoire == 9:#logarithme droite JOUEUR
            temp = 2*(math.log(self.time+81/2)-math.log(self.time+1/2))
            self.direction = [+temp,math.sqrt(9-temp)-12]
        self.time += 1

      def draw(self, surface): #Affichage du projectile
        surface.blit(self.image, self.rect)

def Colision(p_tirs,p_P1,p_enemies,p_explo,boosts,tempscore,p_alive):  #Detection des colisions
    for shoot in p_tirs:
        if shoot.team == 0:                                                      #si un tir ennemi
            if pygame.sprite.collide_rect(shoot,p_P1):                              #est proche du joueur
                if pygame.sprite.collide_mask(shoot,p_P1):                          #au point de le toucher
                    p_P1.PV -= shoot.damage                                         #le joueur subit des dégats
                    if shoot in p_tirs:
                        p_tirs.remove(shoot)                                        #le tir est supprimé
                    if p_P1.PV <= 0:                                                #si les dégats ont réduit les PV du joueur à 0
                        p_alive = Mort(p_tirs,p_P1,p_enemies)                       #celui ci n'est plus en vie
        else:                                                                    #si un tir alié
            for enemy in p_enemies:
                if pygame.sprite.collide_rect(shoot,enemy) and enemy.id != 'b2':    #est proche d'un ennemi 
                    if pygame.sprite.collide_mask(shoot,enemy):                     #au point de le toucher
                        enemy.PV -=  shoot.damage                                   #l'ennemi subit des dégats
                        if shoot in p_tirs and shoot.trajectoire != 10:             #et si il ne s'agit pas du laser
                            p_tirs.remove(shoot)                                    #le tir est supprimé
                        if enemy.PV <= 0:                                           #si les dégats on réduit les PV de l'ennemi à 0
                            tempscore+=enemy.score                                  #le joueur gagne des points
                            p_explo.append(menu.explosion(enemy))                   #une explosion se produit
                            bonus.dropBooster(boosts,enemy)                         #il y a une chance de faire tomber un bonus
                            p_enemies.remove(enemy)                                 #et l'ennemi est supprimé
    for enemy in p_enemies:                                                     #si un ennemi
        if pygame.sprite.collide_rect(p_P1, enemy) and enemy.id != 'b2':            #est proche du joueur
            if pygame.sprite.collide_mask(p_P1,enemy):                              #au point de le toucher 
                p_P1.PV -= enemy.ATK                                                #le joueur subit des dégats
                tempscore+=enemy.score                                              #le joueur gagne des points
                p_explo.append(menu.explosion(enemy))                               #une explosion se produit
                bonus.dropBooster(boosts,enemy)                                     #il y a une chance de faire tomber un bonus
                p_enemies.remove(enemy)                                             #l'ennemi est détruit
                if p_P1.PV <= 0:                                                    #si les dégats ont réduit les PV du joueur à 0
                    p_alive = Mort(p_tirs,p_P1,p_enemies)                           #celui si n'est plus en vie
                
    return (tempscore,p_alive)                                                 #le nouveau score et la situation du joueur est communiquée
    
def Mort(p_tirs,p_P1,p_enemies): #Lorsque le joueur est mort
    p_tirs.clear()    #on vide les fonctions
    p_enemies.clear()
    return False #fin de la boucle while alive