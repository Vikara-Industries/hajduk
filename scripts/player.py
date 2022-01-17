from os import path
import pygame
from pygame import mouse
from pygame import mixer


class Player(pygame.sprite.Sprite):
    def __init__(self, level,enemies, x, y, weapon):
        super(Player,self).__init__()
        self.level = level
        self.enemies = enemies
        #animation
        self.anim_speed = 0.2
        self.flip = False
        self.animation_list = [pygame.image.load("./sprites/hajduk/Stand.png").convert_alpha()]

        self.idle = [pygame.image.load("./sprites/hajduk/Stand.png").convert_alpha(),pygame.image.load("./sprites/hajduk/Stand.png").convert_alpha()]

        self.aiming = False
        self.aim = [pygame.image.load("./sprites/hajduk/aim.png").convert_alpha(),pygame.image.load("./sprites/hajduk/aim.png").convert_alpha()]

        self.moving = False
        self.walking = []
        self.walking.append(pygame.image.load("./sprites/hajduk/walk 1.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/hajduk/walk 2.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/hajduk/walk 3.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/hajduk/walk 4.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/hajduk/walk 5.png").convert_alpha())
        self.walking.append(pygame.image.load("./sprites/hajduk/walk 6.png").convert_alpha())

        self.gunshot_sound = mixer.Sound("./Sound/gunshot.mp3")
        self.shooting = False
        self.shooting_freeze = 0
        self.shooting_anim = []
        self.shooting_anim.append(pygame.image.load("./sprites/hajduk/shoot 1.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("./sprites/hajduk/shoot 2.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("./sprites/hajduk/shoot 3.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("./sprites/hajduk/shoot 4.png").convert_alpha())
        self.shooting_anim.append(pygame.image.load("./sprites/hajduk/shoot 5.png").convert_alpha())


        self.death_timer = 0
        self.died = False
        self.death_anim = []
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 1.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 2.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 3.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 4.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 5.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 6.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 7.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 8.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 9.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 10.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 11.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 12.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 13.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 14.png").convert_alpha())
        self.death_anim.append(pygame.image.load("./sprites/hajduk/Death 15.png").convert_alpha())

        self.hiding = False
        self.hide_anim = [pygame.image.load("./sprites/hajduk/Crouch.png").convert_alpha(),pygame.image.load("./sprites/hajduk/Crouch.png").convert_alpha()]


        self.frame_index = 0

        self.image = self.animation_list[self.frame_index]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.hitbox = pygame.rect.Rect(self.rect.left + 12,self.rect.top, 26 ,self.rect.height)


        self.x = x
        self.y = y
        self.speed = 5

        self.sneaking = False

        self.score = 0
        self.weapon = weapon
        self.shot = False

        self.ammo = 6
        self.reloading = False
        self.reload_timer = 0

        self.hp = 3
        self.interact_with = None
        self.interact_timer = pygame.time.get_ticks()
        self.interact_cooldown = 800



    def update(self):
        if self.hp > 0:
            if self.moving and not self.sneaking:
                self.weapon.spread = self.weapon.spread_max


            if self.reloading:
                self.reload()
            if self.shooting:
                if self.shooting_freeze == 0:
                    self.gunshot_sound.play()
                    self.ammo -=1
                    for block in self.level:
                        shootline = block.rect.clipline(self.x, self.y, self.shot[0], self.shot[1])
                        if shootline: self.shot = shootline[0]

                    for enemy in self.enemies:
                        shootline = enemy.rect.clipline(self.x, self.y, self.shot[0], self.shot[1])
                        if shootline: 
                            enemy.died = True
                            self.score += 100


                self.shooting_freeze += self.anim_speed
                if self.shooting_freeze > len(self.shooting_anim):
                    self.shooting = False
                    self.shooting_freeze = 0
            else:
                self.input()



            
            self.y += 5
            self.checkCollision(self.level)
            self.rect.center = (self.x, self.y)

            if self.flip:
                self.rect.center = (self.x - 25, self.y)
                self.hitbox.topleft = (self.rect.topleft[0] + 64, self.rect.topleft[1])
            else:
                self.rect.center = (self.x+5, self.y)
                self.hitbox.topleft = (self.rect.topleft[0] + 12, self.rect.topleft[1])
        else: self.died = True
        self.animate()


    def animate(self):
        if self.died == True:
            self.anim_speed = 0.07
            self.animation_list = self.death_anim
            if self.frame_index > len(self.animation_list):
                self.frame_index = len(self.animation_list)
        elif self.shooting:
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
        elif self.hiding:
            self.animation_list = self.hide_anim
        else: self.animation_list = self.idle

        self.frame_index += self.anim_speed
        if self.frame_index > len(self.animation_list):
            self.frame_index = 0

        self.image = self.animation_list[int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.flip(self.image, self.flip, False)



    def draw_ui(self,screen,myfont):
        ammotxt = myfont.render(f"Ammo:{self.ammo}",1,(100,250,60))
        hptxt = myfont.render(f"Health:{self.hp}",1,(100,250,60))
        screen.blit(hptxt, (600, 20))
        screen.blit(ammotxt, (40, 20))
        if self.died:
            
            screen.blit(myfont.render("GAME OVER",1,(100,250,60)), (350,100))
            screen.blit(myfont.render(f"The Ottomans will kill {self.score} Serbs as revenge.",1,(100,250,60)), (20,220))
        if self.reloading:
            screen.blit(myfont.render("Reloading",1,(100,250,60)), (self.hitbox.midtop[0] -75, self.hitbox.midtop[1] - 30))

        if self.aiming:
            pygame.draw.line(screen,(255,0,0),self.hitbox.center, (mouse.get_pos()[0] ,mouse.get_pos()[1] + self.weapon.spread/5))
            pygame.draw.line(screen,(255,0,0),self.hitbox.center, (mouse.get_pos()[0] ,mouse.get_pos()[1] - self.weapon.spread/5))

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
                self.reload_timer = 0
                self.reloading = False
        else:
            self.reloading = False



    def checkCollision(self, level):
        if self.hitbox.collidelist(level) != -1:

            self.y -= 5
