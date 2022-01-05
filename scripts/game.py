import pygame, sys
from player import *
from weapons import *

block = "../sprites/ground.png"
class Tile(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        super(Tile,self).__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


LEVEL0 = [Tile(block,0,400),]

def main():
    SCREENW = 800
    SCREENH = 600

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))


    bg = pygame.image.load("../sprites/bg.png")

    level_group = pygame.sprite.Group()

    for tile in LEVEL0:
        level_group.add(tile)

    player_group = pygame.sprite.GroupSingle()
    player = Player(20,50,Gun())
    player_group.add(player)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: sys.exit()
        screen.blit(bg,(0,0))
        player_group.update()
        player.draw_ui(screen)
        player_group.draw(screen)
        level_group.draw(screen)

        pygame.display.update()
        
main()