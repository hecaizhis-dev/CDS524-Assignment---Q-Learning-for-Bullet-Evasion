
#Q(s,a)=Q(s,a)+alpha*(target-Q(s,a))
#finished:target=r+gamma*max Q(s',a')
#unfinished:target=r
import random
import pickle
import os

#9 actions: 0 idle,1 up,2 down,3 left,4 right,5 speedup,6 slowdown,7 restore the speed,8 invincible for 0.6 seconds
ACTIONS_SUM=9
ALPHA=0.1
GAMMA=0.95
EPSILON=0.02

QTABLE_PATH="model/q-learning_model.pkl"


class QAgent:
    def __init__(self):
        self.qtable={}

    def get_qtable(self,state,action):
        key=(state,action)
        return self.qtable.get(key,0.0)

    def select_action(self,state,training=True):
        #when training:epsilon-greedy
        if training and random.random()<EPSILON:
            return random.randint(0,ACTIONS_SUM-1)
        #when not training:choose the maximum q
        ans=0
        qmax=self.get_qtable(state,0)
        for i in range(1,ACTIONS_SUM):
            tmp=self.get_qtable(state,i)
            if tmp>qmax:
                qmax=tmp
                ans=i
        return ans

    def update(self,state,action,score,next_state,finished):
        old_q=self.get_qtable(state,action)
        #target=r
        if finished:
            target=score
        else:
        #target=r+gamma*max Q(s',a')  
            qmax=self.get_qtable(next_state,0)
            for i in range(1,ACTIONS_SUM):
                tmp=self.get_qtable(next_state,i)
                if tmp>qmax:
                    qmax=tmp
            target=score+GAMMA*qmax
        new_q=old_q+ALPHA*(target-old_q)
        self.qtable[(state,action)]=new_q

    def save(self):       
        path=os.path.dirname(QTABLE_PATH)
        os.makedirs(path,exist_ok=True)
        with open(QTABLE_PATH,"wb") as a:
            pickle.dump(self.qtable,a)

    def load(self):
        try:
            with open(QTABLE_PATH,"rb") as a:
                self.qtable=pickle.load(a)
        except Exception as e:
            self.qtable={}
            print("loaded error")
