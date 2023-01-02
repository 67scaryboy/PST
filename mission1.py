import pygame, sys, math, fight, time, cinematiques, pickle
from pygame.locals import *
import personnages, menu, bonus, gc
import constantes as const    

def LancerMission1():

    FramePerSec = pygame.time.Clock()
    score = 0
    alive = True
    dialogue = 1
    numformation=0
    appui = False
    VaisseauChoisis = menu.ChoixPerso()
    valeurs_cinematique = cinematiques.Cinematique1(VaisseauChoisis) #cinématique
    AP = menu.Arrièreplan(3)# 1 a 3 pour le fond
    AP.rect.center = valeurs_cinematique[3]
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP2.rect.center = valeurs_cinematique[2]
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    AP3.rect.center = valeurs_cinematique[1]
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(valeurs_cinematique[0])
    CP = personnages.Compagon(P1)
    bulle = menu.Affichage("sprites/bulletexte.png",const.SCREEN_WIDTH-270,110)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    P1.rect.center = pygame.mouse.get_pos()
    cooldown = P1.cooldown

    enemies = [] 
    tirs = []
    explo = []
    boosts = []
    gc.collect()
    while alive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0] and not appui: #Pour faire en sorte qui si on laisse le clic envoncé, ca ne skip pas le dialogue
            dialogue+=1
            appui = pygame.mouse.get_pressed()[0]
        if not pygame.mouse.get_pressed()[0]:
            appui = pygame.mouse.get_pressed()[0]
        personnages.DISPLAYSURF.fill(const.WHITE)
        AP3.move(3)#vitesse de déplacement des couches
        AP2.move(2)
        AP.move(1)#laisser 1 pour le fond, sinon ca file la gerbe
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        P1.draw(personnages.DISPLAYSURF)
        bulle.draw(personnages.DISPLAYSURF)
        if dialogue==1:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Soldat ! Vous êtes la dernière troupe qu'il nous reste dans le secteur !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Les autres escouades ont toutes été balayées, vous allez devoir", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("avancer sans support jusqu'au vaisseau ennemi !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==2:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Nous ne vous abandonnerons pas pour autant, même si on aurait", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("préferé...", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Vous êtes la dernière unitée combatante dont nous disposons,", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("croyez moi, ça ne m'enchante pas plus que vous.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==3:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Malgré votre QI d'huitre, je vais tenter de vous expliquer", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("simplement ce que vous devez faire:", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Evitez les tirs ennemis.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Trucidez-les avant qu'ils ne vous trucident.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Même vous, vous devriez avoir compris je pense.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==4:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Lorsqu'ils sont détruits, les vaisseaux aliens larguent des", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("composants appelés 'score'. Cherchez pas, ils sont fous ces aliens.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("A la fin de votre mission, vous pourrez vous servir  de ces", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("composants afin d'améliorer votre vaisseau. Nous vous mettrons", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("à disposition un atelier dédié. Evitez de le casser...", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==5:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Votre vaisseau est équipé d'un protocole {SAVE THE PILOT}.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Vu que vous n'avez surement pas lu le manuel, je vais vous rappeler", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("ce que cela veut dire: même en cas de destruction, votre vaisseau", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("vous gardera en vie et mettra en sécurité les compostants récupérés.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Vous avez de la chance de disposer de ce prototype.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==6:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Je pense qu'on à fait le tour.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Des questions ?", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Oui ?", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("C'est dommage, c'est pas mon problème.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Bonne chance !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        else:
            tempsdemarrage = time.time() #A mettre ici, sinon les adversaires risquent de spawn pendant le dialogue.
            break
                
        pygame.display.update()
        FramePerSec.tick(const.FPS)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    while alive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        score,alive=fight.Colision(tirs,P1,enemies,explo,boosts,score,alive)
        bonus.AttraperBoost(boosts,P1)

        for boost in boosts:
                    boost.move()
                    if boost.rect.bottom > const.SCREEN_HEIGHT:
                            boosts.remove(boost)

        #Boucle de spawn après timer
        tempspasse = time.time() - tempsdemarrage
        if tempspasse > 5 and numformation==0: # Temps en secondes
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-20,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+20,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+40,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-40,-40)
            numformation=1
        elif tempspasse > 7 and numformation==1: #Création d'une formation rectangle
            for c in range (0,4,1): #Nombre de colonne
                for l in range (0,7,1): #Nombre de lignes
                    fight.SpawHistoire(enemies,1,l*40,c*(-30))
            numformation=2
        elif tempspasse > 15 and numformation==2:
            for i in range (1,11,1): #Creation d'une rampe
                fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-(i*30),i*(-30))
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+40,-350)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-40,-350)
            numformation=3
        elif tempspasse > 20 and numformation==3:
            fight.SpawHistoire(enemies,1,10,-60)
            fight.SpawHistoire(enemies,1,40,-30)
            fight.SpawHistoire(enemies,1,70,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-10,-60)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-40,-30)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-70,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2,-60)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2,-30)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2,0)
            numformation=4
        elif tempspasse > 25 and numformation==4:
            for i in range (0,5,1): #Formation carée décalé
                for j in range (0,5,1):
                    fight.SpawHistoire(enemies,1,10+j*40+i*20,i*(-30))
            for c in range (0,4,1): #Nombre de colonne
                for l in range (0,3,1): #Nombre de lignes
                    fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-l*40,c*(-30)-200)#Formation carée
            numformation=5
        elif tempspasse > 32 and numformation==5:
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+30,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-30,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+60,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-60,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-60,-30)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+60,-30)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-60,-60)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+60,-60)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-60,-90)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+60,-90)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-30,-90)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2,-90)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+30,-90)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2,-45)
            numformation=6
        elif tempspasse > 35 and numformation==6:
            for i in range (1,5,1):
                fight.SpawHistoire(enemies,2,i*40,0)
                fight.SpawHistoire(enemies,2,l*(-40),0)
            numformation=7
        elif tempspasse > 40 and numformation==7:
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2,0)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2-30,0)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2+30,0)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2+60,0)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2-60,0)
            numformation=8
        elif numformation==8 and tempspasse>50:
            menu.MenuFinPartie(score,True)
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f)
            if temp['Histoire']==0:
                temp['Histoire']=1
            with open('sauvegarde.pkl', 'wb') as f:
                    pickle.dump(temp, f)
            break


        #tir automatique
        if P1.cooldown == 0:
            with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir si on à débloqué ou pas les vaisseaux
                temp = pickle.load(f)
            if VaisseauChoisis==1: #Permet de changer le sprite des tirs en fonction du nombre d'amélioration d'attaque
                if temp['V1'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira.png")
                    shootf= fight.Projectile(CP,0,"sprites/tira.png")
                elif temp['V1'][4]==1:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shootf= fight.Projectile(CP,0,"sprites/tira2.png")
                elif temp['V1'][4]==2:
                    shoot = fight.Projectile(P1,0,"sprites/tira3.png")
                    shootf= fight.Projectile(CP,0,"sprites/tira3.png")
            elif VaisseauChoisis==2: 
                if temp['V2'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shootf= fight.Projectile(CP,0,"sprites/tira2.png")
                elif temp['V2'][4]==1:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    shootf= fight.Projectile(CP,0,"sprites/tira2.png")
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
                    shootf= fight.Projectile(CP,0,"sprites/tira2.png")
            elif VaisseauChoisis==3:
                if temp['V3'][4]==0:
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.right=P1.rect.right
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,0,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    shootf= fight.Projectile(CP,0,"sprites/tira2.png")
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
                    shootf= fight.Projectile(CP,0,"sprites/tira2.png")
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
                    shootf= fight.Projectile(CP,0,"sprites/tira2.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,8,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.left
                    tirs.append(shoot)
                    shoot = fight.Projectile(P1,9,"sprites/tira2.png")
                    shoot.rect.left=P1.rect.right

            tirs.append(shoot)
            tirs.append(shootf)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1
        
        for entity in enemies: #Déplacement linéaire des ennemis !A CHANGER!
            if entity.active == 1:
                entity.move()
            if entity.rect.bottom > const.SCREEN_HEIGHT:
                    enemies.remove(entity)


        #faire avance les tirs
        for shoot in tirs:
            shoot.move()
            if shoot.rect.bottom > const.SCREEN_HEIGHT:
                    tirs.remove(shoot)

        ###Partie graphique###
        personnages.DISPLAYSURF.fill(const.WHITE)

        #Déplacement et affichage des images de fond
        AP3.move(3)#vitesse de déplacement des couches
        AP2.move(2)
        AP.move(1)#laisser 1 pour le fond, sinon ca file la gerbe
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        #Affichage des tirs
        for shoot in tirs:
            if shoot.trajectoire == 3 and shoot.tireur_id == "e1":
                menu.Animation(const.boules,shoot)
            shoot.draw(personnages.DISPLAYSURF)
        
        #Affichage des bonus
        for boost in boosts:
            boost.draw(personnages.DISPLAYSURF)

        #Affichage des explosions
        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)

        #Affichage des adversaires restants
        for entity in enemies:
            if entity.active == 1:
                entity.draw(personnages.DISPLAYSURF)
        P1.souris(personnages.DISPLAYSURF)#Affichage joueur
        P1.draw_health(personnages.DISPLAYSURF)
        CP.update(P1)
        CP.draw(personnages.DISPLAYSURF)#Affichage Compagnon
        MB.draw(personnages.DISPLAYSURF)#Affichage menu bas
        menu.AfficheScore(score) #Affichage score


        pygame.display.update()
        FramePerSec.tick(const.FPS)
    if alive != True: #En cas de victoire, on sort de la boucle avec alive=True
        menu.MenuFinPartie(score,False)#Dans le menu, le score est ajouté comme argent
        