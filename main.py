import pygame, sys
from pygame.locals import *
import random, personnages, menu
import constantes as const

pygame.init()


FramePerSec = pygame.time.Clock()

AP = menu.Arrièreplan()
MG = menu.MenuGauche()
P1 = personnages.Player()
E1 = personnages.Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    P1.update()
    for entity in enemies:
        personnages.DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    AP.move()

    personnages.DISPLAYSURF.fill(const.WHITE)
    AP.draw(personnages.DISPLAYSURF)
    E1.draw(personnages.DISPLAYSURF)
    P1.draw(personnages.DISPLAYSURF)    
    MG.draw(personnages.DISPLAYSURF)
    

    pygame.display.update()
    FramePerSec.tick(const.FPS)
