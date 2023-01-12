import pygame, sys, math, fight, time, cinematiques, pickle, random, boss
from pygame.locals import *
import personnages, menu, bonus, gc
import constantes as const    

def LancerMission5():
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
            texte=font.render("Félicitations pour votre victoire.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Je me passerais d'ironie pour cette fois", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==2:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Vous avez récupéré un vaisseau alien.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Selon l'analyse du labo, il pourra devenir très puissant si", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("vous l'améliorez. Nous vous conseillons donc de rassembler du", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("matériel, quitte à retourner dans des secteurs déjà passés.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==3:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Pour la suite de la mission, les ordres sont toujours les mêmes:", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Avancez, et atteignez le vaisseau mère des aliens", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        else:
            tempsdemarrage = time.time() #A mettre ici, sinon les adversaires risquent de spawn pendant le dialogue.
            pygame.mixer.music.load("sons/Mission5.mp3")
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
            fight.SpawHistoire(enemies,1,100,-20)
            fight.SpawHistoire(enemies,1,200,-20)
            fight.SpawHistoire(enemies,1,300,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-100,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-200,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-300,-20)

            fight.SpawHistoire(enemies,5,100,-100)
            fight.SpawHistoire(enemies,5,200,-100)
            fight.SpawHistoire(enemies,5,300,-100)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2,-100)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH-100,-100)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH-200,-100)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH-300,-100)

            fight.SpawHistoire(enemies,4,0,-100)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH,-100)
            numformation=1
        elif tempspasse > 10 and numformation==1:
            for i in range (1,4,1):#De 1 inclus a 4 exclu
                for l in range (0,const.SCREEN_WIDTH,40):
                    fight.SpawHistoire(enemies,i,l,-40*i)
            numformation=2
        elif tempspasse > 15 and numformation==2:
            fight.SpawHistoire(enemies,5,0,-100)
            fight.SpawHistoire(enemies,5,100,-100)
            fight.SpawHistoire(enemies,5,200,-100)
            fight.SpawHistoire(enemies,5,400,-100)
            fight.SpawHistoire(enemies,5,500,-100)
            fight.SpawHistoire(enemies,5,600,-100)
            fight.SpawHistoire(enemies,5,700,-100)
            fight.SpawHistoire(enemies,5,800,-100)
            numformation=3
        elif tempspasse > 16 and numformation==3:
            fight.SpawHistoire(enemies,5,0,-100)
            fight.SpawHistoire(enemies,5,100,-100)
            fight.SpawHistoire(enemies,5,200,-100)
            fight.SpawHistoire(enemies,5,400,-100)
            fight.SpawHistoire(enemies,5,500,-100)
            fight.SpawHistoire(enemies,5,600,-100)
            fight.SpawHistoire(enemies,5,700,-100)
            fight.SpawHistoire(enemies,5,800,-100)
            numformation=4
        elif tempspasse > 17 and numformation==4:
            fight.SpawHistoire(enemies,5,0,-100)
            fight.SpawHistoire(enemies,5,100,-100)
            fight.SpawHistoire(enemies,5,200,-100)
            fight.SpawHistoire(enemies,5,400,-100)
            fight.SpawHistoire(enemies,5,500,-100)
            fight.SpawHistoire(enemies,5,600,-100)
            fight.SpawHistoire(enemies,5,700,-100)
            fight.SpawHistoire(enemies,5,800,-100)
            
            numformation=5
        elif tempspasse > 18 and numformation==5:
            fight.SpawHistoire(enemies,5,200,-100)
            fight.SpawHistoire(enemies,5,400,-100)
            
            numformation=6
        elif tempspasse > 19 and numformation==6:
            fight.SpawHistoire(enemies,5,150,-100)
            fight.SpawHistoire(enemies,5,350,-100)
            
            numformation=7
        elif tempspasse > 20 and numformation==7:
            fight.SpawHistoire(enemies,5,100,-100)
            fight.SpawHistoire(enemies,5,300,-100)
            
            numformation=8
        elif tempspasse > 25 and numformation==8:
            fight.SpawHistoire(enemies,3,100,-20)
            fight.SpawHistoire(enemies,3,260,-20)
            fight.SpawHistoire(enemies,3,400,-40)
            fight.SpawHistoire(enemies,3,740,-40)
            fight.SpawHistoire(enemies,3,600,-60)
            fight.SpawHistoire(enemies,3,360,-60)
            fight.SpawHistoire(enemies,3,520,-80)
            fight.SpawHistoire(enemies,3,600,-80)
            fight.SpawHistoire(enemies,3,310,-100)
            fight.SpawHistoire(enemies,3,450,-100)
            fight.SpawHistoire(enemies,3,700,-120)
            fight.SpawHistoire(enemies,3,500,-120)
            fight.SpawHistoire(enemies,3,100,-140)
            fight.SpawHistoire(enemies,3,250,-140)
            fight.SpawHistoire(enemies,3,100,-160)
            numformation=9
        elif tempspasse > 30 and numformation==9:
            for l in range (0,const.SCREEN_WIDTH,40):
                fight.SpawHistoire(enemies,1,l,-20)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2,-100)
            numformation=10
        elif tempspasse > 33 and numformation==10:
            for l in range (0,const.SCREEN_WIDTH,40):
                fight.SpawHistoire(enemies,2,l,-20)
            fight.SpawHistoire(enemies,4,100,-100)
            numformation=11
        elif tempspasse > 36 and numformation==11:
            for l in range (0,const.SCREEN_WIDTH,40):
                fight.SpawHistoire(enemies,3,l,-20)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH-100,-100)
            numformation=12
        elif tempspasse > 40 and numformation==12:
            fight.SpawHistoire(enemies,6,const.SCREEN_WIDTH//2,-70)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2,-150)
            numformation=13
        elif tempspasse > 45 and numformation==13:
            fight.SpawHistoire(enemies,6,const.SCREEN_WIDTH//2-200,-70)
            fight.SpawHistoire(enemies,6,const.SCREEN_WIDTH//2,-70)
            fight.SpawHistoire(enemies,6,const.SCREEN_WIDTH//2+200,-70)
            for l in range (const.SCREEN_WIDTH//2-200,const.SCREEN_WIDTH//2+200,40):
                fight.SpawHistoire(enemies,1,l,-150)
            numformation=14
        elif numformation==14 and len(enemies)==0:
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f)
            if temp['Histoire']==4:
                temp['Histoire']=5
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
        
        for entity in enemies: #Déplacement linéaire des ennemis !A CHANGER!
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
        