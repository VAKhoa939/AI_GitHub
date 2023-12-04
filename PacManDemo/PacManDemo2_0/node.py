from pacman import *

class Node:
    def __init__(self, pacman, board, total_point, depth, path, cost):
        self.board = []
        for i in range(len(board)):
            self.board.append(board[i].copy())
        self.pacman = pacman.copy()
        self.nodes = []
        self.total_point = total_point
        self.direction = ""
        self.path = path.copy()
        self.depth = depth
        self.cost = cost
        self.is_goal = False
        self.heuristic_value = 1000000
    
    def copy(self):
        node = Node(self.pacman, self.board, self.total_point, self.depth, self.path, self.cost)
        node.direction = self.direction
        node.is_goal = self.is_goal
        node.heuristic_value = self.heuristic_value
        return node
    
    def compare(self, other):
        if self.pacman.x != other.pacman.x or self.pacman.y != other.pacman.y:
            return False
        return True
    
    def swap(self, other):
        node_a = other.copy()
        node_b = self.copy()
        return node_a, node_b
        
    def expand(self):
        directions = ["u", "r", "d", "l"]
        self.check_position()
        for i in range(4):
            if self.pacman.turn_allowed[i] == True:
                node = self.copy()
                node.direction = directions[i]
                node.pacman.direction = directions[i]
                node.move()
                node.depth += 1
                node.path.append(directions[i])
                self.nodes.append(node)
        
    def check_position(self):
        self.pacman.turn_allowed = [False, False, False, False]
        p_y, p_x = self.pacman.find_position()
        if self.board[p_y - 1][p_x] != "#":
            self.pacman.turn_allowed[0] = True
        if self.board[p_y][p_x + 1] != "#":
            self.pacman.turn_allowed[1] = True
        if self.board[p_y + 1][p_x] != "#":
            self.pacman.turn_allowed[2] = True
        if self.board[p_y][p_x - 1] != "#":
            self.pacman.turn_allowed[3] = True
            
    def eat_point(self):
        p_y, p_x = self.pacman.find_position()
        if self.board[p_y][p_x] == "o":
            self.board[p_y][p_x] = " "
            self.total_point += 1
            self.is_goal = True
            
    def move(self):
        self.check_position()
        self.pacman.state = "run"
        while self.pacman.state == "run":
            self.pacman.move()
            self.cost += 1
            self.eat_point()
            self.check_position()
            self.pacman.check_state()
            
    # def is_goal(self):
    #     if self.total_point == self.max_point:
    #         return True
    #     return False
    
    def get_backward_move(self):
        if self.direction == "":
            return
        directions = ["u", "r", "d", "l"]
        dir_id = directions.index(self.direction)
        self.direction = directions[(dir_id + 2) % 4]
        self.pacman.direction = self.direction
            