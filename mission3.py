import pygame, sys, math, fight, time, cinematiques, pickle, random
from pygame.locals import *
import personnages, menu, bonus, gc
import constantes as const    

def LancerMission3():
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
    tempsdemarrage = time.time()

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
            texte=font.render("....KrzkRRzkkRR....kRKrkrrr.......zzkrkkrkkrzkk......krzkrk..kkrkz", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("....KrzkRkkrkkrRzkkRR..krkz..kRKrkrrr...zkk......krzkrk..kkr....zz", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("krkk...kRKrkrrr...zkk....krzrRzkkRR..krkz.krk..kkr....zz....KrzkRk", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("...krzrRzkkRR..krkz.krk..kkr..krkk...kRKrkrrr...zkk...zz....KrzkRk", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        else:
            tempsdemarrage = time.time() #A mettre ici, sinon les adversaires risquent de spawn pendant le dialogue.
            #pygame.mixer.music.load("sons/Mission3.mp3")
            #pygame.mixer.music.set_volume(0.3)
            #pygame.mixer.music.play()
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
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-120,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-80,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-40,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+40,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+80,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+120,-20)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2,-100)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2+90,-100)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2-90,-100)
            
            numformation=1
        elif tempspasse > 10 and numformation==1: 
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH,0)
            fight.SpawHistoire(enemies,4,0,0)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2-180,-20)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2-90,-20)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2,-20)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2+90,-20)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2+180,-20)
            numformation=2
        elif tempspasse > 15 and numformation==2:
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-30,-20)
            fight.SpawHistoire(enemies,1,40,-50)
            fight.SpawHistoire(enemies,1,200,-100)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-100,-30)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-250,-70)
            fight.SpawHistoire(enemies,1,350,-20)
            fight.SpawHistoire(enemies,1,570,-50)
            fight.SpawHistoire(enemies,1,100,-80)
            fight.SpawHistoire(enemies,1,650,-90)
            fight.SpawHistoire(enemies,1,450,-70)
            fight.SpawHistoire(enemies,4,100,-50)
            fight.SpawHistoire(enemies,4,450,-70)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH,-100)
            numformation=3
        elif tempspasse > 20 and numformation==3:
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2,-20)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2-30,-20)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2+30,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2,-50)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2+60,-20)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH//2-60,-20)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2-70,-70)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2+70,-70)
            fight.SpawHistoire(enemies,5,70,-50)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH-70,-50)
            numformation=4
        elif tempspasse > 21 and numformation==4:
            fight.SpawHistoire(enemies,4,0,0)
            numformation=5
        elif tempspasse > 22 and numformation==5:
            fight.SpawHistoire(enemies,4,200,-20)
            numformation=6
        elif tempspasse > 23 and numformation==6:
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH-200,-40)
            numformation=7
        elif tempspasse > 26 and numformation==7:
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-50,20)
            fight.SpawHistoire(enemies,2,50,-20)
            fight.SpawHistoire(enemies,2,600,-30)
            fight.SpawHistoire(enemies,2,400,-40)
            fight.SpawHistoire(enemies,2,250,-50)
            fight.SpawHistoire(enemies,2,300,-60)
            fight.SpawHistoire(enemies,2,700,-70)
            fight.SpawHistoire(enemies,2,120,-80)
            fight.SpawHistoire(enemies,2,680,-90)
            fight.SpawHistoire(enemies,2,500,-100)
            fight.SpawHistoire(enemies,2,80,-110)
            fight.SpawHistoire(enemies,2,750,-120)
            fight.SpawHistoire(enemies,2,420,-130)
            fight.SpawHistoire(enemies,2,340,-140)
            fight.SpawHistoire(enemies,2,120,-150)
            numformation=8
        elif tempspasse > 30 and numformation==8:
            fight.SpawHistoire(enemies,2,400,0)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2,-70)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2-90,-70)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2-180,-70)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2+90,-70)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2+180,-70)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-90,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-180,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+90,-20)
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2+180,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-45,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-90,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2-135,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+45,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+90,0)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH//2+135,0)
            fight.SpawHistoire(enemies,3,50,-20)
            fight.SpawHistoire(enemies,3,50,-50)
            fight.SpawHistoire(enemies,3,50,-80)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-50,-20)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-50,-50)
            fight.SpawHistoire(enemies,3,const.SCREEN_WIDTH-50,-80)
            fight.SpawHistoire(enemies,4,100,-120)
            numformation+=1
        elif tempspasse > 35 and numformation==9:
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-50,20)
            fight.SpawHistoire(enemies,2,50,-20)
            fight.SpawHistoire(enemies,2,600,-30)
            fight.SpawHistoire(enemies,2,400,-40)
            fight.SpawHistoire(enemies,2,250,-50)
            fight.SpawHistoire(enemies,2,300,-60)
            fight.SpawHistoire(enemies,2,700,-70)
            fight.SpawHistoire(enemies,2,120,-80)
            fight.SpawHistoire(enemies,2,680,-90)
            fight.SpawHistoire(enemies,2,500,-100)
            fight.SpawHistoire(enemies,2,80,-110)
            fight.SpawHistoire(enemies,2,750,-120)
            fight.SpawHistoire(enemies,2,420,-130)
            fight.SpawHistoire(enemies,2,340,-140)
            fight.SpawHistoire(enemies,2,120,-150)
            numformation=10
        elif tempspasse > 37 and numformation==10:
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-50,20)
            fight.SpawHistoire(enemies,2,50,-20)
            fight.SpawHistoire(enemies,2,600,-30)
            fight.SpawHistoire(enemies,2,400,-40)
            fight.SpawHistoire(enemies,2,250,-50)
            fight.SpawHistoire(enemies,2,300,-60)
            fight.SpawHistoire(enemies,2,700,-70)
            fight.SpawHistoire(enemies,2,120,-80)
            fight.SpawHistoire(enemies,2,680,-90)
            fight.SpawHistoire(enemies,2,500,-100)
            fight.SpawHistoire(enemies,2,80,-110)
            fight.SpawHistoire(enemies,2,750,-120)
            fight.SpawHistoire(enemies,2,420,-130)
            fight.SpawHistoire(enemies,2,340,-140)
            fight.SpawHistoire(enemies,2,120,-150)
            numformation=11
        elif tempspasse > 39 and numformation==11:
            fight.SpawHistoire(enemies,2,const.SCREEN_WIDTH//2-50,20)
            fight.SpawHistoire(enemies,2,50,-20)
            fight.SpawHistoire(enemies,2,600,-30)
            fight.SpawHistoire(enemies,2,400,-40)
            fight.SpawHistoire(enemies,2,250,-50)
            fight.SpawHistoire(enemies,2,300,-60)
            fight.SpawHistoire(enemies,2,700,-70)
            fight.SpawHistoire(enemies,2,120,-80)
            fight.SpawHistoire(enemies,2,680,-90)
            fight.SpawHistoire(enemies,2,500,-100)
            fight.SpawHistoire(enemies,2,80,-110)
            fight.SpawHistoire(enemies,2,750,-120)
            fight.SpawHistoire(enemies,2,420,-130)
            fight.SpawHistoire(enemies,2,340,-140)
            fight.SpawHistoire(enemies,2,120,-150)
            numformation=12
        elif tempspasse > 44 and numformation==12:
            fight.SpawHistoire(enemies,1,50,-20)
            fight.SpawHistoire(enemies,1,100,-20)
            fight.SpawHistoire(enemies,1,75,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-50,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-75,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-100,-20)
            fight.SpawHistoire(enemies,1,150,-20)
            fight.SpawHistoire(enemies,1,200,-20)
            fight.SpawHistoire(enemies,1,175,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-150,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-200,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-175,-40)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2,-20)
            numformation=13
        elif tempspasse > 49 and numformation==13:
            fight.SpawHistoire(enemies,1,50,-20)
            fight.SpawHistoire(enemies,1,100,-20)
            fight.SpawHistoire(enemies,1,75,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-50,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-75,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-100,-20)
            fight.SpawHistoire(enemies,1,150,-20)
            fight.SpawHistoire(enemies,1,200,-20)
            fight.SpawHistoire(enemies,1,175,-40)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-150,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-200,-20)
            fight.SpawHistoire(enemies,1,const.SCREEN_WIDTH-175,-40)
            fight.SpawHistoire(enemies,5,const.SCREEN_WIDTH//2,-20)
            numformation=14
        elif tempspasse>55 and numformation==14:
            fight.SpawHistoire(enemies,4,120,-20)
            fight.SpawHistoire(enemies,4,580,-150)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2,-300)
            fight.SpawHistoire(enemies,4,700,-450)
            fight.SpawHistoire(enemies,4,260,-600)
            fight.SpawHistoire(enemies,4,440,-750)
            fight.SpawHistoire(enemies,4,360,-900)
            fight.SpawHistoire(enemies,4,230,-1050)
            fight.SpawHistoire(enemies,4,590,-1200)
            fight.SpawHistoire(enemies,4,const.SCREEN_WIDTH//2,-1350)
            numformation=15
        elif numformation==15 and len(enemies)==0:
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f)
            if temp['Histoire']==2:
                temp['Histoire']=3
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
        