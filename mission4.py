import pygame, sys, math, fight, time, cinematiques, pickle, random, boss
from pygame.locals import *
import personnages, menu, bonus, gc
import constantes as const    

def LancerMission4():

    FramePerSec = pygame.time.Clock()
    score = 0
    alive = True
    dialogue = 1
    numformation=0
    appui = False
    VaisseauChoisis = menu.ChoixPerso()
    AP = menu.Arrièreplan(2)# 1 a 3 pour le fond
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(VaisseauChoisis)
    CP = personnages.Compagon(P1)
    bulle = menu.Affichage("sprites/bulletexte.png",const.SCREEN_WIDTH-270,110)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    P1.souris(personnages.DISPLAYSURF)
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
            texte=font.render("Enfin on a réussit à rétablir les communications !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("...", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Je ne me souvenais pas que votre tête était aussi ...", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Bref", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==2:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("J'ai une mauvaise nouvelle soldat.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Nos radars longue portée ont détécté un énorme vaisseau alien", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("tout proche de vous. Vous allez surement l'avoir bientot en", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("visuel.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==3:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Nouveaux ordres prioritaires:", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Abattez cette menace à tout prix", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Selon nos informations, ce truc transporte des vaisseaux", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("aliens. Si vous arrivez à l'abattre, il est possible que vous", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("arriviez à en ramener un avec vous.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==4:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("On vous recontactera dès qu'on ne verra plus ce gros truc sur", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("les écrans radar.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Bonne chance", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Vous allez en avoir besoin", True, const.BLACK)
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
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-200,-120)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-160,-100)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-120,-80)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-80,-60)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-40,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+40,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+80,-60)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+120,-80)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+160,-100)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+200,-120)
            numformation=1
        elif tempspasse > 10 and numformation==1: 
            fight.SpawHistoire(enemies,2,200+200,-120)
            fight.SpawHistoire(enemies,2,200+160,-100)
            fight.SpawHistoire(enemies,2,200+120,-80)
            fight.SpawHistoire(enemies,2,200+80,-60)
            fight.SpawHistoire(enemies,2,200+40,-40)
            fight.SpawHistoire(enemies,1,200,-20)
            fight.SpawHistoire(enemies,3,200-200,-40)
            fight.SpawHistoire(enemies,3,200-160,-60)
            fight.SpawHistoire(enemies,3,200-120,-80)
            fight.SpawHistoire(enemies,3,200-80,-100)
            fight.SpawHistoire(enemies,3,200-40,-120)

            fight.SpawHistoire(enemies,2,600-200,-120)
            fight.SpawHistoire(enemies,2,600-160,-100)
            fight.SpawHistoire(enemies,2,600-120,-80)
            fight.SpawHistoire(enemies,2,600-80,-60)
            fight.SpawHistoire(enemies,2,600-40,-40)
            fight.SpawHistoire(enemies,1,600,-20)
            fight.SpawHistoire(enemies,3,600+200,-40)
            fight.SpawHistoire(enemies,3,600+160,-60)
            fight.SpawHistoire(enemies,3,600+120,-80)
            fight.SpawHistoire(enemies,3,600+80,-100)
            fight.SpawHistoire(enemies,3,600+40,-120)
            numformation=2
        elif tempspasse > 15 and numformation==2:
            fight.SpawHistoire(enemies,2,200-200,-120)
            fight.SpawHistoire(enemies,2,200-160,-100)
            fight.SpawHistoire(enemies,2,200-120,-80)
            fight.SpawHistoire(enemies,2,200-80,-60)
            fight.SpawHistoire(enemies,2,200-40,-40)
            fight.SpawHistoire(enemies,2,200,-20)
            fight.SpawHistoire(enemies,2,200+40,-40)
            fight.SpawHistoire(enemies,2,200+80,-60)
            fight.SpawHistoire(enemies,2,200+120,-80)
            fight.SpawHistoire(enemies,2,200+160,-100)
            fight.SpawHistoire(enemies,2,200+200,-120)
            fight.SpawHistoire(enemies,2,600-200,-120)
            fight.SpawHistoire(enemies,2,600-160,-100)
            fight.SpawHistoire(enemies,2,600-120,-80)
            fight.SpawHistoire(enemies,2,600-80,-60)
            fight.SpawHistoire(enemies,2,600-40,-40)
            fight.SpawHistoire(enemies,2,600,-20)
            fight.SpawHistoire(enemies,2,600+40,-40)
            fight.SpawHistoire(enemies,2,600+80,-60)
            fight.SpawHistoire(enemies,2,600+120,-80)
            fight.SpawHistoire(enemies,2,600+160,-100)
            fight.SpawHistoire(enemies,2,600+200,-120)
            numformation=3
        elif tempspasse > 16 and numformation==3:
            fight.SpawHistoire(enemies,5,160,-40)
            numformation=4
        elif tempspasse > 17 and numformation==4:
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH-100,-40)
            numformation=5
        elif tempspasse > 18 and numformation==5:
            fight.SpawHistoire(enemies,5,350,-40)
            numformation=6
        elif tempspasse > 19 and numformation==6:
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH-300,-40)
            numformation=7
        elif tempspasse > 20 and numformation==7:
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH-200,-40)
            numformation=8
        elif tempspasse > 21 and numformation==8:
            fight.SpawHistoire(enemies,5,100,-40)
            numformation=9
        elif tempspasse > 22 and numformation==9:
            fight.SpawHistoire(enemies,5,300,-40)
            numformation=10
        elif tempspasse > 25 and numformation==10:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH-100,-40)
            numformation=11
        elif tempspasse > 30 and numformation==11:
            fight.SpawHistoire(enemies,3,40,-20)
            fight.SpawHistoire(enemies,3,50,-40)
            fight.SpawHistoire(enemies,3,70,-60)
            fight.SpawHistoire(enemies,3,100,-80)
            fight.SpawHistoire(enemies,3,140,-100)
            fight.SpawHistoire(enemies,3,190,-120)
            fight.SpawHistoire(enemies,3,250,-140)
            fight.SpawHistoire(enemies,3,320,-160)
            fight.SpawHistoire(enemies,3,400,-180)

            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-40,-20)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-50,-40)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-70,-60)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-100,-80)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-140,-100)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-190,-120)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-250,-140)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-320,-160)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-400,-180)
            numformation=12
        elif tempspasse > 33 and numformation==12:
            fight.SpawHistoire(enemies,4,40,-80)
            fight.SpawHistoire(enemies,4,500,-160)
            numformation=13
        elif tempspasse > 37 and numformation==13:
            fight.SpawHistoire(enemies,3,40,-20)
            fight.SpawHistoire(enemies,3,80,-20)
            fight.SpawHistoire(enemies,3,40,-60)
            fight.SpawHistoire(enemies,3,80,-60)
            fight.SpawHistoire(enemies,3,240,-80)
            fight.SpawHistoire(enemies,3,240,-120)
            fight.SpawHistoire(enemies,3,280,-80)
            fight.SpawHistoire(enemies,3,280,-120)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-100,-70)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-140,-70)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-100,-110)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-140,-110)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-200,-140)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-240,-140)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-200,-180)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH-240,-180)
            fight.SpawHistoire(enemies,1,370,-120)
            fight.SpawHistoire(enemies,1,410,-120)
            fight.SpawHistoire(enemies,1,370,-160)
            fight.SpawHistoire(enemies,1,410,-160)
            numformation=14
        elif tempspasse > 40 and numformation==14:
            fight.SpawHistoire(enemies,1,450,-20)
            fight.SpawHistoire(enemies,1,410,-20)
            fight.SpawHistoire(enemies,1,450,-60)
            fight.SpawHistoire(enemies,1,410,-60)
            fight.SpawHistoire(enemies,1,300,-80)
            fight.SpawHistoire(enemies,1,340,-120)
            fight.SpawHistoire(enemies,1,300,-80)
            fight.SpawHistoire(enemies,1,340,-120)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-250,-70)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-290,-70)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-250,-110)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-290,-110)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-300,-140)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-260,-140)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-300,-180)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-260,-180)
            fight.SpawHistoire(enemies,2,110,-120)
            fight.SpawHistoire(enemies,2,150,-120)
            fight.SpawHistoire(enemies,2,110,-160)
            fight.SpawHistoire(enemies,2,150,-160)
            numformation+=1
        elif len(enemies)==0 and numformation==15: #Début du combat de boss
            pygame.mixer.music.load("sons/boss1.mp3")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            temp = boss.temp(P1,score,AP3,AP2,AP,VaisseauChoisis)
            pygame.mixer.music.fadeout(10000)
            if temp[0]==0:
                menu.MenuFinPartie(score,False)
                break
            score=temp[0]
            numformation+=1
        elif numformation==24 and len(enemies)==0:
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f)
            if temp['Histoire']==1:
                temp['Histoire']=2
                temp['V2'][0]=True
            with open('sauvegarde.pkl', 'wb') as f:
                    pickle.dump(temp, f)
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
        