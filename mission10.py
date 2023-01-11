import pygame, sys, math, fight
from pygame.locals import *
import personnages, menu, bonus
import constantes as const

def LancerMission10():
    FramePerSec = pygame.time.Clock()
    scoreArcade = 0
    alive = True

    AP = menu.Arrièreplan(3)# 1 a 3 pour le fond
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(menu.ChoixPerso())
    CP = personnages.Compagon(P1)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    P1.souris(personnages.DISPLAYSURF)

    cooldown = P1.cooldown

    enemies = [] 
    tirs = []
    explo = []
    boosts = []

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
        