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
            texte=font.render("...", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Malheureusement, le temps que vous le rejoignez l'escadron", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("à été pris en embuscade... Et il semblerait que la formation", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("d'1h30 au pilotage n'est pas été suffisante.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==2:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Au moins ils sont morts en défendant une cause juste :", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("l'intégrité de nos précieux originaux de 'Space inviders'.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Jamais nous ne laisserons les aliens nous les dérober !", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
        elif dialogue==3:
            font = pygame.font.SysFont("arial", 13)
            texte=font.render("Il semblerait que leurs assaillants soient toujours dans les", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,85)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("parages. Soyez prudent, restez discret et tâchez de ne pas", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,100)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("vous faire repérer.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,115)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("Ouvrez le feu uniquement quand vous avez les ennemis dans", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,130)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render("le viseur.", True, const.BLACK)
            texterect=texte.get_rect()
            texterect.center=(465,145)
            personnages.DISPLAYSURF.blit(texte,texterect)
        else:
            tempsdemarrage = time.time() #A mettre ici, sinon les adversaires risquent de spawn pendant le dialogue.
            #pygame.mixer.music.load("sons/Mission5.mp3")
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
        
        tempspasse = time.time() - tempsdemarrage

        if tempspasse > 3 and numformation==0:
            personnages.poser_debrits(debrits, 1, 40, -40, 2, numformation)
            personnages.poser_debrits(debrits, 1, 120, -40, 45, numformation)
            personnages.poser_debrits(debrits, 1, 210, -40, -20, numformation)
            personnages.poser_debrits(debrits, 1, 300, -40, 75, numformation)
            personnages.poser_debrits(debrits, 1, 390, -40, -86, numformation)
            personnages.poser_debrits(debrits, 1, 480, -40, 25, numformation)
            personnages.poser_debrits(debrits, 1, 570, -40, 12, numformation)
            personnages.poser_debrits(debrits, 1, 660, -40, 12, numformation)

            personnages.poser_debrits(debrits, 1, 760, -250, 22, numformation)
            personnages.poser_debrits(debrits, 1, 670, -250, -35, numformation)
            personnages.poser_debrits(debrits, 1, 580, -250, 70, numformation)
            personnages.poser_debrits(debrits, 1, 390, -250, 65, numformation)
            personnages.poser_debrits(debrits, 1, 300, -250, 120, numformation)
            personnages.poser_debrits(debrits, 1, 210, -250, 219, numformation)
            personnages.poser_debrits(debrits, 1, 120, -250, 175, numformation)
            personnages.poser_debrits(debrits, 1, 30, -250, 2, numformation)
            numformation=1
        elif tempspasse > 6 and numformation == 1:
            personnages.poser_debrits(debrits, 2, -30, -50, 10, numformation)
            debrits[-1].chgtTraj(1)
            personnages.poser_debrits(debrits, 2, 830, -80, -10, numformation)
            debrits[-1].chgtTraj(2)
            personnages.poser_debrits(debrits, 2, 1000, 500, 90, numformation)
            debrits[-1].chgtTraj(4)
            personnages.poser_debrits(debrits, 2, -200, 300, 45, numformation)
            debrits[-1].chgtTraj(3)
            personnages.poser_debrits(debrits, 2, -30, 850, 75, numformation)
            debrits[-1].chgtTraj(6)
            personnages.poser_debrits(debrits, 2, 840, 870, 145, numformation)
            debrits[-1].chgtTraj(5)

            numformation = 2
        elif tempspasse > 10 and numformation == 2:
            personnages.poser_debrits(debrits, 2, 760, -90, 50, numformation)
            personnages.poser_debrits(debrits, 2, 660, -70, 47, numformation)
            personnages.poser_debrits(debrits, 2, 560, -50, 60, numformation)
            personnages.poser_debrits(debrits, 2, 460, -70, -30, numformation)
            personnages.poser_debrits(debrits, 2, 360, -90, 130, numformation)

            numformation = 3
        elif len(debrits) == 0 and numformation==3: #combat de boss
            boss.Boss2(P1, score,AP3,AP2,AP,VaisseauChoisis)
            numformation=15
        elif numformation==15: #victoire
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f)
            if temp['Histoire']==6:
                temp['Histoire']=7
            with open('sauvegarde.pkl', 'wb') as f:
                    pickle.dump(temp, f)
            pygame.mixer.music.fadeout(10000)
            menu.MenuFinPartie(score,True)
            break
        
        for entity in debrits: #Déplacement des ennemis 
            entity.move()
            if entity.rect.top > const.SCREEN_HEIGHT and entity.direction[1] > 0:
                debrits.remove(entity)
            elif entity.rect.bottom < 0 and entity.direction[1] < 0:
                debrits.remove(entity)
            elif entity.direction[1] == 0:
                if entity.rect.right < 0 and entity.direction[0] < 0:
                    debrits.remove(entity)
                elif entity.rect.left > const.SCREEN_WIDTH and entity.direction[0] > 0:
                    debrits.remove(entity)
                

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
        