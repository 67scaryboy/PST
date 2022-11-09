import pygame, sys
from pygame.locals import *
import random, personnages
import constantes as const

def Spawn(enemies,q):
    p = random.randint(0,100)
    if p < q:
        enemy  = personnages.Enemy(1)
        enemies.append(enemy)
