import pygame, sys, math, fight, time, cinematiques, pickle, random
from pygame.locals import *
import personnages, menu, bonus, gc
import constantes as const    

def LancerMission2():
    pygame.mixer.music.stop()
    FramePerSec = pygame.time.Clock()
    score = 0
    alive = True
    dialogue = 1
    numformation=0
    appui = False
    VaisseauChoisis = menu.ChoixPerso()
    AP = menu.Arrièreplan(3)# 1 a 3 pour le fond
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(VaisseauChoisis)
    CP = personnages.Compagon(P1)
    bulle = menu.Affichage("sprites/bulletexte.png",const.SCREEN_WIDTH-270,110)
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
            texte=font.render("Vous avez réussit à vous sortir de ce mauvais pas !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Vous l'aurez peut être remarqué, mais pendant que vous", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("vous amusiez avec les aliens, nous on a bossé pour de vrai.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==2:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Premièrement nous avons appris le but des aliens:", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Aucun alien n'a jamais réussi à terminer le jeu 'Space invader'.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Considérant cela comme une tâche prioritaire pour leur espèces, ils", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("ont apparemment décidé de voler toutes les versions du jeu.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==3:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Enfin, l'équipe technique à bossée dur pour vous:", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Un vieux satellite des années 2000 a été ré-équipé", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("par des drones afin de vous servir d'atelier. Vous devriez", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("même pouvoir bricoler des armes et vaisseaux aliens si vous", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("arrivez à en rafler aux aliens.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==4:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Votre prochaine mission est d'avancer en territoire alien afin de", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("récupérer des informations. Méfiez vous, ceux que vous avez affronté", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("précédemment ne sont rien d'autres que de simples vaisseaux. Vos", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("nouveaux enemis seront plus nombreux, et plus puissant. La communication", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("va bientôt couper. On vous recontacte dès qu'elle sera rétablie !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        else:
            tempsdemarrage = time.time() #A mettre ici, sinon les adversaires risquent de spawn pendant le dialogue.
            pygame.mixer.music.load("sons/Mission2.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
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
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-30,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-30,-50)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-30,-80)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-30,-110)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-30,-140)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+30,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+30,-50)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+30,-80)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+30,-110)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+30,-140)
            fight.SpawHistoire(enemies,1,60,-80)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-60,-80)
            numformation=1
        elif tempspasse > 10 and numformation==1: 
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH-60,0)
            numformation=2
        elif tempspasse > 11 and numformation==2:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2,0)
            numformation=3
        elif tempspasse > 12 and numformation==3:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH,0)
            numformation=4
        elif tempspasse > 13 and numformation==4:
            fight.SpawHistoire(enemies,4,0,0)
            numformation=5
        elif tempspasse > 14 and numformation==5:
            fight.SpawHistoire(enemies,4,200,0)
            numformation=6
        elif tempspasse > 15 and numformation==6:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH-200,0)
            numformation=7
        elif tempspasse > 16 and numformation==7:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2-50,0)
            numformation=8
        elif tempspasse > 17 and numformation==8:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2+50,0)
            numformation=9
        elif tempspasse > 18 and numformation==9:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH-50,0)
            numformation=10
        elif tempspasse > 19 and numformation==10:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH,0)
            fight.SpawHistoire(enemies,4,0,0)
            fight.SpawHistoire(enemies,4,100,0)
            numformation=11
        elif tempspasse > 22 and numformation==11:
            for i in range (0,5,1):
                fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2+i*40,0)
                fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2-i*40,0)
            numformation=12
        elif tempspasse > 25 and numformation==12:
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-30,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-70,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-50,-30)
            fight.SpawHistoire(enemies,2,30,0)
            fight.SpawHistoire(enemies,2,70,0)
            fight.SpawHistoire(enemies,2,50,-30)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+15,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-15,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2,-30)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2,-60)
            numformation=13
        elif tempspasse > 30 and numformation==13:
            fight.SpawHistoire(enemies,1,30,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-30,0)
            fight.SpawHistoire(enemies,2,70,0)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-70,0)
            fight.SpawHistoire(enemies,3,110,0)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-110,0)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH,-100)
            numformation=14
        elif tempspasse > 35 and numformation==14:
            fight.SpawHistoire(enemies,4,const.SCREEN_HEIGHT,0)
            fight.SpawHistoire(enemies,4,0,0)
            numformation+=1
        elif tempspasse > 36 and numformation==15:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2,0)
            fight.SpawHistoire(enemies,4,0,0)
            numformation+=1
        elif tempspasse > 37 and numformation==16:
            fight.SpawHistoire(enemies,4,const.SCREEN_HEIGHT,0)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2,0)
            numformation+=1
        elif tempspasse > 38 and numformation==17:
            fight.SpawHistoire(enemies,4,const.SCREEN_HEIGHT//2+50,0)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2-50,0)
            numformation+=1
        elif tempspasse > 39 and numformation==18:
            fight.SpawHistoire(enemies,4,50,0)
            fight.SpawHistoire(enemies,4,100,0)
            numformation+=1
        elif tempspasse > 40 and numformation==19:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH,0)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH-150,0)
            numformation+=1
        elif tempspasse > 41 and numformation==20:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2+150,0)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2-350,0)
            numformation+=1
        elif tempspasse > 42 and numformation==21:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2,0)
            fight.SpawHistoire(enemies,4,100,0)
            numformation+=1
        elif tempspasse > 43 and numformation==22:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH-400,0)
            fight.SpawHistoire(enemies,4,400,0)
            numformation+=1
        elif tempspasse > 47 and numformation==23:
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH-100,0)
            fight.SpawHistoire(enemies,5,100,0)
            numformation+=1
        elif numformation==24 and len(enemies)==0:
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f)
            if temp['Histoire']==1:
                temp['Histoire']=2
            with open('sauvegarde.pkl', 'wb') as f:
                    pickle.dump(temp, f)
            pygame.mixer.music.fadeout(10000)
            menu.MenuFinPartie(score,True)
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
        
        for entity in enemies: #Déplacement linéaire des ennemis 
            if entity.active == 1:
                entity.move()
                entity.moveKamikaze(P1)
            p = random.randint(0,300)
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
                elif (entity.id == "e5"):
                    shoot = fight.Projectile(entity,4,"sprites_animation/boule1.png")
                    tirs.append(shoot)
                    shoot = fight.Projectile(entity,5,"sprites_animation/boule1.png")
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
            if shoot.trajectoire == 3 and shoot.tireur_id == "e1" or shoot.tireur_id == "e5":
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
        