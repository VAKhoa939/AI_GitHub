import random, time
from pieces import Pieces

class Algorithms:
    def __init__(self, puzzle, algorithm_text):
        self.puzzle = puzzle
        self.name = algorithm_text.get()
        self.solution = []
        self.max_depth = 1
        self.nodes = 1
        self.g = 1000000
        

    def dfs(self):
        print("Start! Max depth = {}, Nodes = {}".format(self.max_depth, self.nodes))
        depth = 1
        check_list = []
        explored = []
        prev_explored = []
        prev_explored_id = -1
        check_list.append(self.puzzle.curr_state.copy_pieces())
        explored.append(self.puzzle.curr_state.copy_pieces())
        prev_explored.append(prev_explored_id)
        while True:
            neighbors = self.puzzle.curr_state.get_neighbors()
            no_neighbors = len(neighbors)
            no_unvis_neighbors = 0
            for _ in range(no_neighbors):
                neighbor = neighbors.pop(random.randint(0, len(neighbors) - 1)).copy_pieces()
                # neighbor = neighbors.pop().copy_pieces()
                if not self.__is_visited(neighbor, explored):
                    if depth < self.puzzle.random_moves:
                        check_list.append(neighbor.copy_pieces())
                        no_unvis_neighbors += 1
            if no_unvis_neighbors > 0:
                self.puzzle.curr_state = check_list.pop().copy_pieces()
                depth += 1
                if depth > self.max_depth:
                    self.max_depth = depth
                prev_explored.append(len(explored) - 1)
                prev_explored_id = prev_explored[-1]
            else:
                if prev_explored_id == -1:
                    break
                self.puzzle.curr_state = explored[prev_explored_id].copy_pieces()
                depth -= 1
                prev_explored_id = prev_explored[prev_explored_id]
                prev_explored.append(prev_explored_id)
            self.nodes += 1
            explored.append(self.puzzle.curr_state.copy_pieces())
            self.puzzle.update_puzzle()
            print("Depth = {}, Nodes = {}, Blank_pos: ({}, {}), Prev_id = {}".format(depth, self.nodes, self.puzzle.curr_state.blank_row, self.puzzle.curr_state.blank_col, prev_explored_id))
            time.sleep(0.1)
            if self.puzzle.is_goal():
                break
        print("Finished! Max depth = {}, Nodes = {}".format(self.max_depth, self.nodes))
        self.solution.extend(explored)
        
        
    def bfs(self):
        print("Start! Depth = {}, Nodes = {}".format(self.max_depth, self.nodes))
        check_list = []
        explored = []
        prev_explored = []
        prev_explored_id = -1
        check_list.append(self.puzzle.curr_state.copy_pieces())
        prev_explored.append(prev_explored_id)
        while True:
            check_list_size = len(check_list)
            for _ in range(check_list_size):
                self.puzzle.curr_state = check_list.pop(0).copy_pieces()
                explored.append(self.puzzle.curr_state.copy_pieces())
                for i in range(len(explored)):
                    if self.puzzle.curr_state.compare_pieces(explored[i]):
                        prev_explored_id = i
                        break
                if self.puzzle.is_goal():
                    break
                neighbors = self.puzzle.curr_state.get_neighbors()
                for neighbor in neighbors:
                    if not self.__is_visited(neighbor, explored):
                        check_list.append(neighbor.copy_pieces())
                        prev_explored.append(prev_explored_id)
                        self.nodes += 1
                        print("Depth = {}, Nodes = {}, Blank_pos: ({}, {}), Prev_id = {}".format(self.max_depth, self.nodes, neighbor.blank_row, neighbor.blank_col, prev_explored_id))
            if self.puzzle.is_goal():
                break
            self.max_depth += 1
        print("Finished! Depth = {}, Nodes = {}".format(self.max_depth, self.nodes))
        while prev_explored_id != -1:
            self.solution.insert(0, explored[prev_explored_id])
            prev_explored_id = prev_explored[prev_explored_id]
        
    def ucs(self):
        print("Start! Depth = {}, Nodes = {}, Cost = {}".format(self.max_depth, self.nodes, self.puzzle.curr_state.g))
        depth = 1
        check_list = []
        explored = []
        prev_explored = []
        prev_explored_id = -1
        check_list.append(self.puzzle.curr_state.copy_pieces())
        prev_explored.append(prev_explored_id)
        while True:
            min_id = -1
            min_g = 1000000
            for i in range(len(check_list)):
                if check_list[i].g < min_g:
                    min_id = i
                    min_g = check_list[i].g
            if min_id == -1:
                break
            self.puzzle.curr_state = check_list.pop(min_id).copy_pieces()
            if self.puzzle.curr_state.g >= self.g:
                continue
            for i in range(len(explored)):
                if self.puzzle.curr_state.compare_pieces(explored[i]):
                    prev_explored_id = i
                    break
            print("Depth = {}, Nodes = {}, Blank_pos: ({}, {}), Prev_id = {}, G = {}".format(depth, self.nodes, self.puzzle.curr_state.blank_row, self.puzzle.curr_state.blank_col, prev_explored_id, self.puzzle.curr_state.g))
            depth += 1
            if depth > self.max_depth:
                self.max_depth = depth
            self.nodes += 1
            if self.puzzle.is_goal():
                print("Found a solution!")
                if self.puzzle.curr_state.g < self.g: 
                    solution = []
                    while prev_explored_id != -1:
                        solution.insert(0, explored[prev_explored_id])
                        prev_explored_id = prev_explored[prev_explored_id]
                    self.solution.clear()
                    no_steps = len(solution)
                    for _ in range(no_steps):
                        self.solution.append(solution.pop(0).copy_pieces())
                    self.g = self.puzzle.curr_state.g
                continue
            neighbors = self.puzzle.curr_state.get_neighbors()
            no_neighbors = len(neighbors)
            for _ in range(no_neighbors):
                neighbor = neighbors.pop().copy_pieces()
                if not self.__is_visited(neighbor, explored):
                    check_list.append(neighbor.copy_pieces())
        print("Finished! Depth = {}, Nodes = {}".format(self.max_depth, self.nodes))
    

    def greedy(self):
        pass
    
    def a_star(self):
        pass
    
    def __is_visited(self, neighbor, explored):
        for state in explored:
            if neighbor.compare_pieces(state):
                return True
        return False
    
    
    def __sort_list_ucs(self, check_list):
        pass
