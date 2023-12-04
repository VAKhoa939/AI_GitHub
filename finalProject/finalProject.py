from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time, os

from player import *
from style import *
from variable import *
from node import *
from algorithms import *


#initial start location
#PacMan initial
PacMan = player('PacMan',(row // 2) * num1 - num1, (column // 2) * num2 + (7 * num2), 0)
player.add_frame(PacMan)
direction = 0
player_imgs.append(PacMan.imgs[0])

#Ghost initial
blinky = ghost('blinky',num1 * 3, num2 * 2 + num3, 0, 'red', 0, True)
blinky.set_target(PacMan.x, PacMan.y)

pinky = ghost('pinky',num1 * 30, num2 * 2 + num3, 1, 'pink', 1, True)
pinky.set_target(PacMan.x, PacMan.y)

inky = ghost('inky',num1 * 3, num2 * 27 + num3, 2, 'blue', 2, True)
inky.set_target(PacMan.x, PacMan.y)

clyde = ghost('clyde',num1 * 30, num2 * 27 + num3, 3, 'orange', 3, True)
clyde.set_target(PacMan.x, PacMan.y)

#state of ghost
spooked_img = Image.open('assets/ghost/powerup.png').resize((30, 30))
dead_img = Image.open('assets/ghost/dead.png').resize((30, 30))


#Begin program
#start GUI
root =Tk()
root.title('PAC MAN')
root.configure(background= 'Black')
root.geometry('1350x800') #level 1650x800
#root.geometry('1650x800')


#score initial
score_display = StringVar()
score_display.set('score: 0')

status_display = StringVar()
current_status = 'Choosing mode'
status_display.set(str(current_status))

ai = Algorithms(food_positions)
algorithm_text = StringVar()
edit_text = StringVar()
solution = []
depth = 0
nodes = 0
cost = 0

top_frame = Canvas(root, bg = 'Black', width = WIDTH, height = HEIGHT)
top_frame.pack(padx = 200,side=LEFT)

top_frame.spooked = ImageTk.PhotoImage(spooked_img)
top_frame.dead = ImageTk.PhotoImage(dead_img)

right_frame = Frame(root, bg = 'Black', width = 50, height = HEIGHT)
right_frame.pack(side=LEFT)

top_frame1 = Frame(right_frame, bg = 'Black', width = WIDTH // 4 + 20, height = HEIGHT // 4)
top_frame1.pack()

logo_frame = Image.open('assets/logo/PacMan.jpg').resize((WIDTH // 2 + 20, HEIGHT // 4))
logo_frame = ImageTk.PhotoImage(logo_frame)
logo = Label(top_frame1, bg = 'Black' ,image= logo_frame)
logo.image = logo_frame
logo.pack()

topFrame2 = Frame(right_frame, bg = 'Black', width = WIDTH // 4 + 20, height = HEIGHT // 4)
topFrame2.pack()

score_frame = Label(topFrame2, textvariable= score_display, font= font, bg = 'Black', fg = 'White')
score_frame.pack()

game_status = Label(topFrame2, textvariable= status_display, font = font, bg = 'Black', fg = 'White')
game_status.pack()

bot_frame1 = Frame(right_frame, bg = 'Black', width = 50, height = HEIGHT // 2)
bot_frame1.pack()

bot_frame2 = Frame(right_frame, bg = 'Black', width = 50, height = HEIGHT // 2)



#function

#draw random
def draw_random(index):
    global PacMan, life
    
    #life display 
    if life >= 1:
        top_frame.life = ImageTk.PhotoImage(player_imgs[0])
        top_frame.create_image(WIDTH - 20, HEIGHT - 50, image = top_frame.life, anchor = CENTER)
    if life >= 2:
        top_frame.life1 = ImageTk.PhotoImage(player_imgs[0])
        top_frame.create_image(WIDTH - 55, HEIGHT - 50, image = top_frame.life1, anchor = CENTER)
    if life >= 3:
        top_frame.life2 = ImageTk.PhotoImage(player_imgs[0])
        top_frame.create_image(WIDTH - 90, HEIGHT - 50, image = top_frame.life2, anchor = CENTER)
    #power_up indication
    if PacMan.powerup == True:
        top_frame.create_oval(num1 * 3, HEIGHT - 50, num1 * 3, HEIGHT - 50, outline = color, width= 20)
        
    status_display.set(str(current_status) + str(loading[index]))
    
#init a board
def draw_board():
    for i in range(len(level)) :
        for j in range (len(level[i])) :
            if level[i][j] == 1 : #create normal point
                top_frame.create_oval((j* num2 + (0.5 * num2), i * num1 + (0.5 * num1), j* num2 + (0.5 * num2) , i * num1 + (0.5 * num1)), outline = 'white', width = 4)
            if level[i][j] == 2 and not flicker: #create Special point
                top_frame.create_oval((j* num2 + (0.5 * num2), i * num1 + (0.5 * num1), j* num2 + (0.5 * num2) , i * num1 + (0.5 * num1)), outline = 'white', width = 10)
            if level[i][j] == 3 : #create line vertical
                top_frame.create_line((j* num2 + (0.5 * num2), i * num1, j* num2 + (0.5 * num2) , i * num1 + num1), fill = color, width= 5)    
            if level[i][j] == 4 : # create line horizontal
                top_frame.create_line((j* num2 , i * num1 + (0.5 * num1), j* num2 + num2, i * num1 + (0.5 * num1)), fill = color, width= 5)  
            if level[i][j] == 5 : # create corner 1
                top_frame.create_arc((j* num2 - (num2 * 0.5) , i * num1 + (0.5 * num1), j* num2 + (0.5 * num2), i * num1 + 1.5 * num1), outline = color , width= 5, start = 0, extent = 90, style = ARC) 
            if level[i][j] == 6 : # create corner 2
               top_frame.create_arc((j* num2 + (.5 * num2) , i * num1 + (1.65 * num1), j* num2 + (1.5 * num2) , i * num1 + (.5 * num1)), outline = color , width= 5, start = 180, extent = -90, style = ARC)    
            if level[i][j] == 7 : # create corner 3 
               top_frame.create_arc((j* num2 + (num2 * 0.5) , i * num1 - (1 * num1), j* num2 + (num2 * 1.65) , i * num1 + (0.5 * num1)), outline = color , width= 5, start = 180, extent = 90, style = ARC)  
            if level[i][j] == 8 : # create corner 4
               top_frame.create_arc((j* num2 + (num2 * 0.5) , i * num1 - (0.5 * num1), j* num2 - (num2 * 0.65) , i * num1 + (0.5 * num1)), outline = color , width= 5, start = 0, extent = -90, style = ARC)  
            
            if level[i][j] == 9 : # create the white line
                top_frame.create_line((j* num2 , i * num1 + (0.5 * num1), j* num2 + num2, i * num1 + (0.5 * num1)), fill = 'white', width= 2)    


def draw_explored_board():
    for i in range(len(explore_board)):
        for j in range(len(explore_board[i])):
            print(explore_board[i][j], end = " ")
        print()

# GUI function
def draw_panel():
    # First page
    global algorithm_text
    play_button = Button(bot_frame1, font = font ,text = 'Play', command = play_PacMan)
    play_button.pack(pady = 20)
    edit_combobox = ttk.Combobox(bot_frame1, font = font,width = 20, textvariable = algorithm_text)
    edit_combobox['values'] = ('Depth First Search',
                               'Breadth First Search',
                               'Uniform Cost Search',
                               'Greedy Search',
                               'A-star Search')
    edit_combobox.current(0)
    edit_combobox.pack()
    solve_button = Button(bot_frame1, font = font ,text = 'Solve', command = solve_PacMan)
    solve_button.pack(pady = 20)
    reset_button = Button(bot_frame1, font = font ,text = 'Reset', command = reset_board)
    reset_button.pack(pady = 20)
    edit_button = Button(bot_frame1, font = font ,text = 'Edit Mode', command = switch_edit_mode)
    edit_button.pack(pady = 20)
    exit_button = Button(bot_frame1, font = font ,text = 'Exit', command = root.destroy)
    exit_button.pack(pady = 20)

    # Second page
    edit_combobox = ttk.Combobox(bot_frame2, font = font,width = 20, textvariable = edit_text)
    edit_combobox['values'] = ('Empty',
                               'Dot',
                               'Big dot',
                               'Pac Man',
                               'Blinky',
                               'Pinky',
                               'Inky',
                               'Clyde',)
    edit_combobox.pack(pady = 20)
    confirm_button = Button(bot_frame2, font = font ,text = 'Confirm', command = root.destroy)
    confirm_button.pack(pady = 20)
    back_button = Button(bot_frame2, font = font ,text = 'Back', command = switch_main_mode)
    back_button.pack(pady = 20)
    
def switch_edit_mode():
    update_game_status('Editing')
    draw_random(0)
    bot_frame1.forget()
    bot_frame2.pack()
    
def switch_main_mode():
    update_game_status('Choosing mode')
    draw_random(0)
    bot_frame2.forget()
    bot_frame1.pack()
   
def update_score(score):
    global score_display
    score_display.set('score: ' + str(score))
    
def update_game_status(state):
    global current_status
    current_status = state
    
# Core Function
# reset board
def reset_board():
    global score, frame, count, state, start, flicker_time, powerup_counter, start_up, moving, hit, loading_index, time_start, time_end, life, flicker, eaten_ghost, history, mode, level, explore_board, food_positions, ai, solution, depth, nodes, cost
    score = 0
    frame = 0
    count = 0 #use for PacMan animation looping 
    state = -1
    start = -1
    flicker_time = 0
    powerup_counter = 0 
    start_up = 0
    moving = 0
    hit = False
    loading_index = 0
    time_start = 0
    time_end = 0

    # variable for life increase / decrease
    life = 3

    #control the flashing off the point
    flicker = False

    #widely used var
    eaten_ghost = [False, False, False, False]

    # bonus Var
    history.clear()
    mode = 0

    #settings
    level.clear()
    explore_board.clear()
    food_positions.clear()
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
    
    PacMan.direction = 0
    PacMan.change_direction_player()
    PacMan.reset_attributes((row // 2) * num1 - num1, (column // 2) * num2 + (7 * num2), 0)
    blinky.reset_attributes(num1 * 3, num2 * 2 + num3, 0)
    pinky.reset_attributes(num1 * 30, num2 * 2 + num3, 1)
    inky.reset_attributes(num1 * 3, num2 * 27 + num3, 2)
    clyde.reset_attributes(num1 * 30, num2 * 27 + num3, 3)
    
    ai = Algorithms(food_positions)
    solution.clear()
    depth = 0
    nodes = 0
    cost = 0
    update_game_status('Choosing mode')
    draw_random(0)
    
def reset_ai():
    global ai
    explore_board.clear()
    for i in range(len(level1)):
        explore_board.append([])
        for j in range(len(level1[i])):
            if level1[i][j] < 3:
                explore_board[i].append(" ")
            else:
                explore_board[i].append("#")
    ai = Algorithms(food_positions)

#draw initial player
def draw_initial_player():
    global PacMan, state, frame, turn_allowed, blinky, pinky, inky, clyde
    if PacMan.cdirection == 0: #Right
        for i in range (0, 4):  
            PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 0)
    if PacMan.cdirection == 1: # Left
        for i in range (0, 4):
            PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 180)    
    if PacMan.cdirection == 2: #Up
        for i in range (0, 4):  
            PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 90)
    if PacMan.cdirection == 3: #Down
        for i in range (0, 4):  
            PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = -90)
            
    update_player(frame)
  
# going throught each frame of the PacMan cycle
def update_player(frame) : 
    global state, PacMan, count, flicker
    top_frame.img = ImageTk.PhotoImage(PacMan.imgs[frame])
    top_frame.create_image(PacMan.x, PacMan.y, image=top_frame.img, anchor= CENTER)

# create each ghost on the screen
def ghost_instance():
    top_frame.img1 = ImageTk.PhotoImage(blinky.imgs[0]) 
    top_frame.img2 = ImageTk.PhotoImage(pinky.imgs[0])
    top_frame.img3 = ImageTk.PhotoImage(inky.imgs[0])
    top_frame.img4 = ImageTk.PhotoImage(clyde.imgs[0])    

def draw_ghost(A, B):
     #if (not PacMan.powerup and not A.dead) or (eaten_ghost[A.id]): 
     global PacMan, eaten_ghost, life, hit
     if PacMan.powerup != True:
        top_frame.create_image(A.x, A.y, image= B, anchor=CENTER)
        if (A.center_x // num1 == PacMan.center_x // num1 and A.center_y // num2 == PacMan.center_y // num2 and hit == False):
           life -= 1
           hit = True
     else:
        if (A.center_x // num1 == PacMan.center_x // num1 and A.center_y // num2 == PacMan.center_y // num2):
            eaten_ghost[A.id] = True
        if eaten_ghost[A.id] == True :
            top_frame.create_image(A.x, A.y, image= top_frame.dead, anchor = CENTER)
        else:
            top_frame.create_image(A.x, A.y, image= top_frame.spooked, anchor = CENTER)

def check_position(A) :
    turn = [False, False, False, False]
    if A.center_x // row < row :
        if A.cdirection == 0: 
            if level[A.center_y // num1][(A.center_x + num3 - 1) // num2] >= 3 :
                A.state = -1
                #print (f'{A.name} contact right')
            if level[A.center_y // num1][(A.center_x - num2) // num2] < 3:
                turn[1] = True
                
        if A.cdirection == 1:
            if level[A.center_y // num1][(A.center_x - num2 + 1) // num2] >= 3 :
                A.state = -1 
                #print(f'{A.name} contact left')
            if level[A.center_y // num1][(A.center_y + num3) // num2] < 3:
                turn[0] = True
                
        if A.cdirection == 2:
            if level[(A.center_y - num1) // num1][(A.center_x) // num2] >= 3 :
                A.state = -1
                #print(f'{A.name} contact up')
            if level[(A.center_y + num3) // num1][(A.center_x) // num2] < 3:
                turn[3] = True
                
        if A.cdirection == 3:
            if level[(A.center_y + num3) // num1][(A.center_x) // num2] >= 3 :
                A.state = -1
                #print (f'{A.name} contact Down')
            if level[(A.center_y - num1) // num1][(A.center_x) // num2] < 3:
                turn[2] = True
                
                
        if A.cdirection == 2 or A.cdirection == 3 :
            if num2 - num3 <= A.center_x % num2 <= num2 + num3 :
                if level[(A.center_y + num3) // num1][(A.center_x) // num2] < 3 :
                    turn[3] = True
                if level[(A.center_y - num3) // num1][(A.center_x) // num2] < 3 :
                    turn[2] = True
            if num1 - num3 <= A.center_y % num1 <= num1 + num3 :
                if level[(A.center_y) // num1][(A.center_x + num2) // num2] < 3 :
                    turn[0] = True
                if level[(A.center_y) // num1][(A.center_x - num2) // num2] < 3 :
                    turn[1] = True
            
        if A.cdirection == 0 or A.cdirection == 1 :
            if num2 - num3 <= A.center_x % num2 <= num2 + num3 :
                if level[(A.center_y + num1) // num1][(A.center_x) // num2] < 3 :
                    turn[3] = True
                if level[(A.center_y - num1) // num1][(A.center_x) // num2] < 3 :
                    turn[2] = True
            if num1 - num3 <= A.center_y % num1 <= num1 + num3 :
                if level[(A.center_y) // num1][(A.center_x + num2) // num2] < 3 :
                    turn[0] = True
                if level[(A.center_y) // num1][(A.center_x - num2) // num2] < 3 :
                    turn[1] = True
    else: 
        turn [0] = True
        turn [1] = True
    A.turn_allowed = turn

def check_collison(score):
    global PacMan, level
    if  0 < PacMan.x < 600 :
        if level[PacMan.center_y // num1][PacMan.center_x//num2] == 1:
            level[PacMan.center_y // num1][PacMan.center_x//num2] = 0
            score += 10
        if level[PacMan.center_y// num1][PacMan.center_x//num2] == 2:
            level[PacMan.center_y// num1][PacMan.center_x//num2] = 0
            PacMan.powerup = True
            score += 50
    return score

# movement control
def move_left(event):
    global PacMan
    PacMan.state = 1
    PacMan.direction = 1
    #print('Key A is pressed')
    history.append('A')
    check_position(PacMan)
    PacMan.change_direction_player()
def move_right(event):
    global PacMan
    PacMan.state = 1
    PacMan.direction = 0
    #print('Key D is pressed')
    history.append('D')
    check_position(PacMan)
    PacMan.change_direction_player()
def move_up(event):
    global PacMan
    PacMan.state = 1
    PacMan.direction = 2
    #print('Key W is pressed')
    history.append('W')
    check_position(PacMan)
    PacMan.change_direction_player()
def move_down(event):
    global PacMan
    PacMan.state = 1
    PacMan.direction = 3
    #print('Key S is pressed')
    history.append('S')
    check_position(PacMan)
    PacMan.change_direction_player()
    
# other control    
def pause(event):
    global PacMan, mode, goal_score
    PacMan.state = -1
    mode = 1
    goal_score = goal_point(level)
    #print (goal_score)
    
#end Function
def print_history():
    print('--------------------------')
    for i in range (len(history)):
        print(f'{i +1}: ', history[i])    
    # print(blinky.center_x // num2)
    # print(blinky.center_y // num1)
    # print(num1)
    # print(num2)
    # print(num3)
    # print(row)
    # print(column)
    
def play_PacMan():
    global start, moving, time_start
    if moving == 1:
        moving = 0
    start = 1
    PacMan.state = 1
    update_game_status('Playing')
    time_start = time.time()
    # key bind
    bA = root.bind('a', move_left)
    bL =root.bind('<Left>',move_left)
    bS = root.bind('s', move_down)
    bDw = root.bind('<Down>',move_down)
    bW = root.bind('w', move_up)
    bU = root.bind('<Up>',move_up)
    bD = root.bind('d', move_right)
    bR = root.bind('<Right>',move_right)
    bP = root.bind('p', pause)
    
def solve_PacMan():
    global moving, start, time_start
    moving = 1
    start = 1
    PacMan.state = 1
    time_start = time.time()
    
def choose_algorithm():
    global ai, solution, depth, nodes, cost
    if ai.solution_ptr == len(ai.solution):
        reset_ai()
        update_game_status('Calculating')
        draw_random(0)
        top_frame.delete('all')
        draw_board()
        if ai.name == "":
            ai.name = algorithm_text.get()
        ai.start_node = Node(PacMan, level, score, ai.depth, [], 0)
        
    while ai.solution_ptr == len(ai.solution):
        if ai.name == 'Depth First Search':
            ai.depth_first_search()
        elif ai.name == 'Breadth First Search':
            ai.breadth_first_search()
        elif ai.name == 'Uniform Cost Search':
            ai.uniform_cost_search()
        elif ai.name == 'Greedy Search':
            ai.greedy_search()
        elif ai.name == 'A-star Search':
            ai.a_star_search()
            
        update_explore_board()
        os.system("cls")
        draw_explored_board()
        top_frame.delete('all')
        draw_board()
        time.sleep(0.5)
        
    update_game_status('Solving')
    PacMan.direction = ai.solution[ai.solution_ptr]
    ai.solution_ptr += 1
    
    if ai.solution_ptr == len(ai.solution):
        solution.extend(ai.solution)
        depth += ai.depth
        nodes += ai.nodes
        cost += ai.cost
    return True

def update_explore_board():
    global explore_board
    # solution tile "S"
    if len(ai.solution) > 0:
        node = Node(PacMan, level, score, ai.depth, [], 0)
        for i in range(len(ai.solution)):
            node.expand()
            for j in range(len(node.nodes)):
                if node.nodes[j].direction == ai.solution[i]:
                    node = node.nodes[j].copy()
                    break
            curr_node = node.copy()
            curr_node.get_backward_move()
            curr_node.check_position()
            curr_node.PacMan.state = 1
            PacMan_y, PacMan_x = curr_node.PacMan.get_matrix_position()
            explore_board[PacMan_y][PacMan_x] = "S"
            while curr_node.PacMan.state == 1:
                curr_node.PacMan.move()
                PacMan_y, PacMan_x = curr_node.PacMan.get_matrix_position()
                if curr_node.PacMan.matrix_y != PacMan_y or curr_node.PacMan.matrix_x != PacMan_x:
                    curr_node.check_position()
                    curr_node.PacMan.check_state()
                explore_board[PacMan_y][PacMan_x] = "S"
        return
        
    # frontier tile "F" and explored tile "."
    ai.check_list.append(ai.start_node)
    for i in range(len(ai.check_list) - 1, -1, -1):
        curr_node = ai.check_list[i].copy()
        PacMan_y, PacMan_x = curr_node.PacMan.get_matrix_position()
        explore_board[PacMan_y][PacMan_x] = "F"
        curr_node.get_backward_move()
        curr_node.check_position()
        curr_node.PacMan.state = 1
        while curr_node.PacMan.state == 1:
            curr_node.PacMan.move()
            PacMan_y, PacMan_x = curr_node.PacMan.get_matrix_position()
            if curr_node.PacMan.matrix_y != PacMan_y or curr_node.PacMan.matrix_x != PacMan_x:
                curr_node.check_position()
                curr_node.PacMan.check_state()
                explore_board[PacMan_y][PacMan_x] = "."
    ai.check_list.pop()

# main loop
def main():
    global PacMan, flicker_time, flicker, frame, count, score, state, powerup_counter, life, eaten_ghost, hit, mode, start, loading_index, time_start, time_end
    if mode == 0 :
        #update board
        top_frame.delete('all')
        draw_board()
        draw_ghost(blinky, top_frame.img1)
        draw_ghost(pinky, top_frame.img2)
        draw_ghost(inky, top_frame.img3)
        draw_ghost(clyde, top_frame.img4)
        if loading_index == 4:
            loading_index = 0
        if start != -1:
            check_position(blinky)
            blinky.change_direction()
            check_position(pinky)
            pinky.change_direction()
            check_position(inky)
            inky.change_direction()
            check_position(clyde)
            clyde.change_direction()
            if moving == 1 :
                PacMan.check_state()
                if PacMan.state == -1:
                    if choose_algorithm():
                        PacMan.state = 1
                        PacMan.change_direction_player()
                PacMan.move()
            else:
                PacMan.move()
            update_player(frame)
            check_position(PacMan)
            PacMan.change_direction_player()
            
            #sum score and update score
            score = check_collison(score)
            update_score(score)
            if score == goal_score:
                loading_index = 0
                time_end = time.time()
                if moving == 1:
                    status = f'FINISHED! Time = {round((time_end - time_start), 2)}s\rDepth = {ai.depth}, Nodes = {ai.nodes}'
                    if ai.name == 'Uniform Cost Search':
                        status += f"\rCost = {cost}"
                    if ai.name == 'Greedy Search':
                        status += f"\rH value = {round(cost, 1)}"
                    if ai.name == 'A-star Search':
                        status += f"\rF value = {round(cost, 1)}"
                    update_game_status(status)
                else:
                    update_game_status(f'WIN! Time = {round((time_end - time_start), 2)}s')
                start = -1
            if life == 0:
                start = -1
                update_game_status('Game Over!')
                
            # debug console
            # check_position(blinky)
            # if blinky.state == 1:
            #     check_collison(blinky)
            # for i in range (0, 4):
            #     print(PacMan.turn_allowed[i])
            # for i in range (0, 4):
            #     print(blinky.turn_allowed[i])
            # print('y: ',blinky.center_y // num1, ' x: ', blinky.center_x // num2, 'state: ', blinky.state, 'cdirec: ', blinky.cdirection)
            # print('------------------------------------------')
            
            # main functionality
            frame = (frame + 1) % len(PacMan.imgs)
            if count < 19: # control the cycle of PacMan
                count += 1
                if count > 1:
                    flicker = False
            else:
                loading_index += 1
                flicker = True
                count = 0
                hit = False

            if PacMan.powerup == True and powerup_counter < 100:
                powerup_counter += 1
            elif PacMan.powerup == True and powerup_counter >= 100:
                powerup_counter = 0
                PacMan.powerup = False
                eaten_ghost = [False, False, False, False]
            draw_random(loading_index)  
        else:
            check_position(PacMan)
            draw_initial_player()
        root.after(1000 // desired_fps, main)
    else:
        print('program has been stopped!')
        slide_arr(history)
        # print_history()
    
draw_panel()
ghost_instance()
main()
    
root.mainloop()