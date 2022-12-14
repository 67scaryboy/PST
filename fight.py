import pygame, sys, math, boss
from pygame.locals import *
import random, personnages, menu, bonus
import constantes as const
import pickle, os

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

def SpawHistoire(listeennemis,idennemis,posX,posY):#Faire spawn un ennemis précis à certaine coordonnés.
    enemy  = personnages.Enemy(idennemis)
    enemy.rect.center=(posX,posY)
    listeennemis.append(enemy)

def Arcade():
    FramePerSec = pygame.time.Clock()
    scoreArcade = 0
    alive = True
    niveau=0
    VaisseauChoisis = menu.ChoixPerso()
    font = pygame.font.Font('freesansbold.ttf', 32)

    AP = menu.Arrièreplan(3)# 1 a 3 pour le fond
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(VaisseauChoisis)
    E1 = personnages.Enemy(1)
    CP = personnages.Compagon(P1)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)

    cooldown = P1.cooldown
    backup = cooldown

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
            with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir si on à débloqué ou pas les vaisseaux
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
        
        #gestion des ultis
        if P1.DureeUlti == -1:
            P1.ulti(enemies,tirs,explo)
        elif P1.DureeUlti > 0:
            P1.DureeUlti -= 1
            cooldown = P1.cooldown
        elif P1.DureeUlti == 0:
            for shoot in tirs:
                if shoot.trajectoire == 10:
                    tirs.remove(shoot)
            cooldown = backup
            P1.DureeUlti -= 1



        #faire avance les tirs
        for shoot in tirs:
            for i in range (0,niveau+1,1):#Tirs plus rapides en fonction du nombre de boss battus
                shoot.move()
                if shoot.trajectoire == 10:
                    shoot.suivre(P1)
            if (((shoot.rect.bottom > const.SCREEN_HEIGHT) or (shoot.rect.top < 0)) and (shoot.trajectoire != 10)):
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

        if scoreArcade%11000<10000: #Verification du score (utile pour le spawn du boss de temps en temps) | 2000 correspond au modulo choisi et 1500 au seuil de controle
            #ATTENTION: Avant de modifier les valeurs au dessus, aller voir la fonction qui fait spawn le boss
            Spawn(enemies,2) #Apparition aléatoire d'adversaires.
        else:
            if len(enemies)==0: #Si la limite de score a été atteinte et qu'il y a plus d'adversaires sur le terrain
                temp = boss.temp(P1,scoreArcade,AP3,AP2,AP,VaisseauChoisis)
                AP.rect.center = temp[1]
                AP2.rect.center = temp[2]
                AP3.rect.center = temp[3]
                if temp[0]==0:
                    break
                else:
                    scoreArcade=temp[0]
                    niveau+=1

        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        
        for shoot in tirs:
            if shoot.trajectoire == 3 and shoot.tireur_id == "e1":
                menu.Animation(const.boules,shoot)
            shoot.draw(personnages.DISPLAYSURF)
            if shoot.trajectoire == 10:
                menu.Animation(const.laserboss, shoot)
        
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
        P1.draw_ulti(personnages.DISPLAYSURF)
        CP.draw(personnages.DISPLAYSURF)#Affichage Compagnon
        MB.draw(personnages.DISPLAYSURF)#Affichage menu gauche
        menu.AfficheScore(scoreArcade) #Affichage score
        texte=font.render("Niveau: "+str(niveau), True, const.GREEN)
        texterect=texte.get_rect()
        texterect.center=(const.SCREEN_WIDTH-200,const.SCREEN_HEIGHT-12)
        personnages.DISPLAYSURF.blit(texte,texterect)


        pygame.display.update()
        FramePerSec.tick(const.FPS)
    
    if os.path.exists('topscorearcade.pkl'): #Calcul des meilleurs scores
        # Do something if the file exists
        with open('topscorearcade.pkl', 'rb') as f:
            temp = pickle.load(f)
            for i in range (1,6,1):
                if temp[i]<scoreArcade and i<5:
                    for a in range(5,i,-1):
                        temp[a]=temp[a-1]
                    temp[i]=scoreArcade 
                    break
                elif temp[i]<scoreArcade:
                    temp[i]=scoreArcade
        with open('topscorearcade.pkl', 'wb') as f:
            pickle.dump(temp, f)       
    else:
        # Do something if the file does not exist
        topscore = {1: scoreArcade,
        2: 0,
        3: 0,
        4: 0,
        5:0}
        with open('topscorearcade.pkl', 'wb') as f:
            pickle.dump(topscore, f)  

    menu.MenuFinPartieArcade(scoreArcade)
    return (scoreArcade)


