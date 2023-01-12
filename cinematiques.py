import pygame, sys, math, fight, time
from pygame.locals import *
import personnages, menu, bonus
import constantes as const

def Cinematique1(numero):                       #Cinématique du début du mode histoire
    FramePerSec = pygame.time.Clock()
    montee = 0
    deplacementlaser=0
    descente = 0

    AP = menu.Arrièreplan(3)# 
    AP2= menu.Arrièreplan(5)#Arrière plan (Paralax)
    AP3= menu.Arrièreplan(6)#
    PNJ1 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2)-200,const.SCREEN_HEIGHT-100)   #
    PNJ2 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2)-100,const.SCREEN_HEIGHT-150)   #
    PNJ3 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2),const.SCREEN_HEIGHT-200)       #Escadron
    PNJ4 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2)+100,const.SCREEN_HEIGHT-150)   #
    PNJ5 = menu.Affichage("sprites/p"+str(numero)+".png",(const.SCREEN_WIDTH/2)+200,const.SCREEN_HEIGHT-100)   #
    Laser = menu.Affichage("sprites_animation/laser1.png",(const.SCREEN_WIDTH/2)-110,10)     #Laser du Boss
    Boss = menu.Affichage("sprites/b1.png",(const.SCREEN_WIDTH),-200)                        #Boss
    bulle = menu.Affichage("sprites/bulletexte.png",const.SCREEN_WIDTH-270,100)              #Bulle de dialogue
    partie = 1
    PNJs = [PNJ1,PNJ2,PNJ3,PNJ4,PNJ5]
    explo = []

    while partie == 1:                       #les vaisseaux sont détruits par le boss final
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        AP3.move(3) #
        AP2.move(2) #défilement de l'arrière plan
        AP.move(1)  #
        AP.draw(personnages.DISPLAYSURF)  #
        AP2.draw(personnages.DISPLAYSURF) #Affichage de l'arrière plan
        AP3.draw(personnages.DISPLAYSURF) #
        PNJ1.mouvement(0,montee) #
        PNJ2.mouvement(0,montee) #
        PNJ3.mouvement(0,montee) #Mouvement de montée de l'escadron
        PNJ4.mouvement(0,montee) #
        PNJ5.mouvement(0,montee) #
        Boss.mouvement(0, descente) #Mouvement de descente du boss
        Laser.mouvement(deplacementlaser,0) #Balayage du laser
        
        for PNJ in PNJs:
            PNJ.draw(personnages.DISPLAYSURF) #Affichage des personnages

        if PNJ1.rect.top >= 250:                                      #Tant que le PNJ1 n'a pas atteind une certaine hauteur
            montee = -2                                                 #L'escadron continue de monter
        elif PNJ1.rect.top >=200:                                     #lorsque une certaine hauteur est atteinte
            PNJs.append(Laser)                                          #le laser est aussi affiché
            deplacementlaser = 10                                       #le laser commence à se déplacer
            menu.Animation(const.laserboss,Laser)
            if Laser.rect.center[0] == (const.SCREEN_WIDTH/2)-100:    #lorsque le laser atteinds une certaine position
                explo.append(menu.explosion(PNJ2))                      #faire exploser le PNJ2
                PNJs.remove(PNJ2)
            elif Laser.rect.center[0]  == (const.SCREEN_WIDTH/2):     #lorsque le laser atteinds une certaine position
                explo.append(menu.explosion(PNJ3))                      #faire exploser le PNJ3
                PNJs.remove(PNJ3)
            elif Laser.rect.center[0]  == (const.SCREEN_WIDTH/2)+100: #lorsque le laser atteinds une certaine position
                explo.append(menu.explosion(PNJ4))                      #faire exploser le PNJ4
                PNJs.remove(PNJ4)
        elif PNJ1.rect.top < 200:                                     #lorsque le PNJ1 atteinds une certaine position
            montee = 0                                                  #l'escadron arrête de monter
            menu.Animation(const.laserboss,Laser) #animation du laser
            if Laser.rect.center[0]  == (const.SCREEN_WIDTH/2)+200:   #lorsque le laser atteinds une certaine position
                explo.append(menu.explosion(PNJ5))                      #faire exploser le PNJ5
                PNJs.remove(PNJ5)
            elif Laser.rect.center[0]  == (const.SCREEN_WIDTH):       #lorsque le laser atteinds une certaine position
                PNJs.append(Boss)                                       #le boss est aussi affiché
                descente = 12                                           #le boss commence à descendre
            elif Laser.rect.center[0] == (const.SCREEN_WIDTH) + 100:  #lorsque le laser atteinds une certaine position
                deplacementlaser = 0                                    #il arrête de se déplacer 
            
            if Boss.rect.top > (const.SCREEN_HEIGHT):                 #lorsque le boss atteinds une certaine position
                descente = 0                                            #il arrête de descendre
                partie = 2                                              #passage à la dauxième partie
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
        
        AP3.move(3) #
        AP2.move(2) #défilement de l'arrièreplan
        AP.move(1)  #

        #Affichage
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        PNJ1.draw(personnages.DISPLAYSURF)

        if PNJ1.rect.center[0] < (const.SCREEN_WIDTH/2):         #tant que le PNJ1 n'a pas atteinds une certaine position
            PNJ1.mouvement(2, 3)                                    #il se déplace
        elif PNJ1.rect.center[1] < (const.SCREEN_HEIGHT)-200:    #tant que le PNJ1 n'a pas atteinds une certaine position
            PNJ1.mouvement(0,1)                                     #il se déplace
        else:
            partie = 3                                           #passage à la troisième partie

        pygame.display.update()
        FramePerSec.tick(const.FPS)

    return [numero,AP3.rect.center,AP2.rect.center,AP.rect.center] #on renvoit les informations nécéssaires à la continuité du défilement de l'arrière plan et du vaisseau


