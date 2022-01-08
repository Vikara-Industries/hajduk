import pygame, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy,self).__init__()
        #animation
        if y > 300:
            self.xrange =(0,800)
        elif x< 100:
            self.xrange =(0,275)
        else:
            self.xrange =(530,800)
        self.anim_speed = 0.2
        self.flip = False
        self.animation_list = [pygame.image.load("../sprites/turk/Stand.png").convert_alpha()]

        self.idle = [pygame.image.load("../sprites/turk/Stand.png").convert_alpha(),pygame.image.load("../sprites/turk/Stand.png").convert_alpha()]

        self.aiming = False
        self.aim = [pygame.image.load("../sprites/turk/aim.png").convert_alpha(),pygame.image.load("../sprites/turk/aim.png").convert_alpha()]

        self.moving = False
        self.walking = []
        self.walking.append(pygame.image.load("../sprites/turk/walk 1.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 2.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 3.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 4.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 5.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 6.png").convert_alpha())

        self.shooting = False
        self.shooting_freeze = 0
        self.shooting_anim = []
        self.shooting_anim.append(pygame.image.load("../sprites/turk/shoot 1.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("../sprites/turk/shoot 2.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("../sprites/turk/shoot 3.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("../sprites/turk/shoot 4.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("../sprites/turk/shoot 5.png").convert_alpha())

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
        if self.reloading:
            self.reload()
        if self.shooting:
            self.shooting_freeze += self.anim_speed
            if self.shooting_freeze > len(self.shooting_anim):
                self.shooting = False
                self.shooting_freeze = 0
        else: self.input(player, level)

        self.animate()
        self.rect.center = (self.x, self.y)

        if self.flip:
            self.rect.center = (self.x - 25, self.y)
            self.hitbox.topleft = (self.rect.topleft[0] + 64, self.rect.topleft[1])
        else:
            self.rect.center = (self.x+5, self.y)
            self.hitbox.topleft = (self.rect.topleft[0] + 12, self.rect.topleft[1])


    def animate(self):

        if self.shooting:
            self.animation_list = self.shooting_anim
            self.hiding = False
        elif self.moving:
            self.hiding = False
            self.animation_list = self.walking


        elif self.aiming:
            self.hiding = False
            self.animation_list = self.aim

        else: self.animation_list = self.idle

        self.frame_index += self.anim_speed
        if self.frame_index > len(self.animation_list):
            self.frame_index = 0

        self.image = self.animation_list[int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def reload(self):

        if self.reload_timer/60 < 2:
            self.reload_timer += 1
        else:
            self.shooting = True
    def fire(self, player):
        self.shooting = True
        shot = random.randrange(0,9)
        if shot > 6:
            player.hp -= 1

    def patrol(self):
        pass
    def input(self,player,level):
        self.patrol()
        if self.sees(player,level):
            if self.aimed():
                self.fire(player)

    def aimed(self):
        if self.aim_timer/60 < 3:
            self.aim_timer += 1
        else:
            aim_timer = 0
            return True

    def sees(self, player, level):
        if player.hiding:
            return False
        else:
            self.aim = True
            for block in level:
                obscured = block.rect.clipline(self.rect.center, player.hitbox.center)
                if obscured: self.aim = False

            line_to_player = self.rect.clipline(self.rect.center, player.hitbox.center)
            if self.flip:
                if line_to_player[1][0] < line_to_player[0][0]: facing = True
                else: facing = False
            else:
                if line_to_player[1][0] > line_to_player[0][0]: facing = True
                else: facing = False

            if facing and self.aim: return True
            else:                   return False
