import pygame, sys
from pygame.locals import *
import random, personnages, menu, fight
import constantes as const

pygame.init()

scoretotal = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    scoretotal += fight.Arcade()