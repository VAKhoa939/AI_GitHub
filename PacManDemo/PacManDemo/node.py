from pacman import *

class Node:
    def __init__(self, pacman, board, total_point, max_point):
        self.board = []
        for i in range(len(board)):
            self.board.append(board[i].copy())
        self.pacman = PacMan(pacman.x, pacman.y)
        self.pacman.direction = pacman.direction
        self.nodes = []
        self.total_point = total_point
        self.max_point = max_point
        self.state = False
        
    def expand(self):
        directions = ["u", "r", "d", "l"]
        self.check_position()
        for i in range(4):
            if self.pacman.turn_allowed[i] == True:
                node = Node(self.pacman, self.board, self.total_point, self.max_point)
                node.pacman.direction = directions[i]
                node.pacman.check_state()
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
            self.state = True
            
    def move(self):             
        self.pacman.check_state()
        while self.pacman.state == "run":
            self.pacman.move()
            self.eat_point()
            self.check_position()
            self.pacman.check_state()