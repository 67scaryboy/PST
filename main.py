import pygame, sys
from pygame.locals import *
import random, personnages, menu, fight
import constantes as const

pygame.init()


FramePerSec = pygame.time.Clock()

AP = menu.Arrièreplan()
MG = menu.MenuGauche()
#P1 = personnages.Player(menu.ChoixPerso())
P1 = personnages.Player(1)
E1 = personnages.Enemy(1)
CP = personnages.Compagon(P1)

enemies = [] 
enemies.append(E1)
tirs = []

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    P1.update()
    CP.update(P1)
    for entity in enemies:
        if entity.active == 1:
            entity.move()
            #ici pour décider si il tire
            p = random.randint(0,100)
            if p < 1:
                shoot = fight.Projectile(entity)
                tirs.append(shoot)
            if entity.rect.bottom > const.SCREEN_HEIGHT:
                enemies.remove(entity)
    for shoot in tirs:
        shoot.move()
        if shoot.rect.bottom > const.SCREEN_HEIGHT:
                tirs.remove(shoot)
    
    AP.move()

    fight.Spawn(enemies,2)

    personnages.DISPLAYSURF.fill(const.WHITE)
    AP.draw(personnages.DISPLAYSURF)

    for shoot in tirs:
        personnages.DISPLAYSURF.blit(entity.image, entity.rect)
        shoot.draw(personnages.DISPLAYSURF)

    for entity in enemies:
        if entity.active == 1:
            personnages.DISPLAYSURF.blit(entity.image, entity.rect)
            entity.draw(personnages.DISPLAYSURF)
    P1.draw(personnages.DISPLAYSURF)
    CP.draw(personnages.DISPLAYSURF)
    MG.draw(personnages.DISPLAYSURF)


    pygame.display.update()
    FramePerSec.tick(const.FPS)
