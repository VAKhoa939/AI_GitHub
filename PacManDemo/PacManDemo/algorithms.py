from pacman import *
from node import *

class Algorithms:
    def __init__(self, pacman, board, total_point, max_point):
        self.solution = []
        self.start_node = Node(pacman, board, total_point, max_point)

    def depth_first_search(self):
        check_list = []
        explored = []
        check_list.append(self.start_node)
        while check_list:
            node = check_list.pop(0)
    