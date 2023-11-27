from player import *

class Node:
    def __init__(self, pacman, board, total_point, max_point):
        self.board = []
        for i in range(len(board)):
            self.board.append(board[i].copy())
        self.pacman = player(pacman.x, pacman.y)
        self.pacman.direction = pacman.direction
        self.nodes = []
        self.total_point = total_point
        self.max_point = max_point
        self.direction = pacman.direction
    
    def compare(self, other):
        if self.pacman.x != other.pacman.x or self.pacman.y != other.pacman.y or self.total_point != other.total_point:
            return False
        return True
        
    def expand(self):
        directions = ["u", "r", "d", "l"]
        self.check_position()
        for i in range(4):
            if self.pacman.turn_allowed[i] == True:
                node = Node(self.pacman, self.board, self.total_point, self.max_point)
                node.direction = directions[i]
                node.pacman.direction = directions[i]
                node.move()
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
            self.board[p_y][p_x] = "."
            self.total_point += 1
            
    def move(self):
        self.check_position()
        self.pacman.state = "run"
        while self.pacman.state == "run":
            self.pacman.move()
            self.eat_point()
            self.check_position()
            self.pacman.check_state()
            
    def is_goal(self):
        return self.total_point == self.max_point
            
