import pygame

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
PLAYER_SIZE=8
PLAYER_SPEED=7
PLAYER_COLOR=(0,100,255)
INVI_COOLDOWN=6


class Player:

    def __init__(self):
        self.radius=PLAYER_SIZE
        self.x=SCREEN_WIDTH/2
        self.y=SCREEN_HEIGHT/2
        self.speed=PLAYER_SPEED
        self.original_speed=PLAYER_SPEED
        self.invincible_timer=0
        #if use invincible skill,should wait 6 seconds for cd.
        self.invincible_cooldown=0

    def move(self,action):
        dx=0
        dy=0
        #four move directions,up down left right
        if action==1:
            dy=-self.speed
        elif action==2:
            dy=self.speed
        elif action==3:
            dx=-self.speed
        elif action==4:
            dx=self.speed
        self.x=self.x+dx
        self.y=self.y+dy
        if self.x<self.radius:
            self.x=self.radius
        #prevent player out of the window    
        if self.x>SCREEN_WIDTH-self.radius:
            self.x=SCREEN_WIDTH-self.radius
        if self.y<self.radius:
            self.y=self.radius
        if self.y>SCREEN_HEIGHT-self.radius:
            self.y=SCREEN_HEIGHT-self.radius

    def draw(self,screen):
        if self.invincible_timer>0:
            #if invincible, the player will be semi-transparent
            s=pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA)
            pygame.draw.circle(s,(*PLAYER_COLOR,128),(self.radius,self.radius),self.radius)
            screen.blit(s,(int(self.x)-self.radius,int(self.y)-self.radius))
        else:
            pygame.draw.circle(screen,PLAYER_COLOR,(int(self.x),int(self.y)),self.radius)

    #player can speed up two times
    def speedup(self):
        self.speed=self.speed*1.5
        if self.speed>self.original_speed*3:
            self.speed=self.original_speed*3
    #player can speed down two times
    def speeddown(self):
        self.speed=self.speed*0.5
        if self.speed<self.original_speed*0.25:
            self.speed=self.original_speed*0.25

    def speed_restored(self):
        self.speed=self.original_speed

    #to let q-learning know when to change speed
    def get_speed_level(self):
        r=self.original_speed
        if self.speed<=r*0.4:
            return 0
        elif self.speed<=r*0.7:
            return 1
        elif self.speed<=r*1.2:
            return 2
        elif self.speed<=r*1.8:
            return 3
        elif self.speed<=r*2.6:
            return 4
        return 5


    def be_invincible(self,time):
        if self.invincible_cooldown<=0:
            self.invincible_timer=time
            self.invincible_cooldown=INVI_COOLDOWN


