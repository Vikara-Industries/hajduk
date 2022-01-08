import pygame, sys
from pygame.sprite import spritecollideany

from pygame.transform import smoothscale
from player import *
from weapons import *
from Enemy import *
#from Enemy import *
from interactable import *


block = "../sprites/ground.png"
floor = "../sprites/invis.png"
lplat = "../sprites/invis.png"
rplat = "../sprites/invis.png"



class Tile(pygame.sprite.Sprite):
    def __init__(self,img,x,y,sx,sy):
        super(Tile,self).__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (sx,sy))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)




def main():
    SCREENW = 800
    SCREENH = SCREENW* 0.6

    GROUND = [Tile(floor,0,480,SCREENW,95), Tile(lplat,0,230,275,46),Tile(rplat,520,230,270,46)]
    COLIDABLES = [Portal(0,385),Portal(0,180),Hide(140,380),Hide(560,380),Portal(720,385),Portal(720,180)]


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))


    random_spawn_timer = random.randint(3000,4000)

    enemy_spawner = pygame.USEREVENT +2

    pygame.time.set_timer(enemy_spawner,random_spawn_timer)
    enemy_group = pygame.sprite.Group()



    bg = pygame.image.load("../sprites/bg/full Level.png").convert()
    bg = pygame.transform.scale(bg,(SCREENW,SCREENH))

    level_group = pygame.sprite.Group()
    interact_group = pygame.sprite.Group()

    for tile in COLIDABLES:
        interact_group.add(tile)
    for tile in GROUND:
        level_group.add(tile)


    player_group = pygame.sprite.GroupSingle()
    player = Player(GROUND,20,50,Gun())
    player_group.add(player)





    spawn_counter = 0
    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT: sys.exit()

            if event.type == enemy_spawner:
                spawn_counter +=1
                #print(spawn_counter)
                enemy_group.add(Enemy(spawn_counter))
                spawn_counter -= 1



        screen.blit(bg,(0,0))
        level_group.draw(screen)
        interact_group.draw(screen)
        player_group.update()
        player.draw_ui(screen)
        player_group.draw(screen)



        #print(len(position_enemy))

        player.interact_with = pygame.sprite.spritecollideany(player, interact_group)

        if player.interact_with:
            player.interact_with.draw_prompt(screen)

        #print(enemy_group)
        enemy_group.update()
        #enemy_group.draw(screen)





        pygame.display.update()

main()
