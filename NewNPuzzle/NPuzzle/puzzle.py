from pieces import Pieces
import random, time

class Puzzle:
    def __init__(self, root, state):
        self.root = root
        self.init_state = state
        self.curr_state = self.init_state.copy_pieces()
        self.goal_state = self.init_state.copy_pieces()
        self.random_moves = 0
        

    def draw_puzzle(self):
        for i in range(self.curr_state.rows):
            for j in range(self.curr_state.columns):
                self.curr_state.pieces[i][j].image.grid(row = i, column = j)
        

    def remove_puzzle(self):
        for i in range(self.curr_state.rows):
            for j in range(self.curr_state.columns):
                self.curr_state.pieces[i][j].image.grid_remove()
                

    def update_puzzle(self):
        self.remove_puzzle()
        self.draw_puzzle()
        self.root.update()
        

    def randomize(self):
        times = self.curr_state.columns * self.curr_state.rows
        for _ in range(times):
            move = random.choice(self.curr_state.find_avail_moves())
            self.curr_state.move(move)
            if self.is_goal():
                self.curr_state.move_backward(move)
                times += 1
        self.init_state = Pieces.copy_pieces(self.curr_state)
        self.random_moves += times
        

    def is_goal(self):
        return self.curr_state.compare_pieces(self.goal_state)
        

    def reset(self):
        self.curr_state = self.init_state.copy_pieces()
        

    def show_solution(self, algorithms):
        print("Solution:", end = " ")
        no_steps = len(algorithms.solution)
        for _ in range(no_steps):
            self.curr_state = algorithms.solution.pop(0).copy_pieces()
            self.update_puzzle()
            if algorithms.name == "Breadth First Search":
                print("({}, {})".format(self.curr_state.blank_row, self.curr_state.blank_col), end = ", ")
            if algorithms.name == "Uniform Cost Search":
                print("({}, {})".format(self.curr_state.blank_row, self.curr_state.blank_col, self.curr_state.g), end = ", ")
            time.sleep(0.1)
        print("")
        