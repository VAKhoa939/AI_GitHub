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
time_start = 0
time_end = 0

# variable for life increase / decrease
life = 3

#control the flashing off the point
flicker = False

#widely used var
eaten_ghost = [False, False, False, False]
ghost_img = []

# bonus Var
history = []
mode = 0
cheat_code = ['','','','']
color = 'Blue'

#settings
level = [] #import the boards matrix from board.py
explore_board = []
food_positions = []
for i in range(len(level1)):
    explore_board.append([])
    for j in range(len(level1[i])):
        if level1[i][j] < 3:
            explore_board[i].append(" ")
            if level1[i][j] == 1 or level1[i][j] == 2:
                food_positions.append((i, j))
        else:
            explore_board[i].append("#")
    level.append(level1[i].copy())
# for i in range(len(level1)):
#     level.append(level1[i].copy())
row = len(level) #33
column = len(level[0]) #30
WIDTH = column * 20 #600
HEIGHT = row * 20 #660
num1 = (HEIGHT - 60) // row #vertical padding
num2 = (WIDTH // column) #horizontal padding
num3 = (num1 + num2) // 5 # 10
player_imgs = []
goal_score = goal_point(level)
