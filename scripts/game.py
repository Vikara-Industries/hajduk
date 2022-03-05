import pygame, sys
from pygame.sprite import spritecollideany
from pygame import mixer

from player import *
from weapons import *
from NewEnemy import *
#from Enemy import *
from interactable import *



block = "./sprites/ground.png"
floor = "./sprites/invis.png"
lplat = "./sprites/invis.png"
rplat = "./sprites/invis.png"



class Tile(pygame.sprite.Sprite):
    def __init__(self,img,x,y,sx,sy):
        super(Tile,self).__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (sx,sy))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

class Scene:
    def __init__(self):
        self.colidables = []
        self.interactables = []
        self.enemies = []
        self.player = False
    
    def update(self):
        pass

level0 = Scene()
level0.colidables = [Tile(floor,0,480,800,95), Tile(lplat,0,230,275,46),Tile(rplat,530,230,275,46)]
level0.interactables = [Portal(0,385),Portal(0,180),Hide(140,380),Hide(560,380),Portal(720,385),Portal(720,180)]

def main():
    pygame.init()
    currentScene = level0
    ###### Music settings and scene specific song
    pygame.mixer.init()
    mixer.music.load("./Sound/The Underscore Orkestra - Balkan Nights.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.4)
    ######
    SCREENW = 800
    SCREENH = SCREENW* 0.6

    myfont = pygame.font.SysFont("monospace", 30)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))

####### IN SCEEN
    bg = pygame.image.load("./sprites/bg/full Level.png").convert()
    bg = pygame.transform.scale(bg,(SCREENW,SCREENH))


####### HANDLE THIS IN SCEENE.UPDATE()
    random_spawn_timer = random.randint(2000,6000)
    random_pickup_timer = random.randint(10000,15000)
    enemy_spawner = pygame.USEREVENT +2

    pickup_spawner = pygame.USEREVENT +3

    pygame.time.set_timer(enemy_spawner,random_spawn_timer)
    pygame.time.set_timer(pickup_spawner,random_pickup_timer)
    enemy_group = pygame.sprite.Group()
#######


####### POPULATE SPR GROUPS FROM SCEENE ARRAYS
    level_group = pygame.sprite.Group()
    interact_group = pygame.sprite.Group()
    player_group = pygame.sprite.GroupSingle()


    for tile in currentScene.interactables:
        interact_group.add(tile)
    for tile in currentScene.colidables:
        level_group.add(tile)
    
    player = Player(currentScene.colidables,currentScene.enemies,20,50,Gun())
    player_group.add(player)

#######

    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT: sys.exit()


######## HANDLE THIS IN SCEENE.UPDATE()
            if event.type == enemy_spawner:
                spawn = random.choice([(50,145),(50,345),(750,135),(750,345)])
                enemy = Enemy(spawn[0],spawn[1])
                currentScene.enemies.append(enemy)
                enemy_group.add(enemy)

            if event.type == pickup_spawner:
                spawn = random.choice([(190,185),(500,180),(350,400)])
                if random.random() > 0.4:
                    pickup = Ammo_box(spawn[0],spawn[1])
                else: pickup = Hp_box(spawn[0],spawn[1])
                interact_group.add(pickup)
########

        interact_group.update()
        player_group.update()
        enemy_group.update(player,currentScene.colidables)

        screen.blit(bg,(0,0))
        level_group.draw(screen)
        interact_group.draw(screen)
        player.draw_ui(screen,myfont)
        player_group.draw(screen)
        enemy_group.draw(screen)

####### PUT THIS IN PLAYER
        player.interact_with = None
        for colidable in interact_group:
            if colidable.rect.collidepoint(player.hitbox.center):
                if colidable == Ammo_box:
                    colidable.interact(player)
                player.interact_with = colidable
####### SEPERATE OUT UI
        if player.interact_with and not player.hiding:
            player.interact_with.draw_prompt(screen)

        pygame.display.update()
