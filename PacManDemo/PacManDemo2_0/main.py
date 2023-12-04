import os
import time
from algorithms import *
from pacman import *
from node import *


# global variables
init_board = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", " ", "#", "#", "#", "#", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", "o", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]
# init_board = [
#     ["#", "#", "#", "#", "#", "#", "#"],
#     ["#", "o", "o", "o", "o", "o", "#"],
#     ["#", "o", "#", "#", "#", "o", "#"],
#     ["#", "o", "o", "o", "o", "o", "#"],
#     ["#", "o", "#", "#", "#", "o", "#"],
#     ["#", "o", "o", "o", "o", "o", "#"],
#     ["#", "#", "#", "#", "#", "#", "#"],
# ]
curr_board = []
explore_board = []
food_positions = []
for i in range(len(init_board)):
    explore_board.append([])
    for j in range(len(init_board[i])):
        if init_board[i][j] != "#":
            explore_board[i].append(" ")
            if init_board[i][j] == "o":
                food_positions.append((i, j))
        else:
            explore_board[i].append(init_board[i][j])
    curr_board.append(init_board[i].copy())
max_point = 0
total_point = 0
game_mode = "manual"
pacman = PacMan(0, 0)
ai = Algorithms(food_positions)
solution = []
depth = 0
nodes = 0
cost = 0


# functions
def reset_board():
    global curr_board, explore_board, food_positions, max_point, total_point, game_mode, pacman, ai, solution, depth, nodes, cost
    curr_board.clear()
    explore_board.clear()
    food_positions.clear()
    for i in range(len(init_board)):
        explore_board.append([])
        for j in range(len(init_board[i])):
            if init_board[i][j] != "#":
                explore_board[i].append(" ")
            else:
                explore_board[i].append(init_board[i][j])
                if init_board[i][j] == "o":
                    food_positions.append((i, j))
        curr_board.append(init_board[i].copy())
    max_point = count_point()
    total_point = 0
    game_mode = "manual"
    pacman = PacMan(0, 0)
    ai = Algorithms(food_positions)
    solution.clear()
    depth = 0
    nodes = 0
    cost = 0
    
def reset_ai():
    global explore_board, ai, depth, nodes, cost
    explore_board.clear()
    for i in range(len(init_board)):
        explore_board.append([])
        for j in range(len(init_board[i])):
            if init_board[i][j] != "#":
                explore_board[i].append(" ")
            else:
                explore_board[i].append(init_board[i][j])
    ai_name = ai.name
    ai = Algorithms(food_positions)
    ai.name = ai_name

def draw_board():
    for i in range(len(curr_board)):
        for j in range(len(curr_board[i])):
            pacman_y, pacman_x = pacman.find_position()
            if i == pacman_y and j == pacman_x:
                print("P", end = " ")
            else:
                print(curr_board[i][j], end = " ")
        print(end = "    ")
        for j in range(len(explore_board[i])):
            print(explore_board[i][j], end = " ")
        print()
        
def count_point():
    max_point = 0
    for i in range(len(curr_board)):
        for j in range(len(curr_board[i])):
            if curr_board[i][j] == "o":
                max_point += 1
    return max_point
                
def eat_point():
    global total_point
    pacman_y, pacman_x = pacman.find_position()
    if curr_board[pacman_y][pacman_x] == "o":
        curr_board[pacman_y][pacman_x] = " "
        total_point += 1
        
def check_position(subject):
    subject.turn_allowed = [False, False, False, False]
    pacman_y, pacman_x = subject.find_position()
    if curr_board[pacman_y - 1][pacman_x] != "#":
        subject.turn_allowed[0] = True
    if curr_board[pacman_y][pacman_x + 1] != "#":
        subject.turn_allowed[1] = True
    if curr_board[pacman_y + 1][pacman_x] != "#":
        subject.turn_allowed[2] = True
    if curr_board[pacman_y][pacman_x - 1] != "#":
        subject.turn_allowed[3] = True
        
def update_explore_board():
    global explore_board
    # solution tile "S"
    if len(ai.solution) > 0:
        node = Node(pacman, curr_board, total_point, ai.depth, [], 0)
        for i in range(len(ai.solution)):
            node.expand()
            for j in range(len(node.nodes)):
                if node.nodes[j].direction == ai.solution[i]:
                    node = node.nodes[j].copy()
                    break
            curr_node = node.copy()
            curr_node.get_backward_move()
            curr_node.check_position()
            curr_node.pacman.state = "run"
            pacman_y, pacman_x = curr_node.pacman.find_position()
            explore_board[pacman_y][pacman_x] = "S"
            while curr_node.pacman.state == "run":
                curr_node.pacman.move()
                curr_node.check_position()
                curr_node.pacman.check_state()
                pacman_y, pacman_x = curr_node.pacman.find_position()
                if explore_board[pacman_y][pacman_x] != "S":
                    explore_board[pacman_y][pacman_x] = "S"
        return
        
    # frontier tile "F" and explored tile "x"
    ai.check_list.append(ai.start_node)
    for i in range(len(ai.check_list) - 1, -1, -1):
        curr_node = ai.check_list[i].copy()
        curr_node.get_backward_move()
        curr_node.check_position()
        curr_node.pacman.state = "run"
        pacman_y, pacman_x = curr_node.pacman.find_position()
        explore_board[pacman_y][pacman_x] = "F"
        while curr_node.pacman.state == "run":
            curr_node.pacman.move()
            curr_node.check_position()
            curr_node.pacman.check_state()
            pacman_y, pacman_x = curr_node.pacman.find_position()
            if explore_board[pacman_y][pacman_x] != "x":
                explore_board[pacman_y][pacman_x] = "x"
    ai.check_list.pop()
        
def is_goal():
    global game_mode
    if total_point == max_point:
        print("Finished! You have eaten all points!")
        if game_mode == "ai":
            print("Depth = {0}, Nodes = {1}".format(depth, nodes), end = "")
            if ai.name == "ucs":
                print(", Cost = {0}".format(cost), end = "")
            print()
            print("Solution:", end = " ")
            for direction in solution:
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
    global ai, solution, depth, nodes, cost
    if ai.solution_ptr == len(ai.solution):
        reset_ai()
        os.system("cls")
        draw_board()
        if ai.name == "":
            ai.name = input("Type an algorithm: ")
        ai.start_node = Node(pacman, curr_board, total_point, ai.depth, [], 0)
    while ai.solution_ptr == len(ai.solution):
        if ai.name == "dfs":
            ai.depth_first_search()
        if ai.name == "bfs":
            ai.breadth_first_search()
        if ai.name == "ucs":
            ai.uniform_cost_search()
        if ai.name == "a star":
            ai.a_star_search()
        os.system("cls")
        update_explore_board()
        draw_board()
        time.sleep(0.2)
    pacman.direction = ai.solution[ai.solution_ptr]
    ai.solution_ptr += 1
    if ai.solution_ptr == len(ai.solution):
        solution.extend(ai.solution)
        depth += ai.depth
        nodes += ai.nodes
        cost += ai.cost
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