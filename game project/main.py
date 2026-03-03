import sys
import pygame
from game import Game
from q_agent import QAgent

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
TRAINING_TIMES=5000
WHITE=(255,255,255)
BLACK=(0,0,0)


def menu(screen):
    font_title=pygame.font.Font(None,64)
    font_btn=pygame.font.Font(None,48)
    title=font_title.render("Bullet Evasion",True,BLACK)
    mode=[("AI MODE",(200,340)),("TRAIN MODE",(200,400))]
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                sys.exit(0)
            if e.type==pygame.MOUSEBUTTONDOWN:
                x,y=e.pos
                if 200<=x<=400:
                    if 320<=y<=370:
                        return 0
                    if 380<=y<=430:
                        return 1
        screen.fill(WHITE)
        screen.blit(title,(SCREEN_WIDTH//2-120,150))
        for a,(position_x,position_y) in mode:
            screen.blit(font_btn.render(a,True,BLACK),(position_x,position_y))
        pygame.display.flip()




def ai_mode():
    game=Game()
    agent=QAgent()
    agent.load()
    state=game.new_game()
    total=0
    done=False
    while not done:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                sys.exit(0)
        action=agent.select_action(state,training=False)
        state,reward,done=game.update_actions(action)
        total+=reward
        game.render(score=int(total),action=action,reward=reward)
    print("GAME OVER!Reward:",total)
    text=pygame.font.Font(None,72).render("GAME OVER",True,(255,0,0))
    game.screen.blit(text,(SCREEN_WIDTH//2-100,SCREEN_HEIGHT//2-30))
    pygame.display.flip()
    pygame.time.wait(2000)

#train mode
def train_mode():
    game=Game()
    agent=QAgent()
    for ep in range(TRAINING_TIMES):
        state=game.new_game()
        total=0
        done=False
        while not done:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    sys.exit(0)
            action=agent.select_action(state,training=True)
            next_state,reward,done=game.update_actions(action)
            agent.update(state,action,reward,next_state,done)
            state=next_state
            total+=reward
            #if you want to see the training process, please uncomment the code below, but the training speed will be very slow.
            #game.render(score=int(total),action=action,reward=reward)
        print("Ep",ep+1,"Reward:",total)
    agent.save()
    print("Done")


if __name__=="__main__":
    pygame.init()
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    mode=menu(screen)
    if mode==0:
        ai_mode()
    else:
        train_mode()
