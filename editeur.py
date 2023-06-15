import pygame, sys, math, fight, time, cinematiques, pickle, re
from pygame.locals import *
import personnages, menu, bonus, gc, random
import constantes as const    

def MissionEditeur():

    #Récupération des infos du fichier TXT------------------------------------------------
    with open('Editeur.txt', 'r') as fichier:
        lignes = fichier.readlines() #Récupération des lignes sous forme de liste

    #Préparation des valeurs de base du jeu-----------------------------------------------
    pygame.mixer.music.stop()
    FramePerSec = pygame.time.Clock()
    score = 0
    alive = True
    numformation=0
    appui = False
    VaisseauChoisis = menu.ChoixPerso()
    P1 = personnages.Player(VaisseauChoisis)
    CP = personnages.Compagon(P1)
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    P1.souris(personnages.DISPLAYSURF)
    cooldown = P1.cooldown
    backup = cooldown #sert à la gestion des ultis 
    with open('sauvegarde.pkl', 'rb') as f:
        temp = pickle.load(f)
    if VaisseauChoisis == 1:
        Ulti = temp['V1'][7]
    elif VaisseauChoisis == 2:
        Ulti = temp['V2'][7]
    elif VaisseauChoisis == 3:
        Ulti = temp['V3'][7]

    #Valeur de base définie. En cas d'oubli dans l'editeur, le jeu se lancera quand même
    AP = menu.Arrièreplan(3)
    AP2= menu.Arrièreplan(5)
    AP3= menu.Arrièreplan(6)

    enemies = [] 
    tirs = []
    explo = []
    boosts = []
    gc.collect()
    tempsdemarrage = time.time()

    #Actions effectués à chaque images---------------------------------------------
    def ActionsDeChaqueTours(tirs,P1,enemies,explo,boosts,score,alive,cooldown):
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
                entity.moveKamikaze(P1)
                p = random.randint(0,500)
                if p < 1:
                    if (entity.id == "e1"):
                        shoot = fight.Projectile(entity,3,"sprites_animation/boule1.png")
                    elif (entity.id == "e2"):
                        shoot = fight.Projectile(entity,2,"sprites/tir3.png")
                        tirs.append(shoot)
                        shoot = fight.Projectile(entity,1,"sprites/tir3.png")
                        tirs.append(shoot)
                        shoot = fight.Projectile(entity,0,"sprites/tir3.png")
                    elif (entity.id == "e3"):
                        shoot = fight.Projectile(entity,0,"sprites/tir.png")
                    tirs.append(shoot)
            if entity.rect.top > const.SCREEN_HEIGHT:
                    enemies.remove(entity)


        #faire avance les tirs
        for shoot in tirs:
            shoot.move()
            if shoot.trajectoire == 10:
                shoot.suivre(P1)
                menu.Animation(const.laserboss, shoot)
            if (((shoot.rect.bottom > const.SCREEN_HEIGHT) or (shoot.rect.top < 0)) and (shoot.trajectoire != 10)):#pour l'ulti laser
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

        if Ulti: #gestion des ultis
            if P1.DureeUlti == -1:
                P1.ulti(enemies,tirs,explo,score)
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

        CP.update(P1)
        CP.draw(personnages.DISPLAYSURF)#Affichage Compagnon
        MB.draw(personnages.DISPLAYSURF)#Affichage menu bas
        menu.AfficheScore(score) #Affichage score


        pygame.display.update()
        FramePerSec.tick(const.FPS)
        if alive != True: #En cas de victoire, on sort de la boucle avec alive=True
            pygame.mixer.music.fadeout(10000)
            menu.MenuFinPartie(score,False)#Dans le menu, le score est ajouté comme argent
            return False

    #Interpretation de chaque ligne dans le fichier de l'editeur--------------------
    for ligne in lignes:
        if ligne[0:1]=='#': #Permet l'ajout de commentaire au début d'une ligne dans l'éditeur
            pass
        else: #Tout ce qui doit être fait si la ligne n'est pas un commentaire
            #Si dessous, tests pour vérifier que la ligne correspond bien à une commande:

            #Commande de préparation du jeu
            if re.match("ParalaxProfond\((.*)\)",ligne):
                if re.match("ParalaxProfond\((.*)\)",ligne).group(1) in ["1","2","3"]: #Important de mettre la liste en string. Sinon pas de match
                    AP = menu.Arrièreplan(int(re.match("ParalaxProfond\((\d+)\)",ligne).group(1)))
                else:
                    print("Erreur lors de l'appel de la fonction "+ str(ligne) + 
                          "Les paramètres possibles sont 1, 2 ou 3. Actuellement " + str(re.match("ParalaxProfond\((.*)\)",ligne).group(1)))
                    return
            elif re.match("ParalaxIntermediaire\((.*)\)",ligne):
                if re.match("ParalaxIntermediaire\((.*)\)",ligne).group(1) in ["4","5"]:
                    AP2 = menu.Arrièreplan(int(re.match("ParalaxIntermediaire\((\d+)\)",ligne).group(1)))
                else:
                    print("Erreur lors de l'appel de la fonction "+ str(ligne) + 
                          "Les paramètres possibles sont 4 ou 5. Actuellement " + str(re.match("ParalaxIntermediaire\((.*)\)",ligne).group(1)))
                    return
            elif re.match("ParalaxProche\((.*)\)",ligne):
                if re.match("ParalaxProche\((.*)\)",ligne).group(1) in ["6","7"]:
                    AP3 = menu.Arrièreplan(int(re.match("ParalaxProche\((\d+)\)",ligne).group(1)))
                else:
                    print("Erreur lors de l'appel de la commande "+ str(ligne) + 
                          "Les paramètres possibles sont 6 ou 7. Actuellement " + str(re.match("ParalaxProche\((.*)\)",ligne).group(1)))
                    return
           
            #Commandes de création de jeu
            elif re.match("Attendre\((.*)\)",ligne):
                try:
                    if type(int(re.match("Attendre\((\d+)\)",ligne).group(1)))==type(1):
                        pass
                except:
                    print ("Erreur lors de l'execution de la commande " + str(ligne) + "Vous devez entrer un chiffre entre les parentheses")
                    return
                while time.time() - tempsdemarrage<int(re.match("Attendre\((\d+)\)",ligne).group(1)):
                    if ActionsDeChaqueTours(tirs,P1,enemies,explo,boosts,score,alive,cooldown)==False:
                        return
            
            elif re.match(r"Ennemi\((.*),(.*),(.*)\)", ligne):
                match = re.match(r"Ennemi\((.*),(.*),(.*)\)", ligne)
                try:
                    if match.group(1) in ["1","2","3","4","5","6"]:
                        typeAdversaire = int(match.group(1))
                    else:
                        print("Erreur lors de l'appel de la commande " + str(ligne) + 
                          "Le premier nombre doit etre un chiffre compris entre 1 et 6. Actuellement " + match.group(1))
                        return
                except:
                    print("Erreur lors de l'appel de la commande " + str(ligne) + 
                          "Le premier nombre doit etre un chiffre compris entre 1 et 6. Actuellement " + match.group(1))
                    return
                try:
                    positionHorizontale = int(match.group(2))
                except:
                    print("Erreur lors de l'appel de la commande " + str(ligne) + 
                          "Le second nombre doit etre un chiffre compris entre 0 et 800 (tu peut faire plus ou moins, mais on ne verra pas le vaisseau). Actuellement " + match.group(1))
                    return
                try:
                    positionVerticale = int(match.group(3))
                except:
                    print("Erreur lors de l'appel de la commande " + str(ligne) + 
                          "Le dernier nombre doit etre un chiffre (possible qu'il soit négatif si tu le souhaite). Actuellement " + match.group(1))
                    return

                fight.SpawHistoire(enemies,typeAdversaire,positionHorizontale,positionVerticale)
                if ActionsDeChaqueTours(tirs,P1,enemies,explo,boosts,score,alive,cooldown)==False:
                    return
            else:
                print("Erreur lors de la commande " + str (ligne) + "Commande inconnue")
                return
    
    while len(enemies)>0:
        ActionsDeChaqueTours(tirs,P1,enemies,explo,boosts,score,alive,cooldown)
    return

    while alive:
        

        #Boucle de spawn après timer
        """ Exemple, à changer avec lecture dynamique
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
            pygame.mixer.music.fadeout(10000)
            menu.MenuFinPartie(score,True)
            break"""



        