import pygame, sys
from player import *
from weapons import *

def main():
    SCREENW = 800
    SCREENH = 600

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREENW,SCREENH))

    bg = pygame.image.load("bg.png")
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
        pygame.display.update()
        
main()