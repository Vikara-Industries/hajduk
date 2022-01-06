import pygame, sys

from pygame.transform import smoothscale
from player import *
from weapons import *
#from Enemy import *
from interactable import *


block = "../sprites/ground.png"
floor = "../sprites/floor.png"
lplat = "../sprites/left platform.png"
rplat = "../sprites/right platform.png"

class Tile(pygame.sprite.Sprite):
    def __init__(self,img,x,y,sx,sy):
        super(Tile,self).__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.smoothscale(self.image, (sx,sy))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)



def main():
    SCREENW = 800
    SCREENH = SCREENW* 0.6

    GROUND = [Tile(floor,0,480,SCREENW,105), Tile(lplat,0,210,250,46),Tile(rplat,550,210,250,46)]

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))


    bg = pygame.image.load("../sprites/background.png").convert()
    bg = pygame.transform.smoothscale(bg,(SCREENW,SCREENH))
    level_group = pygame.sprite.Group()

    for tile in GROUND:
        level_group.add(tile)

    player_group = pygame.sprite.GroupSingle()
    player = Player(GROUND,20,50,Gun())
    player_group.add(player)

    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT: sys.exit()

        screen.blit(bg,(0,0))
        level_group.draw(screen)
        player_group.update()
        player.draw_ui(screen)
        player_group.draw(screen)

        pygame.display.update()

main()
