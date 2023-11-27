from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from player import *
from style import *
from variable import *
from node import *
from algorithms import *


#initial start location
#PacMan initial
PacMan = player('pacman',(row // 2) * num1 - num1, (column // 2) * num2 + (7 * num2), 0)
player.add_frame(PacMan)
direction = 0
player_imgs.append(PacMan.imgs[0])

#Ghost initial
blinky = ghost('blinky',num1 * 3, num2 * 2 + num3, 0, 'red', 0, True)
blinky.set_target(PacMan.x, PacMan.y)

#(row // 2) * num1 + num1, (column // 2) * num2 - num2
pinky = ghost('pinky',num1 * 3, num2 * 2 + num3, 1, 'pink', 1, True)
pinky.set_target(PacMan.x, PacMan.y)

inky = ghost('inky',num1 * 3, num2 * 2 + num3, 2, 'blue', 2, True)
inky.set_target(PacMan.x, PacMan.y)

clyde = ghost('clyde',num1 * 3, num2 * 2 + num3, 3, 'orange', 3, True)
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
current_status = 'Chosing mode'
status_display.set(str(current_status))

ai = Algorithms()
algorithm_text = StringVar()
edit_text = StringVar()

top_frame = Canvas(root, bg = 'Black', width = WIDTH, height = HEIGHT)
top_frame.pack(padx = 200,side=LEFT)

top_frame.spooked = ImageTk.PhotoImage(spooked_img)
top_frame.dead = ImageTk.PhotoImage(dead_img)

right_frame = Frame(root, bg = 'Black', width = 50, height = HEIGHT)
right_frame.pack(side=LEFT)

top_frame1 = Frame(right_frame, bg = 'Black', width = WIDTH // 4 + 20, height = HEIGHT // 4)
top_frame1.pack()

logo_frame = Image.open('assets/logo/pacman.jpg').resize((WIDTH // 2 + 20, HEIGHT // 4))
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

# GUI function
def draw_panel():
    # First page
    global algorithm_text
    play_button = Button(bot_frame1, font = font ,text = 'Play', command = start_game)
    play_button.pack(pady = 20)
    edit_combobox = ttk.Combobox(bot_frame1, font = font,width = 20, textvariable = algorithm_text)
    edit_combobox['values'] = ('Depth First Search',
                                     'Breadth First Search',
                                     'Uniform Cost Search',
                                     'Greedy Search',
                                     'A-star Search')
    edit_combobox.current(0)
    edit_combobox.pack()
    solve_button = Button(bot_frame1, font = font ,text = 'Solve', command = solve_pacman)
    solve_button.pack(pady = 20)
    # stop_button = Button(bot_frame1, font = font ,text = 'Stop', command = root.destroy)
    # stop_button.pack(pady = 20)
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
    confirm_button = Button(bot_frame2, font = font ,text = 'Confirm', command = root.destroy)
    confirm_button.pack(pady = 20)
    back_button = Button(bot_frame2, font = font ,text = 'Back', command = switch_main_mode)
    back_button.pack(pady = 20)
    
def switch_edit_mode():
    update_game_status('Editing')
    bot_frame1.forget()
    bot_frame2.pack()
    
def switch_main_mode():
    update_game_status('Chosing mode')
    bot_frame2.forget()
    bot_frame1.pack()
   
def update_score(scor):
    global score_display
    score_display.set('score: ' + str(scor))
    
def update_game_status(state):
    global current_status
    current_status = state
    
# Core Function
#draw initil player
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
  
# going throught each frame of the pacman cycle
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
                print (f'{A.name} contact right')
            if level[A.center_y // num1][(A.center_x - num2) // num2] < 3:
                turn[1] = True
                
        if A.cdirection == 1:
            if level[A.center_y // num1][(A.center_x - num2 + 1) // num2] >= 3 :
                A.state = -1 
                print(f'{A.name} contact left')
            if level[A.center_y // num1][(A.center_y + num3) // num2] < 3:
                turn[0] = True
                
        if A.cdirection == 2:
            if level[(A.center_y - num1) // num1][(A.center_x) // num2] >= 3 :
                A.state = -1
                print(f'{A.name} contact up')
            if level[(A.center_y + num3) // num1][(A.center_x) // num2] < 3:
                turn[3] = True
                
        if A.cdirection == 3:
            if level[(A.center_y + num3) // num1][(A.center_x) // num2] >= 3 :
                A.state = -1
                print (f'{A.name} contact Down')
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

def check_collison(scor):
    global PacMan, level
    if  0 < PacMan.x < 650 :
        if level[PacMan.center_y // num1][PacMan.center_x//num2] == 1:
            level[PacMan.center_y // num1][PacMan.center_x//num2] = 0
            scor += 10
        if level[PacMan.center_y// num1][PacMan.center_x//num2] == 2:
            level[PacMan.center_y// num1][PacMan.center_x//num2] = 0
            PacMan.powerup = True
            scor += 50
    return scor

# movement control
def move_left(event):
    global PacMan
    PacMan.state = 1
    PacMan.direction = 1
    print('Key A is pressed')
    history.append('A')
    check_position(PacMan)
    PacMan.change_direction_player()
def move_right(event):
    global PacMan
    PacMan.state = 1
    PacMan.direction = 0
    print('Key D is pressed')
    history.append('D')
    check_position(PacMan)
    PacMan.change_direction_player()
def move_up(event):
    global PacMan
    PacMan.state = 1
    PacMan.direction = 2
    print('Key W is pressed')
    history.append('W')
    check_position(PacMan)
    PacMan.change_direction_player()
def move_down(event):
    global PacMan
    PacMan.state = 1
    PacMan.direction = 3
    print('Key S is pressed')
    history.append('S')
    check_position(PacMan)
    PacMan.change_direction_player()
    
# other control    
def pause(event):
    global PacMan, mode, goal_score
    PacMan.state = -1
    mode = 1
    goal_score = goal_point(level)
    print (goal_score)
    
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
    
def start_game():
    global start, moving
    if moving == 1:
        moving = 0
    start = 1
    PacMan.state = 1
    update_game_status('Playing')
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
    
def solve_pacman():
    global moving, start
    moving = 1
    start = 1
    PacMan.state = 1
    update_game_status('Solving')
    
def choose_algorithm():
    if ai.sol_ptr == len(ai.solution):
        start_node = Node(PacMan, level, score)
        if algorithm_text.get() == 'Depth First Search':
            ai.depth_first_search(start_node)
        return False
    else:
        PacMan.direction = ai.solution[ai.sol_ptr]
        ai.sol_ptr += 1
        return True

# Initialize the player animation
# change the direction of the player
#main 
def main():
    global PacMan, flicker_time, flicker, frame, count, score, state, powerup_counter, life, eaten_ghost, hit, mode, start, loading_index
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
            check_position(blinky)
            
            #sum score and update score
            score = check_collison(score)
            update_score(score)
            if score == goal_score:
                if moving == 1:
                    update_game_status(f'FINISHED!\rDepth = {ai.depth}, Nodes = {ai.nodes}')
                else:
                    update_game_status('WIN!')
                start = -1
            if life == 0:
                start = -1
                update_game_status('Game Over!')
            #debug console
            # for i in range (0, 4):
            #     print(PacMan.turn_allowed[i])
            for i in range (0, 4):
                print(blinky.turn_allowed[i])
            print('y: ',blinky.center_y // num1, ' x: ', blinky.center_x // num2, 'state: ', blinky.state, 'cdirec: ', blinky.cdirection)
            print('------------------------------------------')
            # #main functionality
      
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
                
            # if blinky.state == 1:
            #     check_collison(blinky)

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
        print_history()
    
# draw_board()
draw_panel()
# draw_initial_player()
ghost_instance()
main()
    
root.mainloop()