from PIL import Image
from variable import *
import random

class something_moves:
    def __init__(self, name, x, y, cdirection):
        self.name = name
        self.x = x
        self.y = y
        self.center_x = x + 5
        self.center_y = y + 6
        self.imgs = []
        self.cdirection = cdirection
        self.state = 1
        self.turn_allowed = [False, False, False, False]
        self.speed = 5
        
    def move(self):
        if self.state == 1:
            if self.cdirection == 0:
                self.x += self.speed
                self.center_x = self.x + 5
            if self.cdirection == 1:
                self.x -= self.speed
                self.center_x = self.x + 5
            if self.cdirection == 2:
                self.y -= self.speed
                self.center_y = self.y + 6
            if self.cdirection == 3:
                self.y += self.speed
                self.center_y = self.y + 6
                
    def reset_attributes(self, x, y, cdirection):
        self.x = x
        self.y = y
        self.center_x = x + 5
        self.center_y = y + 6
        self.cdirection = cdirection
        self.state = 1
        self.turn_allowed = [False, False, False, False]
        
                
class player(something_moves):
    def __init__(self, name, x, y, cdirection):
        something_moves.__init__(self, name, x, y, cdirection)
        self.direction = 0
        self.powerup = False
        self.matrix_x = self.center_x // num2
        self.matrix_y = self.center_y // num1
        
    def copy(self):
        PacMan = player(self.name, self.x, self.y, self.cdirection)
        PacMan.direction = self.direction
        PacMan.powerup = self.powerup
        return PacMan
        
    def add_frame(self):
        for i in range (1, 5):
            self.imgs.append(Image.open(f'assets/player/{i}.png').resize((30,30)))
            
    def change_direction_player(self): 
        if self.direction == self.cdirection:
            return
        if self.direction == 0 and self.turn_allowed[0]: #Right
            for i in range (0, 4):  
                 if self.cdirection == 1 : 
                    self.imgs[i] = self.imgs[i].rotate(angle = 180)
                 if self.cdirection == 2:
                    self.imgs[i] = self.imgs[i].rotate(angle = -90)
                 if self.cdirection == 3:
                    self.imgs[i] = self.imgs[i].rotate(angle = 90)
            self.cdirection = 0
            self.state = 1
         
        if self.direction == 1 and self.turn_allowed[1]: #Left
            for i in range (0, 4):  
                 if self.cdirection == 0: 
                    self.imgs[i] = self.imgs[i].rotate(angle = 180)
                 if self.cdirection == 2:
                     self.imgs[i] = self.imgs[i].rotate(angle = 90)
                 if self.cdirection == 3:
                     self.imgs[i] = self.imgs[i].rotate(angle = -90)
            self.cdirection = 1
            self.state = 1
        
        if self.direction == 2  and self.turn_allowed[2]: #Up
           for i in range (0, 4):  
                 if self.cdirection == 3: 
                    self.imgs[i] = self.imgs[i].rotate(angle = 180)
                 if self.cdirection == 1:
                     self.imgs[i] = self.imgs[i].rotate(angle = -90)
                 if self.cdirection == 0:
                     self.imgs[i] = self.imgs[i].rotate(angle = 90)
           self.cdirection = 2
           self.state = 1
        
        if self.direction == 3 and self.turn_allowed[3]: #Down
           for i in range (0, 4):  
                 if self.cdirection == 2: 
                    self.imgs[i] = self.imgs[i].rotate(angle = 180)
                 if self.cdirection == 1:
                     self.imgs[i] = self.imgs[i].rotate(angle = 90)
                 if self.cdirection == 0:
                     self.imgs[i] = self.imgs[i].rotate(angle = -90)
           self.cdirection = 3
           self.state = 1
           
    def check_state(self):
        count = 0
        for i in range(4):
            if i != self.cdirection and self.turn_allowed[i]:
                count += 1
        if count > 1 or not self.turn_allowed[self.cdirection]:
            self.state = -1
        else:
            self.state = 1
            
    def get_position(self):
        return self.center_y, self.center_x
    
    def get_matrix_position(self):
        y = self.center_y // num1
        x = self.center_x // num2
        return y, x
    
    # def move_fast(self):
    #     if self.state == 1:
    #         if self.cdirection == 0:
    #             self.x += self.speed
    #             self.center_x = self.x + 10
    #         if self.cdirection == 1:
    #             self.x -= self.speed
    #             self.center_x = self.x + 10
    #         if self.cdirection == 2:
    #             self.y -= self.speed
    #             self.center_y = self.y + 12
    #         if self.cdirection == 3:
    #             self.y += self.speed
    #             self.center_y = self.y + 12
            
class ghost(something_moves):
    def __init__(self, name, x, y, cdirection, file, Id, box):
        something_moves.__init__(self, name, x, y, cdirection)
        self.id = Id
        self.imgs.append(Image.open(f'assets/ghost/{file}.png').resize((30, 30)))
        self.in_box = box
        
    def set_target(self, player_x, player_y):
        self.target_x = player_x
        self.target_y = player_y
        
    def change_direction(self):
        temp = []
        count_temp = 0 
        for i in range(4):
            if self.turn_allowed[i] == True :
                temp.append(i)
                count_temp += 1
            if count_temp > 2 :
                self.state = -1
        if self.state == -1 :
            self.cdirection = temp[random.randint(0,len(temp)-1)]
            self.state = 1
        self.move()
        
        




