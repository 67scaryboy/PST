import pygame, sys, math, fight, time, cinematiques
from pygame.locals import *
import personnages, menu, bonus
import constantes as const    

def LancerMission1():

    FramePerSec = pygame.time.Clock()
    scoreArcade = 0
    alive = True
    dialogue = 1
    appui = False
    valeurs_cinematique = cinematiques.Cinematique1(menu.ChoixPerso())
    AP = menu.Arrièreplan(3)# 1 a 3 pour le fond
    AP.rect.center = valeurs_cinematique[3]
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP2.rect.center = valeurs_cinematique[2]
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    AP3.rect.center = valeurs_cinematique[1]
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(valeurs_cinematique[0])
    CP = personnages.Compagon(P1)
    bulle = menu.Affichage("sprites/bulletexte.png",const.SCREEN_WIDTH-270,100)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    cooldown = P1.cooldown
    P1.souris(personnages.DISPLAYSURF)

    enemies = [] 
    tirs = []
    explo = []
    boosts = []
    while True:
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
            texterect.center=(465,110)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("avancer sans support jusqu'au vaisseau ennemi !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,120)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==2:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Nous ne vous abandonnerons pas pour autant, même si on aurait", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("préferé...", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,110)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Vous êtes la dernière unitée combatante dont nous disposons,", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,120)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("croyez moi, ça ne m'enchante pas plus que vous.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==3:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Malgré votre QI d'huitre, je vais tenter de vous expliquer", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,90)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("simplement ce que vous devez faire:", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Evitez les tirs ennemis.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,110)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Trucidez-les avant qu'ils ne vous trucident.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,120)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Même vous, vous devriez avoir compris je pense.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==4:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Lorsqu'ils sont détruits, les vaisseaux aliens larguent des", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,90)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("composants appelés 'score'. Cherchez pas, ils sont fous ces aliens.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("A la fin de votre mission, vous pourrez vous servir  de ces", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,110)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("composants afin d'améliorer votre vaisseau. Nous vous mettrons", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,120)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("à disposition un atelier dédié. Evitez de le cassez...", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==5:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Votre vaisseau est équipé d'un protocole {SAVE THE PILOT}.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,90)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Vu que vous n'avez surement pas lu le manuel, je vais vous rappeler", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("ce que cela veut dire: même en cas de destruction, votre vaisseau", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,110)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("vous gardera en vie et mettra en sécurité les compostants récupérés.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,120)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Vous avez de la chance de disposer de ce prototype.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==6:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Je pense qu'on à fait le tour.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,90)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Des questions ?", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Oui ?", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,110)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("C'est dommage, c'est pas mon problème.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,120)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Bonne chance !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        else:
            break
                
        pygame.display.update()
        FramePerSec.tick(const.FPS)
    while alive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        #tir automatique
        if P1.cooldown == 0:
            shoot = fight.Projectile(P1,0,"sprites/tira.png")
            shootf= fight.Projectile(CP,0,"sprites/tira.png")
            tirs.append(shoot)
            tirs.append(shootf)
            P1.cooldown = cooldown
        else:
            P1.cooldown += -1

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
        menu.AfficheScore(scoreArcade) #Affichage score


        pygame.display.update()
        FramePerSec.tick(const.FPS)
        