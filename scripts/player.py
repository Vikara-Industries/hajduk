from os import path
import pygame
from pygame import mouse
class Player(pygame.sprite.Sprite):
    def __init__(self, level, x, y, weapon):
        super(Player,self).__init__()
        self.level = level
        #animation
        self.anim_speed = 0.2
        self.flip = False
        self.animation_list = [pygame.image.load("../sprites/hajduk/Stand.png").convert_alpha()]

        self.idle = [pygame.image.load("../sprites/hajduk/Stand.png").convert_alpha(),pygame.image.load("../sprites/hajduk/Stand.png").convert_alpha()]

        self.aiming = False
        self.aim = [pygame.image.load("../sprites/hajduk/aim.png").convert_alpha(),pygame.image.load("../sprites/hajduk/aim.png").convert_alpha()]

        self.moving = False
        self.walking = []
        self.walking.append(pygame.image.load("../sprites/hajduk/walk 1.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/hajduk/walk 2.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/hajduk/walk 3.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/hajduk/walk 4.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/hajduk/walk 5.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/hajduk/walk 6.png").convert_alpha())

        self.shooting = False
        self.shooting_freeze = 0
        self.shooting_anim = []
        self.shooting_anim.append(pygame.image.load("../sprites/hajduk/shoot 1.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("../sprites/hajduk/shoot 2.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("../sprites/hajduk/shoot 3.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("../sprites/hajduk/shoot 4.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("../sprites/hajduk/shoot 5.png").convert_alpha())

        self.frame_index = 0

        self.image = self.animation_list[self.frame_index]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()


        self.x = x
        self.y = y
        self.speed = 5

        self.sneaking = False

        self.hiding = False

        self.weapon = weapon
        self.shot = False

        self.ammo = 100
        self.reloading = False
        self.reload_timer = 0

        self.interact_with = None
        self.interact_timer = pygame.time.get_ticks()
        self.interact_cooldown = 1000



    def update(self):

        if self.reloading:
            self.reload()
        if self.shooting:
            if self.shooting_freeze == 0:
                for block in self.level:
                    shootline = block.rect.clipline(self.x, self.y, self.shot[0], self.shot[1])
                    if shootline: self.shot = shootline[0]
            self.shooting_freeze += self.anim_speed
            if self.shooting_freeze > len(self.shooting_anim):
                self.shooting = False
                self.shooting_freeze = 0

        else:
            self.input()

        self.animate()
        self.y += 5
        self.checkCollision(self.level)
        self.rect.center = (self.x, self.y)

    def animate(self):

        if self.shooting:
            self.animation_list = self.shooting_anim
            self.hiding = False
        elif self.moving:
            self.hiding = False
            self.animation_list = self.walking
            self.weapon.spread_min = 160

        elif self.aiming:
            self.hiding = False
            self.animation_list = self.aim
            self.weapon.spread_min = 40
        else: self.animation_list = self.idle

        self.frame_index += self.anim_speed
        if self.frame_index > len(self.animation_list):
            self.frame_index = 0

        self.image = self.animation_list[int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.flip(self.image, self.flip, False)


    def draw_ui(self,screen):
        if self.moving and not self.sneaking:
            self.weapon.spread = self.weapon.spread_max

        if self.aiming:
            pygame.draw.line(screen,(255,0,0),self.rect.center, (mouse.get_pos()[0] ,mouse.get_pos()[1] + self.weapon.spread/5))
            pygame.draw.line(screen,(255,0,0),self.rect.center, (mouse.get_pos()[0] ,mouse.get_pos()[1] - self.weapon.spread/5))

        if self.shot:
            pygame.draw.circle(screen, (255,100,200), self.shot,3,2)

    #shooting related stuff
    def fire(self):
        self.shooting = True
        self.shot = self.weapon.shoot(self.rect.center, pygame.mouse.get_pos())


    def input(self):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()
        if mouse_keys[2] == True:
            self.aiming = True
            self.weapon.aim()
        else:
            self.aiming = False
            self.weapon.spread = self.weapon.spread_max

        if mouse_keys[0] == True:
            if self.weapon.loaded:
                self.fire()

        if keys[pygame.K_d]:
            self.x += self.speed
            self.moving = True
            self.flip = False

        elif keys[pygame.K_a]:
            self.x -= self.speed
            self.moving = True
            self.flip = True

        elif keys[pygame.K_w]:
            print(pygame.time.get_ticks() - self.interact_timer)
            if self.interact_with and (pygame.time.get_ticks() - self.interact_timer > self.interact_cooldown):
                self.interact_with.interact(self)
                self.interact_timer = pygame.time.get_ticks()

        else:
            self.moving = False


        if keys[pygame.K_r]:
            self.reloading = True


        if keys[pygame.K_LCTRL]:
            self.speed = 2.5
            self.sneaking = True

        else:
            self.speed = 5
            self.sneaking = False

    def reload(self):
        if self.ammo > 0:
            if self.reload_timer/60 < 2:
                self.reload_timer += 1
            else:
                self.weapon.reload()
                self.ammo -=1
                print(self.ammo)
                self.reload_timer = 0
                self.reloading = False
        else:
            print("no ammo")
            self.reloading = False



    def checkCollision(self, level):
        if pygame.sprite.spritecollideany(self, level) != None:

            self.y -= 5
