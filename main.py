import pygame, sys
import mission1
from pygame.locals import *
import random, personnages, menu, fight, bonus, boss
import constantes as const

pygame.init()

scoretotal = 0
pygame.mouse.set_visible(False)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    option = menu.ChoixMode()

    if option == 1:
        scoretotal += fight.Arcade()
    elif option == 2:
        choix = menu.MenuHistoire(const.Niveau) #Retourne le numero du niveau souhaité (1,2,...,9,10) - 1
        choix += 1
        if choix == 1:
            mission1.LancerMission1()
        #scoretotal += boss.Bossfight()