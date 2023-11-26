import os
import time
from algorithms import *
from pacman import *
from node import *


# global variables
# init_board = [
#     ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
#     ["#", "o", "o", "o", "o", "o", "o", "o", "o", "o", "#"],
#     ["#", "o", "#", "#", "#", "o", "#", "o", "#", "o", "#"],
#     ["#", "o", "o", "o", "o", "o", "#", "o", "#", "o", "#"],
#     ["#", "o", "#", "#", "#", "o", "#", "o", "#", "o", "#"],
#     ["#", "o", "o", "o", "o", "o", "o", "o", "o", "o", "#"],
#     ["#", "o", "#", "#", "#", "o", "#", "o", "#", "o", "#"],
#     ["#", "o", "o", "o", "o", "o", "#", "o", "#", "o", "#"],
#     ["#", "o", "#", "#", "#", "o", "#", "o", "#", "o", "#"],
#     ["#", "o", "o", "o", "o", "o", "o", "o", "o", "o", "#"],
#     ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
# ]
init_board = [
    ["#", "#", "#", "#", "#", "#", "#"],
    ["#", "o", "o", "o", "o", "o", "#"],
    ["#", "o", "#", "#", "#", "o", "#"],
    ["#", "o", "o", "o", "o", "o", "#"],
    ["#", "o", "#", "#", "#", "o", "#"],
    ["#", "o", "o", "o", "o", "o", "#"],
    ["#", "#", "#", "#", "#", "#", "#"],
]
curr_board = []
for i in range(len(init_board)):
    curr_board.append(init_board[i].copy())
max_point = 0
total_point = 0
game_mode = "manual"
pacman = PacMan(0, 0)
ai = Algorithms()
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
    ai = Algorithms()
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
        
def is_goal():
    global game_mode
    if total_point == max_point:
        print("Finished! You have eaten all points!")
        if game_mode == "ai":
            print("Depth = {0}, Nodes = {1}".format(ai.depth, ai.nodes))
            print("Solution:", end = " ")
            for direction in ai.solution:
                print(direction, end = ", ")
            print()
            game_mode = "manual"
        pacman.direction = ""
        pacman.check_state()
        
        
def play_manual():
    global game_mode
    command = input("Type a move or a command: ")
    if command == "exit":
        return False
    if command == "reset":
        os.system("cls")
        reset_board()
    elif command == "gm ai":
        game_mode = "ai"
    elif command in ["u", "r", "d", "l"]:
        pacman.direction = command
    return True

def play_ai():
    global ai_name
    if ai.sol_ptr == len(ai.solution):
        if ai_name == "":
            ai_name = input("Type an algorithm: ")
        start_node = Node(pacman, curr_board, total_point, max_point)
        if ai_name == "dfs":
            ai.depth_first_search(start_node)
    else:
        pacman.direction = ai.solution[ai.sol_ptr]
        ai.sol_ptr += 1
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
        is_goal()
        time.sleep(0.2)
        if pacman.state == "stop":
            if not make_decision():
                os.system("cls")
                return
       
        
# main program
draw_board()
max_point = count_point()
eat_point()
print("Total points: ", total_point)
main()
# ai.depth_first_search(Node(pacman, curr_board, total_point, max_point))