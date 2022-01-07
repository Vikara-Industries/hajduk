import pygame, sys
from pygame.sprite import spritecollideany

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




def main():
    SCREENW = 800
    SCREENH = SCREENW* 0.6

    GROUND = [Tile(floor,0,480,SCREENW,105), Tile(lplat,0,210,250,46),Tile(rplat,550,210,250,46)]
    COLIDABLES = [Hide(140,380),Portal(0,380),Portal(0,164),Hide(560,380),Portal(700,380),Portal(700,164)]


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))


    random_spawn_timer = random.randint(1000,9000)

    enemy_spawner = pygame.USEREVENT +2

    pygame.time.set_timer(enemy_spawner,random_spawn_timer)
    enemy_group = pygame.sprite.Group()



    bg = pygame.image.load("../sprites/background.png").convert()
    bg = pygame.transform.smoothscale(bg,(SCREENW,SCREENH))

    level_group = pygame.sprite.Group()
    interact_group = pygame.sprite.Group()

    for tile in COLIDABLES:
        interact_group.add(tile)
    for tile in GROUND:
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
        interact_group.draw(screen)
        player_group.update()
        player.draw_ui(screen)
        player_group.draw(screen)

        player.interact_with = pygame.sprite.spritecollideany(player, interact_group)

        if player.interact_with:
            player.interact_with.draw_prompt(screen)

        #print(enemy_group)
        enemy_group.draw(screen)
        enemy_group.update()



        pygame.display.update()

main()
