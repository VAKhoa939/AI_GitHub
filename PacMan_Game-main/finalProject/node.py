from player import *
from variable import *

class Node:
    def __init__(self, PacMan, level, score):
        self.level = []
        for i in range(len(level)):
            self.level.append(level[i].copy())
        self.PacMan = player(PacMan.name, PacMan.x, PacMan.y, PacMan.cdirection)
        self.PacMan.direction = PacMan.direction
        self.nodes = []
        self.score = score
        self.direction = PacMan.direction
    
    def compare(self, other):
        if self.PacMan.x != other.PacMan.x or self.PacMan.y != other.PacMan.y or self.score != other.score:
            return False
        return True
        
    def expand(self):
        self.check_position()
        for i in range(4):
            if self.PacMan.turn_allowed[i] == True:
                node = Node(self.PacMan, self.level, self.score)
                node.direction = i
                node.PacMan.direction = i
                node.move()
                self.nodes.append(node)
        
    def check_position(self) :
        turn = [False, False, False, False]
        if self.PacMan.center_x // row < row :
            if self.PacMan.cdirection == 0: 
                if self.level[self.PacMan.center_y // num1][(self.PacMan.center_x + num3 - 1) // num2] >= 3 :
                    self.PacMan.state = -1
                    print (f'{self.PacMan.name} contact right')
                if self.level[self.PacMan.center_y // num1][(self.PacMan.center_x - num2) // num2] < 3:
                    turn[1] = True
                
            if self.PacMan.cdirection == 1:
                if self.level[self.PacMan.center_y // num1][(self.PacMan.center_x - num2 + 1) // num2] >= 3 :
                    self.PacMan.state = -1 
                    print(f'{self.PacMan.name} contact left')
                if self.level[self.PacMan.center_y // num1][(self.PacMan.center_y + num3) // num2] < 3:
                    turn[0] = True
                
            if self.PacMan.cdirection == 2:
                if self.level[(self.PacMan.center_y - num1) // num1][(self.PacMan.center_x) // num2] >= 3 :
                    self.PacMan.state = -1
                    print(f'{self.PacMan.name} contact up')
                if self.level[(self.PacMan.center_y + num3) // num1][(self.PacMan.center_x) // num2] < 3:
                    turn[3] = True
                
            if self.PacMan.cdirection == 3:
                if self.level[(self.PacMan.center_y + num3) // num1][(self.PacMan.center_x) // num2] >= 3 :
                    self.PacMan.state = -1
                    print (f'{self.PacMan.name} contact Down')
                if self.level[(self.PacMan.center_y - num1) // num1][(self.PacMan.center_x) // num2] < 3:
                    turn[2] = True
                
                
            if self.PacMan.cdirection == 2 or self.PacMan.cdirection == 3 :
                if num2 - num3 <= self.PacMan.center_x % num2 <= num2 + num3 :
                    if self.level[(self.PacMan.center_y + num3) // num1][(self.PacMan.center_x) // num2] < 3 :
                        turn[3] = True
                    if self.level[(self.PacMan.center_y - num3) // num1][(self.PacMan.center_x) // num2] < 3 :
                        turn[2] = True
                if num1 - num3 <= self.PacMan.center_y % num1 <= num1 + num3 :
                    if self.level[(self.PacMan.center_y) // num1][(self.PacMan.center_x + num2) // num2] < 3 :
                        turn[0] = True
                    if self.level[(self.PacMan.center_y) // num1][(self.PacMan.center_x - num2) // num2] < 3 :
                        turn[1] = True
            
            if self.PacMan.cdirection == 0 or self.PacMan.cdirection == 1 :
                if num2 - num3 <= self.PacMan.center_x % num2 <= num2 + num3 :
                    if self.level[(self.PacMan.center_y + num1) // num1][(self.PacMan.center_x) // num2] < 3 :
                        turn[3] = True
                    if self.level[(self.PacMan.center_y - num1) // num1][(self.PacMan.center_x) // num2] < 3 :
                        turn[2] = True
                if num1 - num3 <= self.PacMan.center_y % num1 <= num1 + num3 :
                    if self.level[(self.PacMan.center_y) // num1][(self.PacMan.center_x + num2) // num2] < 3 :
                        turn[0] = True
                    if self.level[(self.PacMan.center_y) // num1][(self.PacMan.center_x - num2) // num2] < 3 :
                        turn[1] = True
        else: 
            turn [0] = True
            turn [1] = True
        self.PacMan.turn_allowed = turn
            
    def check_collison(self):
        if  0 < self.PacMan.x < 650 :
            if self.level[self.PacMan.center_y // num1][self.PacMan.center_x//num2] == 1:
                self.level[self.PacMan.center_y // num1][self.PacMan.center_x//num2] = 0
                self.score += 10
            if self.level[self.PacMan.center_y// num1][self.PacMan.center_x//num2] == 2:
                self.level[self.PacMan.center_y// num1][self.PacMan.center_x//num2] = 0
                self.PacMan.powerup = True
                self.score += 50
            
    def move(self):
        self.check_position()
        self.PacMan.state = 1
        while self.PacMan.state == 1:
            self.PacMan.move()
            self.check_collison()
            self.check_position()
            self.PacMan.check_state()
            
    def is_goal(self):
        return self.score == goal_score
            