def MortBoss(P1,Body,AP,AP2,AP3): #cinématique de mort du Boss Modulaire
    FramePerSec = pygame.time.Clock()
    rec = True
    while rec:                            #tant que la cinématique est en cours
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        AP3.move(3)
        AP2.move(2)
        AP.move(1)

        if Body.rect.center[1] > -200:   #tant que le Boss n'est pas à une certaine position
            Body.rect.move_ip(0,-2)         #bouger le boss
        else:
            rec = False                  #mettre fin à la cinématique

        #Affichage
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        P1.draw(personnages.DISPLAYSURF)
        Body.draw(personnages.DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(const.FPS)
    
    pygame.mouse.set_pos(P1.rect.center[0],P1.rect.center[1]) #calibrage de la souris sur la position du sprite du joueur
    return AP.rect.center, AP2.rect.center, AP3.rect.center

def ArriveBoss1(P1,AP,AP2,AP3):  #cinématique d'arrivée du Boss modulaire
    pygame.mouse.set_pos(P1.rect.center[0],P1.rect.center[1]) #calibrage de la souris sur la position du sprite du joueur
    FramePerSec = pygame.time.Clock()
    rec = True
    PNJ1 = menu.Affichage("sprites_boss/boss.png",(const.SCREEN_WIDTH//2),-200)     #sprite du boss
    tempsdemarrage = time.time()
    alerterouge=menu.Affichage("sprites_animation/Alerte1.png",const.SCREEN_WIDTH//2+80,const.SCREEN_HEIGHT//2) #sprite de l'alerte
    alerterouge.draw(personnages.DISPLAYSURF)

    while rec: #Tant que la cinématique est en cours
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        AP3.move(3) #
        AP2.move(2) #défilement de l'arrière plan
        AP.move(1)  #
        
        
        if PNJ1.rect.center[1] < 80:               #tant que le boss n'a pas atteinds une certaine position
            PNJ1.rect.move_ip(0,2)                  #bouger le boss
        else:
            rec = False                            #arrêter la cinématique
        
        #Affichage
        AP.draw(personnages.DISPLAYSURF) 
        AP2.draw(personnages.DISPLAYSURF)  
        AP3.draw(personnages.DISPLAYSURF)  
        P1.souris(personnages.DISPLAYSURF) #mouvement du joueur
        PNJ1.draw(personnages.DISPLAYSURF) 
        menu.Animation(const.alerte,alerterouge)  #animation du logo d'alerte
        alerterouge.draw(personnages.DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(const.FPS)

    pygame.mouse.set_pos(P1.rect.center[0],P1.rect.center[1]) #calibrage de la souris sur la position du sprite du joueur
    return AP.rect.center, AP2.rect.center, AP3.rect.center