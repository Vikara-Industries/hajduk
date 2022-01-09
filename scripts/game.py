import pygame, sys
from pygame.sprite import spritecollideany

from pygame.transform import smoothscale
from player import *
from weapons import *
from NewEnemy import *
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
    pygame.init()


    SCREENW = 800
    SCREENH = SCREENW* 0.6

    myfont = pygame.font.SysFont("monospace", 30)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))

    GROUND = [Tile(floor,0,480,SCREENW,95), Tile(lplat,0,230,275,46),Tile(rplat,530,230,275,46)]
    COLIDABLES = [Portal(0,385),Portal(0,180),Hide(140,380),Hide(560,380),Portal(720,385),Portal(720,180)]
    COLIDABLES.append(Ammo_box(250,385))
    COLIDABLES.append(Hp_box(350,385))
    ENEMIES = []




    random_spawn_timer = random.randint(2000,6000)
    random_pickup_timer = random.randint(10000,15000)
    enemy_spawner = pygame.USEREVENT +2

    pickup_spawner = pygame.USEREVENT +3

    pygame.time.set_timer(enemy_spawner,random_spawn_timer)
    pygame.time.set_timer(pickup_spawner,random_pickup_timer)
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
    player = Player(GROUND,ENEMIES,20,50,Gun())
    player_group.add(player)





    #spawn_counter = 0
    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT: sys.exit()

            if event.type == enemy_spawner:
                #spawn_counter +=1
                #print(spawn_counter)
                spawn = random.choice([(50,145),(50,345),(750,135),(750,345)])
                enemy = Enemy(spawn[0],spawn[1])#spawn_counter)
                ENEMIES.append(enemy)
                enemy_group.add(enemy)
                #spawn_counter -= 1

            if event.type == pickup_spawner:
                spawn = random.choice([(190,185),(500,180),(350,400)])
                if random.random() > 0.4:
                    pickup = Ammo_box(spawn[0],spawn[1])
                else: pickup = Hp_box(spawn[0],spawn[1])
                interact_group.add(pickup)


        screen.blit(bg,(0,0))
        level_group.draw(screen)
        interact_group.update()
        interact_group.draw(screen)

        player_group.update()
        player.draw_ui(screen,myfont)
        player_group.draw(screen)



        #print(len(position_enemy))
        player.interact_with = None
        for colidable in interact_group:
            if colidable.rect.collidepoint(player.hitbox.center):
                if colidable == Ammo_box:
                    colidable.interact(player)
                player.interact_with = colidable

        if player.interact_with and not player.hiding:
            player.interact_with.draw_prompt(screen)

        #print(enemy_group)
        enemy_group.update(player,GROUND)
        enemy_group.draw(screen)

        pygame.display.update()

main()
