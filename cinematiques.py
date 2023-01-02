import pygame, sys, math, fight, time
from pygame.locals import *
import personnages, menu, bonus
import constantes as const

def Cinematique1(numero):#utiliser numero pour modifier image vaisseau 
    FramePerSec = pygame.time.Clock()
    montee = 0
    deplacementlaser=0
    descente = 0

    AP = menu.Arrièreplan(3)# 1 a 3 pour le fond
    AP2= menu.Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP3= menu.Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    PNJ1 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2)-200,const.SCREEN_HEIGHT-100)
    PNJ2 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2)-100,const.SCREEN_HEIGHT-150)
    PNJ3 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2),const.SCREEN_HEIGHT-200)
    PNJ4 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2)+100,const.SCREEN_HEIGHT-150)
    PNJ5 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2)+200,const.SCREEN_HEIGHT-100)
    Laser = menu.Affichage("sprites_animation/laser1.png",(const.SCREEN_WIDTH/2)-110,10)
    Boss = menu.Affichage("sprites/b1.png",(const.SCREEN_WIDTH),-200)
    bulle = menu.Affichage("sprites/bulletexte.png",const.SCREEN_WIDTH-270,100)
    partie = 1
    PNJs = [PNJ1,PNJ2,PNJ3,PNJ4,PNJ5]
    explo = []

    while partie == 1: #les vaisseaux sont détruits par le boss final
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        AP3.move(3)
        AP2.move(2)
        AP.move(1)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        PNJ1.mouvement(0,montee)
        PNJ2.mouvement(0,montee)
        PNJ3.mouvement(0,montee)
        PNJ4.mouvement(0,montee)
        PNJ5.mouvement(0,montee)
        Boss.mouvement(0, descente)
        Laser.mouvement(deplacementlaser,0)
        
        for PNJ in PNJs:
            PNJ.draw(personnages.DISPLAYSURF)

        if PNJ1.rect.top >= 250:
            montee = -2
        elif PNJ1.rect.top >=200:
            PNJs.append(Laser)
            deplacementlaser = 10
            menu.Animation(const.laserboss,Laser)
            if Laser.rect.center[0] == (const.SCREEN_WIDTH/2)-100:
                explo.append(menu.explosion(PNJ2))
                PNJs.remove(PNJ2)
            elif Laser.rect.center[0]  == (const.SCREEN_WIDTH/2):
                explo.append(menu.explosion(PNJ3))
                PNJs.remove(PNJ3)
            elif Laser.rect.center[0]  == (const.SCREEN_WIDTH/2)+100:
                explo.append(menu.explosion(PNJ4))
                PNJs.remove(PNJ4)
        elif PNJ1.rect.top < 200:
            montee = 0
            menu.Animation(const.laserboss,Laser)
            if Laser.rect.center[0]  == (const.SCREEN_WIDTH/2)+200:
                explo.append(menu.explosion(PNJ5))
                PNJs.remove(PNJ5)
            elif Laser.rect.center[0]  == (const.SCREEN_WIDTH):
                PNJs.append(Boss)
                descente = 12
            elif Laser.rect.center[0] == (const.SCREEN_WIDTH) + 100:
                deplacementlaser = 0
            
            if Boss.rect.top > (const.SCREEN_HEIGHT):
                descente = 0
                partie = 2
        menu.aff_explo(explo)
        for boom in explo:
            menu.Animation(const.explosions,boom)

        pygame.display.update()
        FramePerSec.tick(const.FPS)
    while partie == 2: #le vaisseau se place à la position de début de jeu
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        AP3.move(3)
        AP2.move(2)
        AP.move(1)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        PNJ1.draw(personnages.DISPLAYSURF)
        if PNJ1.rect.center[0] < (const.SCREEN_WIDTH/2):
            PNJ1.mouvement(2, 3)
        elif PNJ1.rect.center[1] < (const.SCREEN_HEIGHT)-200:
            PNJ1.mouvement(0,1)
        else:
            partie = 3 

        pygame.display.update()
        FramePerSec.tick(const.FPS)

    return [numero,AP3.rect.center,AP2.rect.center,AP.rect.center]


def MortBoss(P1,Body,AP,AP2,AP3):
    FramePerSec = pygame.time.Clock()
    rec = True
    while rec:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        AP3.move(3)
        AP2.move(2)
        AP.move(1)

        if Body.rect.center[1] > -200:
            Body.rect.move_ip(0,-2)
        else:
            rec = False

        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        P1.draw(personnages.DISPLAYSURF)
        Body.draw(personnages.DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(const.FPS)
    
    pygame.mouse.set_pos(P1.rect.center[0],P1.rect.center[1])
    return AP.rect.center, AP2.rect.center, AP3.rect.center

def ArriveBoss(P1,AP,AP2,AP3):
    FramePerSec = pygame.time.Clock()
    rec = True
    PNJ1 = menu.Affichage("sprites_boss/boss.png",(const.SCREEN_WIDTH//2),-200)
    tempsdemarrage = time.time()
    alerterouge=menu.Affichage("sprites_animation/Alerte1.png",const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT//2)
    alerterouge.draw(personnages.DISPLAYSURF)

    while rec:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        AP3.move(3)
        AP2.move(2)
        AP.move(1)
        
        
        if PNJ1.rect.center[1] < 80:
            PNJ1.rect.move_ip(0,2)
        else:
            rec = False
        
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        P1.draw(personnages.DISPLAYSURF)
        PNJ1.draw(personnages.DISPLAYSURF)
        menu.Animation(const.alerte,alerterouge)
        alerterouge.draw(personnages.DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(const.FPS)

    pygame.mouse.set_pos(P1.rect.center[0],P1.rect.center[1])
    return AP.rect.center, AP2.rect.center, AP3.rect.center