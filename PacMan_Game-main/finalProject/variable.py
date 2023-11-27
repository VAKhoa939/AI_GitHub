from board import *
from function import *
score = 0
goal_score = 0
desired_fps = 25
frame = 0
count = 0 #use for PacMan animation looping 
state = -1
start = -1
flicker_time = 0
powerup_counter = 0 
start_up = 0
moving = 0
hit = False
loading = ['','.','..','...',''] 
loading_index = 0

# variable for life increase / decrease
life = 3

#control the flashing off the point
flicker = False

#settings
color = 'Blue'
level = [] #import the boards matrix from board.py
for i in range(len(level1)):
    level.append(level1[i].copy())
row = len(level) #32
column = len(level[0]) #56
WIDTH = column * 20 #1300
HEIGHT = row * 20 #850
num1 = (HEIGHT - 50) // row #vertical
num2 = (WIDTH // column)
num3 = (num1 + num2) // 5 # 10
player_imgs = []
goal_score = goal_point(level)
