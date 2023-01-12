import pygame, sys, math, fight, time, cinematiques, pickle, random, boss
from pygame.locals import *
import personnages, menu, bonus, gc
import constantes as const    

def LancerMission7():
    pygame.mixer.music.stop()
    FramePerSec = pygame.time.Clock()
    score = 0
    alive = True
    dialogue = 1
    numformation=0
    appui = False
    VaisseauChoisis = menu.ChoixPerso()
    AP = menu.Arrièreplan(2)# 1 a 3 pour le fond
    AP2= menu.Arrièreplan(4)# 4 ou 5 pour le paralax profond
    AP3= menu.Arrièreplan(7)# 6 ou 7 pour le paralax superieur
    MB = menu.Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+130)
    P1 = personnages.Player(VaisseauChoisis)
    CP = personnages.Compagon(P1)
    bulle = menu.Affichage("sprites/bulletexte.png",const.SCREEN_WIDTH-270,110)
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    P1.souris(personnages.DISPLAYSURF)
    cooldown = P1.cooldown

    debrits = []
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
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
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
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
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
        elif dialogue==3:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
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
        
        tempspasse = time.time() - tempsdemarrage

        if tempspasse > 5 and numformation==0:
            personnages.poser_debrits(debrits, 1, 5, 5, 0)
            numformation=1
        elif numformation==15: #ne la faire passer à 15 qu'après le combat de boss
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f)
            if temp['Histoire']==6:
                temp['Histoire']=7
            with open('sauvegarde.pkl', 'wb') as f:
                    pickle.dump(temp, f)
            pygame.mixer.music.fadeout(10000)
            menu.MenuFinPartie(score,True)
            break
        
        alive = personnages.crash(debrits, P1, alive)

        ###Partie graphique###
        personnages.DISPLAYSURF.fill(const.WHITE)

        #Déplacement et affichage des images de fond
        AP3.move(3)#vitesse de déplacement des couches
        AP2.move(2)
        AP.move(1)#laisser 1 pour le fond, sinon ca file la gerbe
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)

        #Affichage des obstacles restants
        for entity in debrits:
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
        pygame.mixer.music.fadeout(10000)
        menu.MenuFinPartie(score,False)#Dans le menu, le score est ajouté comme argent
        