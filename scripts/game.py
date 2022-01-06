import pygame, sys
from player import *
from weapons import *
#from Enemy import *
from interactable import *


block = "../sprites/ground.png"
class Tile(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        super(Tile,self).__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)


GROUND = [Tile(block,0,430),Tile(block,300,430),Tile(block,600,430),Tile(block,0,220),Tile(block,500,220)]


def main():
    SCREENW = 800
    SCREENH = SCREENW* 0.6

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))


    bg = pygame.image.load("../sprites/bg.png")

    level_group = pygame.sprite.Group()

    for tile in GROUND:
        level_group.add(tile)

    player_group = pygame.sprite.GroupSingle()
    player = Player(20,50,Gun())
    player_group.add(player)

    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT: sys.exit()

        screen.blit(bg,(0,0))
        level_group.draw(screen)
        player_group.update(GROUND)
        player.draw_ui(screen)
        player_group.draw(screen)

        pygame.display.update()

main()
