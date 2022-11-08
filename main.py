import pygame, sys
from pygame.locals import *
import random
import personnages
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()


MG = Personnages.MenuGauche()
P1 = Personnages.Player()
E1 = Personnages.Enemy()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    E1.move()

    Personnages.DISPLAYSURF.fill(Personnages.WHITE)
    P1.draw(Personnages.DISPLAYSURF)    
    E1.draw(Personnages.DISPLAYSURF)
    MG.draw(Personnages.DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)
