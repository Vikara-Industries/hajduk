import pygame, random
from pygame import mixer

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy,self).__init__()
        #animation
        if y > 300:
            self.xrange =(30,780)
        elif x< 100:
            self.xrange =(30,280)
        else:
            self.xrange =(520,780)

        if x < 300:  self.flip = False
        else:        self.flip = True
        self.anim_speed = 0.2
        self.animation_list = [pygame.image.load("./sprites/turk/Stand.png").convert_alpha()]

        self.idle = [pygame.image.load("./sprites/turk/Stand.png").convert_alpha(),pygame.image.load("./sprites/turk/Stand.png").convert_alpha()]
        self.stand_timer = 0
        self.aiming = False
        self.aim = [pygame.image.load("./sprites/turk/aim.png").convert_alpha(),pygame.image.load("./sprites/turk/aim.png").convert_alpha()]

        self.moving = False
        self.walking = []
        self.walking.append(pygame.image.load("./sprites/turk/walk 1.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/turk/walk 2.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/turk/walk 3.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/turk/walk 4.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/turk/walk 5.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/turk/walk 6.png").convert_alpha())

        self.gunshot_sound = mixer.Sound("./Sound/gunshot.mp3")
        self.shooting = False
        self.shooting_freeze = 0
        self.shooting_anim = []
        self.shooting_anim.append(pygame.image.load("./sprites/turk/shoot 1.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("./sprites/turk/shoot 2.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("./sprites/turk/shoot 3.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("./sprites/turk/shoot 4.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("./sprites/turk/shoot 5.png").convert_alpha())

        self.died = False
        self.death_timer = 0
        self.death_anim = []
        self.death_anim.append(pygame.image.load("./sprites/turk/death 1.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/turk/death 2.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/turk/death 3.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/turk/death 4.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/turk/death 5.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/turk/death 6.png").convert_alpha())


        self.frame_index = 0

        self.image = self.animation_list[self.frame_index]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.hitbox = pygame.rect.Rect(self.rect.left + 12,self.rect.top, 26 ,self.rect.height)
        self.reloading = False

        self.aim_timer = 0

        self.x = x
        self.y = y
        self.speed = 5


    def update(self,player,level):
        if not self.died:
            if self.shooting:
                self.shooting_freeze += self.anim_speed
                if self.shooting_freeze > len(self.shooting_anim):
                    self.shooting = False
                    self.shooting_freeze = 0
            else: self.input(player, level)

            if self.flip:
                self.rect.center = (self.x - 25, self.y)
                self.hitbox.topleft = (self.rect.topleft[0] + 64, self.rect.topleft[1])
            else:
                self.rect.center = (self.x+5, self.y)
                self.hitbox.topleft = (self.rect.topleft[0] + 12, self.rect.topleft[1])
        else: 
            self.anim_speed = 0.07
            self.die()
        self.animate()
        self.rect.center = (self.x, self.y)

    def animate(self):
        if self.died:
            self.animation_list = self.death_anim
        elif self.shooting:
            self.animation_list = self.shooting_anim
            
        elif self.moving:
            
            self.animation_list = self.walking

        elif self.aiming:
            
            self.animation_list = self.aim

        else: self.animation_list = self.idle

        self.frame_index += self.anim_speed
        if self.frame_index > len(self.animation_list):
            self.frame_index = 0

        self.image = self.animation_list[int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def die(self):
        if self.death_timer/60 < 1.4:
            self.death_timer += 1
        else:
            self.kill()
    def fire(self, player):
        self.gunshot_sound.play()
        self.shooting = True
        shot = random.randrange(0,9)
        if shot > 3:
            player.hp -= 1

    def patrol(self):
        self.moving = True

        if self.xrange[0]< self.x <self.xrange[1]:
            if self.flip:
                self.x -= 2
            else:
                self.x += 2
        else:
            self.moving = False
            if self.stand_timer/60 < 3:
                     self.stand_timer += 1
            else:
                self.stand_timer = 0
                self.flip = not self.flip
                if self.x >= self.xrange[1]: self.x -=20
                if self.x <= self.xrange[0]: self.x += 20



    def input(self,player,level):
        if self.sees(player,level):
            self.moving = False
            if self.aimed():
                self.fire(player)
        else: self.patrol()

    def aimed(self):
        self.aiming = True
        if self.aim_timer/60 < 2:
            self.aim_timer += 1
        else:
            self.aim_timer = 0
            return True

    def sees(self, player, level):
        if player.hiding:
            return False
        else:
            self.aiming = True
            for block in level:
                obscured = block.rect.clipline(self.rect.center, player.hitbox.center)
                if obscured: self.aiming = False

            line_to_player = self.rect.clipline(self.rect.center, player.hitbox.center)
            if self.flip:
                if line_to_player[1][0] < line_to_player[0][0]: facing = True
                else: facing = False
            else:
                if line_to_player[1][0] > line_to_player[0][0]: facing = True
                else: facing = False

            if facing and self.aiming: return True
            else:                   return False
