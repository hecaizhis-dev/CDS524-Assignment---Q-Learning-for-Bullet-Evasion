import pygame

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
BULLET_RADIUS=4
BULLET_COLOR=(255,105,180)


class Bullet:
    def __init__(self,x,y,x_velo,y_velo):
        self.x=x
        self.y=y
        self.x_velo=x_velo
        self.y_velo=y_velo
        self.radius=BULLET_RADIUS

    def update(self):
        self.x=self.x+self.x_velo
        self.y=self.y+self.y_velo

    def draw_bullet(self,screen):
        pygame.draw.circle(screen,BULLET_COLOR,(int(self.x),int(self.y)),self.radius)

    #if bullet is out of the window scope,we regard it has disappeared.
    def is_disappeared(self):
        #get the margin dynamically
        margin=min(SCREEN_WIDTH,SCREEN_HEIGHT)/16
        if self.x<-margin or self.x>SCREEN_WIDTH+margin:
            return True
        if self.y<-margin or self.y>SCREEN_HEIGHT+margin:
            return True
        return False
