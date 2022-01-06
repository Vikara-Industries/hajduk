import pygame, sys
from player import *
from weapons import *
from Enemy import *

from interactable import *


block = "../sprites/ground.png"
class Tile(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        super(Tile,self).__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)


LEVEL0 = [Tile(block,0,450),Tile(block,50,450),Tile(block,100,450),Tile(block,150,450),Tile(block,200,450)]
LEVEL0.append(Hide(100,400))


def main():
    SCREENW = 800
    SCREENH = SCREENW* 0.6

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))


    random_spawn_timer = random.randint(1000,9000)
    enemy_movment = pygame.USEREVENT +1

    enemy_spawner = pygame.USEREVENT +2

    pygame.time.set_timer(enemy_spawner,random_spawn_timer)
    enemy_group = pygame.sprite.Group()








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

            if event.type == enemy_spawner:
                enemy_group.add(Enemy())

        screen.blit(bg,(0,0))
        level_group.draw(screen)
        player_group.update(LEVEL0)
        player.draw_ui(screen)
        player_group.draw(screen)

        print(enemy_group)
        enemy_group.draw(screen)
        enemy_group.update()



        pygame.display.update()

main()