class Projectile(pygame.sprite.Sprite):
      def __init__(self, tireur,traj,adresse):
        super().__init__()
        self.tireur_id = tireur.id
        self.damage = tireur.ATK
        self.image = pygame.image.load(adresse).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = tireur.rect.center
        if tireur.id in ['e1','e2','e3','e5']: #Affiche differents tir en fonction de l'id tireur (e=ennemis, p=player, c=compagnon)
            self.direction = [0,4]  #Vitesse de déplacement horizontale et verticale
            self.team = 0# 0 pour les tirs enemis et 1 pour les aliés
            
        elif tireur.id in ['p1','p2','p3','c1']:
            self.direction = [0,-10] #A modifier pour modifier la vitesse des tirs "normaux"
            self.team = 1
            
        elif tireur.id in ['boss_g', 'boss_d', 'boss_a_g', 'boss_a_d']:
            self.direction = [0,4]
            self.team = 0
            if tireur.id == 'boss_g':
                self.rect.center = (self.rect.center[0]-35,self.rect.center[1])
            elif tireur.id == 'boss_d':
                self.rect.center = (self.rect.center[0]+35,self.rect.center[1])
            elif tireur.id == 'boss_a_g':
                self.rect.center = (self.rect.center[0]-140,self.rect.center[1])
            elif tireur.id == 'boss_a_d':
                self.rect.center = (self.rect.center[0]+140,self.rect.center[1])

        self.trajectoire = traj # 10 pour laser
        if traj == 10:
            self.direction = [0,0]

        self.time = 0
        self.mask = pygame.mask.from_surface(self.image)

      def suivre(self,joueur):
        self.rect.center = (joueur.rect.center[0],joueur.rect.center[1]-250)

      def move(self):
        self.rect.move_ip(self.direction[0],self.direction[1])

        if self.trajectoire == 1:#logarithme droite
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
        if ((self.rect.bottom > const.SCREEN_HEIGHT) or (self.rect.top < 0)):
            self.kill()

      def draw(self, surface):
        surface.blit(self.image, self.rect)

def Colision(p_tirs,p_P1,p_enemies,p_explo,boosts,tempscore,p_alive):
    for shoot in p_tirs:
        if shoot.team == 0:#si tir enemi
            if pygame.sprite.collide_rect(shoot,p_P1): #ajout pour voir si limite les lags
                if pygame.sprite.collide_mask(shoot,p_P1): #colision tirs joueur
                    p_P1.PV -= shoot.damage
                    if shoot in p_tirs:
                        p_tirs.remove(shoot)
                    if p_P1.PV <= 0:
                        p_alive = Mort(p_tirs,p_P1,p_enemies)
        else:
            for enemy in p_enemies:
                if pygame.sprite.collide_rect(shoot,enemy): #ajout pour voir si limite les lags  
                    if pygame.sprite.collide_mask(shoot,enemy):
                        enemy.PV -=  shoot.damage
                        if shoot in p_tirs and shoot.trajectoire != 10:
                            p_tirs.remove(shoot)
                        if enemy.PV <= 0:
                            tempscore+=enemy.score
                            p_explo.append(menu.explosion(enemy))
                            bonus.dropBooster(boosts,enemy)
                            p_enemies.remove(enemy)
    for enemy in p_enemies:
        if pygame.sprite.collide_rect(p_P1, enemy):#ajout pour voir si limite les lags
            if pygame.sprite.collide_mask(p_P1,enemy): #colision ennemi joueur 
                p_P1.PV -= enemy.ATK
                tempscore+=enemy.score
                p_explo.append(menu.explosion(enemy))
                bonus.dropBooster(boosts,enemy)
                p_enemies.remove(enemy)
                if p_P1.PV <= 0:
                    p_alive = Mort(p_tirs,p_P1,p_enemies)
                
    return (tempscore,p_alive)
    
def Mort(p_tirs,p_P1,p_enemies):
    for shoot in p_tirs:
        p_tirs.remove(shoot)
    for enemy in p_enemies:
        p_enemies.remove(enemy)
    return False