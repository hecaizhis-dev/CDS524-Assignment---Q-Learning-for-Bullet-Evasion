import pygame
import random
from player import Player
from bullet import Bullet

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
FPS=120
BLACK=(0,0,0)
WHITE=(255,255,255)
BULLET_SPEED=2
BULLET_CREATETIME=30
BULLET_CREATE_PER=5
INVI_TIME=0.6

REWARD_SURVIVE=1.0
REWARD_DEATH=-100.0


class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock=pygame.time.Clock()
        self.player=Player()
        self.bullets=[]
        self.count=0
        self.font=pygame.font.Font(None,36)

    def new_game(self):
        self.player=Player()
        self.bullets=[]
        self.count=0
        return self.get_state()


    def createbullets(self):
        for i in range(BULLET_CREATE_PER):
            #decide where bullets appear:margin of the left,right,top,bottom margin
            appear_margin=random.randint(0,3)
            if appear_margin==0:
                x=random.randint(0,SCREEN_WIDTH)
                y=0
            elif appear_margin==1:
                x=random.randint(0,SCREEN_WIDTH)
                y=SCREEN_HEIGHT
            elif appear_margin==2:
                x=0
                y=random.randint(0,SCREEN_HEIGHT)
            else:
                x =SCREEN_WIDTH
                y =random.randint(0,SCREEN_HEIGHT)
            dx=random.choice([-1,0,1])
            dy=random.choice([-1,0,1])
            if dx==0 and dy==0:
                dy=1
            self.bullets.append(Bullet(x,y,dx*BULLET_SPEED,dy*BULLET_SPEED))

    def get_state(self):
        player_x=self.player.x
        player_y=self.player.y
        grid_x=int(player_x/100)
        grid_y=int(player_y/100)
        grid_x=max(0,min(7,grid_x))
        grid_y=max(0,min(5,grid_y))

        if len(self.bullets)==0:
            return (
        int(100*grid_x),
        int(100*grid_y),
        0,
        0,
        int(100*self.player.get_speed_level()),
        1 if self.player.invincible_timer>0 else 0,
        1 if self.player.invincible_cooldown>0 else 0)

        nearest_bullet=self.bullets[0]
        distance2=(nearest_bullet.x-player_x)**2+(nearest_bullet.y-player_y)**2
        #find the nearest bullet
        for i in self.bullets:
            d=(i.x-player_x)**2+(i.y-player_y)**2
            if d<distance2:
                distance2=d
                nearest_bullet=i
        relative_x=nearest_bullet.x-player_x
        relative_y=nearest_bullet.y-player_y
        dist=(relative_x*relative_x+relative_y*relative_y)**0.5
        #judge the relative position of the bullet
        #1:right 2:left 3:down 4:up
        if abs(relative_x)>abs(relative_y):
            if relative_x>0:
                direction=1 
            else:
                direction=2
        else:
            if relative_y>0:
                direction=3 
            else:
                direction=4
        #the closer to the player,the more danger bullet is,the higher danger_degree is
        m=min(SCREEN_WIDTH,SCREEN_HEIGHT)
        if dist<m/32:
            danger_degree=3
        elif dist<m/16:
            danger_degree=2
        elif dist<m/8:
            danger_degree=1
        else:
            danger_degree=0                         


    
        speed_level=self.player.get_speed_level()
        #quantization. convert the float into int
        return (
        int(100*grid_x),
        int(100*grid_y),
        int(100*direction),
        int(100*danger_degree),
        int(100*speed_level),
        1 if self.player.invincible_timer>0 else 0,
        1 if self.player.invincible_cooldown>0 else 0)


    #margin check:if collide the margin of the circle
    def check_collision(self):
        if self.player.invincible_timer>0:
            return False
        player_x=self.player.x
        player_y=self.player.y
        player_r=self.player.radius
        for b in self.bullets:
            dis=(b.x-player_x)**2+(b.y-player_y)**2
            if dis<(player_r+b.radius)**2:
                return True
        return False

    def update_actions(self,action):
        self.count=self.count+1
        invincible_penalty=0
        if self.player.invincible_timer>0:
            self.player.invincible_timer-=1/FPS
        if self.player.invincible_cooldown>0:
            self.player.invincible_cooldown-=1/FPS
        if action==5:
            self.player.speedup()
        elif action==6:
            self.player.speeddown()
        elif action==7:
            self.player.speed_restored()
        elif action==8:
                #prevent continuous invincible mechanics using and reward deduction
            if(self.player.invincible_cooldown<=0):
                self.player.be_invincible(INVI_TIME)
            #punishment mechanics
                invincible_penalty=5
                
        else:
            self.player.move(action) 
        if self.count%BULLET_CREATETIME==0:
            self.createbullets()

        #when some bullets disappear from the margin,remove them from the bullet list
        #recover straightly the original bullet list 
        cleared_bullet=[]
        for b in self.bullets:
            if not b.is_disappeared():
                cleared_bullet.append(b)
        self.bullets=cleared_bullet
        for b in self.bullets:
            b.update()

        #handle collision penalty and reward
        if self.check_collision():
            return self.get_state(),REWARD_DEATH,True
            #1 reward for 1 frame living
        return self.get_state(),REWARD_SURVIVE-invincible_penalty ,False

    def render(self,score=0,action=0,reward=0):
        self.screen.fill(WHITE)
        self.player.draw(self.screen)
        for b in self.bullets:
            b.draw_bullet(self.screen)
        text1=self.font.render("Score:"+str(score),True,BLACK)
        self.screen.blit(text1,(10,10))
        pygame.display.flip()
        self.clock.tick(FPS)
