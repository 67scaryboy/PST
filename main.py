import pygame, sys
import mission1, mission2, mission3, mission4, mission5, mission6, mission7, mission8, mission9, mission10
from pygame.locals import *
import editeur, menu, fight, pickle, gc
import constantes as const

pygame.init()

gc.enable()                              #on à essayé de forcer le garbage collector
scoretotal = 0
pygame.mouse.set_visible(False)          #masque la souris
menu.ChoixSauvegarde()
with open('sauvegarde.pkl', 'rb') as f:  #charge les sauvegardes ou les écrase
    temp = pickle.load(f)
const.Niveau=temp['Histoire']
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    option = menu.ChoixMode()       #retourne 1 ou 2 en fonction du bouton cliqué

    if option == 1: #Mode arcade
        scoretotal += fight.Arcade()
    elif option == 2: #Mode histoire
        choix = menu.MenuHistoire() #Retourne le numero du niveau souhaité (1,2,...,9,10)
        if choix == 1:
            mission1.LancerMission1()
        elif choix== 2:
            mission2.LancerMission2()
        elif choix== 3:
            mission3.LancerMission3()
        elif choix== 4:
            mission4.LancerMission4()
        elif choix== 5:
            mission5.LancerMission5()
        elif choix== 6:
            mission6.LancerMission6()
        elif choix== 7:
            mission7.LancerMission7()
        elif choix== 8:
            mission8.LancerMission8()
        elif choix== 9:
            mission9.LancerMission9()
        elif choix== 10:
            mission10.LancerMission10()
    elif option == 3: #Mode éditeur
        editeur.MissionEditeur()