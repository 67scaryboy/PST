import pygame, sys
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
        menu.MenuHistoire()