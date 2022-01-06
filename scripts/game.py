import pygame, sys

from pygame.transform import smoothscale
from player import *
from weapons import *
from Enemy import *
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


<<<<<<< HEAD

LEVEL0 = [Tile(block,0,450),Tile(block,50,450),Tile(block,100,450),Tile(block,150,450),Tile(block,200,450)]
LEVEL0.append(Hide(100,400))
GROUND = [Tile(block,0,430),Tile(block,300,430),Tile(block,600,430),Tile(block,0,220),Tile(block,500,220)]

=======
>>>>>>> 2fe79df4ee418e99bd3ad6cf924d6666fcc3a546


def main():
    SCREENW = 800
    SCREENH = SCREENW* 0.6

    GROUND = [Tile(floor,0,480,SCREENW,105), Tile(lplat,0,210,250,46),Tile(rplat,550,210,250,46)]

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))


<<<<<<< HEAD
    random_spawn_timer = random.randint(1000,9000)
    enemy_movment = pygame.USEREVENT +1

    enemy_spawner = pygame.USEREVENT +2

    pygame.time.set_timer(enemy_spawner,random_spawn_timer)
    enemy_group = pygame.sprite.Group()








    bg = pygame.image.load("../sprites/bg.png")

=======
    bg = pygame.image.load("../sprites/background.png").convert()
    bg = pygame.transform.smoothscale(bg,(SCREENW,SCREENH))
>>>>>>> 2fe79df4ee418e99bd3ad6cf924d6666fcc3a546
    level_group = pygame.sprite.Group()

    for tile in LEVEL0:
        level_group.add(tile)

    player_group = pygame.sprite.GroupSingle()
    player = Player(GROUND,20,50,Gun())
    player_group.add(player)

    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT: sys.exit()

            if event.type == enemy_spawner:
                enemy_group.add(Enemy())

        screen.blit(bg,(0,0))
        level_group.draw(screen)
<<<<<<< HEAD
        player_group.update(LEVEL0)
=======
        player_group.update()
>>>>>>> 2fe79df4ee418e99bd3ad6cf924d6666fcc3a546
        player.draw_ui(screen)
        player_group.draw(screen)

        print(enemy_group)
        enemy_group.draw(screen)
        enemy_group.update()



        pygame.display.update()

main()
