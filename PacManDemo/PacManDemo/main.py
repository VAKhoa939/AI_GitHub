import os
import time
from algorithms import Algorithms
from pacman import *


# global variables
init_board = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "o", "o", "o", "o", "o", "o", "o", "o", "o", "#"],
    ["#", "o", "#", "#", "#", "o", "#", "o", "#", "o", "#"],
    ["#", "o", "o", "o", "o", "o", "#", "o", "#", "o", "#"],
    ["#", "o", "#", "#", "#", "o", "#", "o", "#", "o", "#"],
    ["#", "o", "o", "o", "o", "o", "o", "o", "o", "o", "#"],
    ["#", "o", "#", "#", "#", "o", "#", "o", "#", "o", "#"],
    ["#", "o", "o", "o", "o", "o", "#", "o", "#", "o", "#"],
    ["#", "o", "#", "#", "#", "o", "#", "o", "#", "o", "#"],
    ["#", "o", "o", "o", "o", "o", "o", "o", "o", "o", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]
curr_board = []
for i in range(len(init_board)):
    curr_board.append(init_board[i].copy())
max_point = 0
total_point = 0
game_mode = "manual"
pacman = PacMan(0, 0)
ai = Algorithms(pacman, curr_board, total_point, max_point)
ai_name = ""


# functions
def reset_board():
    global curr_board, max_point, total_point, game_mode, pacman, ai, ai_name
    curr_board.clear()
    for i in range(len(init_board)):
        curr_board.append(init_board[i].copy())
    max_point = count_point()
    total_point = 0
    game_mode = "manual"
    pacman = PacMan(0, 0)
    ai = Algorithms(pacman, curr_board, total_point, max_point)
    ai_name = ""

def draw_board():
    for i in range(len(curr_board)):
        for j in range(len(curr_board[i]) - 1):
            p_y, p_x = pacman.find_position()
            if i == p_y and j == p_x:
                print("P", end = " ")
            else:
                print(curr_board[i][j], end = " ")
        print(curr_board[i][len(curr_board[i]) - 1])
        
def count_point():
    max_point = 0
    for i in range(len(curr_board)):
        for j in range(len(curr_board[i])):
            if curr_board[i][j] == "o":
                max_point += 1
    return max_point
                
def eat_point():
    global total_point
    p_y, p_x = pacman.find_position()
    if curr_board[p_y][p_x] == "o":
        curr_board[p_y][p_x] = "."
        total_point += 1
        
def check_position(subject):
    subject.turn_allowed = [False, False, False, False]
    p_y, p_x = subject.find_position()
    if curr_board[p_y - 1][p_x] != "#":
        subject.turn_allowed[0] = True
    if curr_board[p_y][p_x + 1] != "#":
        subject.turn_allowed[1] = True
    if curr_board[p_y + 1][p_x] != "#":
        subject.turn_allowed[2] = True
    if curr_board[p_y][p_x - 1] != "#":
        subject.turn_allowed[3] = True
        
def play_manual():
    global game_mode
    command = input("Type a move or a command: ")
    if command == "exit":
        return False
    if command == "reset":
        os.system("cls")
        reset_board()
        return True
    if command == "gm ai":
        game_mode = "ai"
        return True
    pacman.direction = command
    return True

def play_ai():
    global ai_name
    if len(ai.solution) == 0:
        if ai_name == "":
            ai_name = input("Type an algorithm: ")
        if ai_name == "dfs":
            ai.depth_first_search()
    else:
        pacman.direction = ai.solution.pop(0)
    return True
        
def make_decision():
    if game_mode == "manual":
        return play_manual()
    if game_mode == "ai":
        return play_ai()

def main():
    while True:
        os.system("cls")
        pacman.move()
        eat_point()
        draw_board()
        check_position(pacman)
        pacman.check_state()
        print("Total points: ", total_point)
        time.sleep(0.2)
        if pacman.state == "stop":
            if not make_decision():
                os.system("cls")
                return
       
        
# main program
draw_board()
eat_point()
print("Total points: ", total_point)
main()