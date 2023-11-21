from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image
import os, time

from pieces import Piece, Pieces
from puzzle import Puzzle
from algorithms import Algorithms

class GUI:
    def __init__(self, root):
        self.root = root
        self.__font = ("Courier", 14)
        self.__image_size = 450
        self.__image_name = "fox.jpeg"
        self.__image = Image.open("puzz-images/fox.jpeg").resize((self.__image_size, self.__image_size))
        self.__puzzle_rows = 3
        self.__puzzle_columns = 3
        self.__puzzle, self.__state_label = self.draw_gui()


    def draw_gui(self):
        # Divide the screen into 4 frames
        top_frame = Frame(self.root)
        top_frame.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)
        left_frame = Frame(self.root)
        left_frame.grid(row = 1, column = 0,  sticky = W, padx = 10, pady = 10)
        right_frame = Frame(self.root)
        right_frame.grid(row = 1, column = 1, sticky = W, padx = 10, pady = 10)
        bottom_frame = Frame(self.root)
        bottom_frame.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10)
        
        # Top frame
        puzzle_name = Label(top_frame, text = "The N-puzzle", font = ("Courier", 30))
        puzzle_name.grid(row = 0, column = 0, columnspan = 7, pady = 2)

        image_path_label = Label(top_frame, text = self.__image_name, font = self.__font)
        image_path_label.grid(row = 1, column = 1,  sticky = W, padx = 10)
        choose_button = Button(top_frame, text = "Choose image", bd = "5", font = self.__font, command = lambda:self.__open_image(image_path_label))
        choose_button.grid(row = 1, column = 0,  sticky = W, padx = 2)
        
        rows_text = StringVar()
        rows_label = Label(top_frame, text = "Rows: ", font = self.__font)
        rows_label.grid(row = 1, column = 2, sticky = W, padx = 2)
        rows_entry = Entry(top_frame, width = 10, font = self.__font, textvariable = rows_text)
        rows_entry.grid(row = 1, column = 3, sticky = W, padx = 2)
        
        columns_text = StringVar()
        column_label = Label(top_frame, text = "Columns: ", font = self.__font)
        column_label.grid(row = 1, column = 4, sticky = W, padx = 2)
        column_entry = Entry(top_frame, width = 10, font = self.__font, textvariable = columns_text)
        column_entry.grid(row = 1, column = 5, sticky = W, padx = 2)
        
        change_button = Button(top_frame, text = "Change", bd = "5", font = self.__font, command = lambda:self.__change_image(right_frame, rows_text, columns_text))
        change_button.grid(row = 1, column = 6)
    
        # Left frame
        random_button = Button(left_frame, text = "Random", bd = "5", font = self.__font, command = lambda:self.__randomize())
        random_button.grid(row = 0, column = 0, pady = 10)
        
        play_button = Button(left_frame, text = "Play", bd = "5", font = self.__font, command = lambda:self.__play(True))
        play_button.grid(row = 1, column = 0, pady = 10)
        
        algorithm_text = StringVar()
        algorithm_label = Label(left_frame, text = "Algorithms:", font = self.__font)
        algorithm_label.grid(row = 2, column = 0, pady = 2)
        algorithms_combobox = ttk.Combobox(left_frame, width = 20, font = self.__font, textvariable = algorithm_text)
        algorithms_combobox["values"] = ("Depth First Search",
                                         "Breadth First Search",
                                         "Uniform Cost Search",
                                         "Greedy Search",
                                         "A-star Search")
        algorithms_combobox.grid(row = 3, column = 0, pady = 15)
        algorithms_combobox.current(0)
    
        solve_button = Button(left_frame, text = "Solve", bd = "5", font = self.__font, command = lambda:self.__solve(algorithm_text))
        solve_button.grid(row = 4, column = 0, pady = 10)
        
        solve_button = Button(left_frame, text = "Reset", bd = "5", font = self.__font, command = lambda:self.__reset())
        solve_button.grid(row = 5, column = 0, pady = 10)
        
        exit_button = Button(left_frame, text = "Exit", bd = "5", command = self.root.destroy, font = self.__font)
        exit_button.grid(row = 6, column = 0, pady = 10)
        
        # Right frame
        puzzle = Puzzle(self.root, self.__make_pieces(right_frame))
        puzzle.draw_puzzle()
    
        # Bottom frame
        state_label = Label(bottom_frame, text = "The puzzle has created.", font = self.__font)
        state_label.grid(row = 0, column = 0)
        return puzzle, state_label
        

    def __make_pieces(self, right_frame):
        height = self.__image_size // self.__puzzle_rows
        width = self.__image_size // self.__puzzle_columns
        new_pieces = []
        index = 0
        for i in range(self.__puzzle_rows):
            pieces_in_row = []
            for j in range(self.__puzzle_columns):
                if j == self.__puzzle_columns - 1 and i == self.__puzzle_rows - 1:
                    img = Image.new("L", (width, height), 255)
                    index = 0
                else:
                    img = self.__image.crop((j * width, i * height, (j + 1) * width, (i + 1) * height))
                    index = i * self.__puzzle_columns + j + 1
                img = ImageTk.PhotoImage(img)
                piece = Label(right_frame, image = img)
                piece.image = img
                pieces_in_row.append(Piece(piece, index))
            new_pieces.append(pieces_in_row)
        return Pieces(new_pieces, self.__puzzle_rows, self.__puzzle_columns, self.__puzzle_rows - 1, self.__puzzle_columns - 1)
        

    def __open_image(self, image_path_label):
        image_path = filedialog.askopenfilename(title = "open puzz-images folder")
        img = Image.open(image_path)
        self.__image = img.resize((450, 450))
        self.__image_name = os.path.basename(image_path)
        image_path_label.config(text = self.__image_name)
        

    def __change_image(self, right_frame, rows_text, columns_text):
        self.__puzzle.remove_puzzle()
        self.__puzzle_rows = int(rows_text.get())
        self.__puzzle_columns = int(columns_text.get())
        self.__puzzle = Puzzle(self.root, self.__make_pieces(right_frame))
        self.__puzzle.draw_puzzle()
        self.__state_label.config(text = "The puzzle has changed.")


    def __randomize(self):
        self.__puzzle.randomize()
        self.__puzzle.update_puzzle()
        self.__state_label.config(text = "The puzzle has randomized.")
        

    def __up(self, event):
        self.__puzzle.curr_state.move(1)
        self.__puzzle.update_puzzle()
        if self.__puzzle.is_goal():
            self.__play(False)
        

    def __right(self, event):
        self.__puzzle.curr_state.move(2)
        self.__puzzle.update_puzzle()
        if self.__puzzle.is_goal():
            self.__play(False)
        

    def __down(self, event):
        self.__puzzle.curr_state.move(3)
        self.__puzzle.update_puzzle()
        if self.__puzzle.is_goal():
            self.__play(False)
        

    def __left(self, event):
        self.__puzzle.curr_state.move(4)
        self.__puzzle.update_puzzle()
        if self.__puzzle.is_goal():
            self.__play(False)
        

    def __play(self, isPlaying):
        self.__state_label.config(text = "")
        b1 = self.root.bind("<Up>", self.__up)
        b2 = self.root.bind("<Right>", self.__right)
        b3 = self.root.bind("<Down>", self.__down)
        b4 = self.root.bind("<Left>", self.__left)
        if not isPlaying:
            self.root.unbind("<Up>", b1)
            self.root.unbind("<Right>", b2)
            self.root.unbind("<Down>", b3)
            self.root.unbind("<Left>", b4)
            self.__puzzle.random_moves = 0
            self.__state_label.config(text = "Finished! You have reached the goal state.")
        

    def __solve(self, algorithm_text):
        self.__state_label.config(text = "")
        algorithms = Algorithms(self.__puzzle, algorithm_text)
        start = time.time()
        if algorithms.name == "Depth First Search":
            algorithms.dfs()
        if algorithms.name == "Breadth First Search":
            algorithms.bfs()
        if algorithms.name == "Uniform Cost Search":
            algorithms.ucs()
            
        if algorithms.name != "Depth First Search":
            self.__puzzle.show_solution(algorithms)
        end = time.time()
        self.__puzzle.random_moves = 0
        if algorithms.name == "Breadth First Search":
            self.__state_label.config(text = "Finished! Depth = {}, Nodes = {}, Time = {} s".format(algorithms.max_depth, algorithms.nodes, round((end - start), 2)))
        if algorithms.name == "Uniform Cost Search":
            self.__state_label.config(text = "Finished! Depth = {}, Nodes = {}, G = {}, Time = {} s".format(algorithms.max_depth, algorithms.nodes, algorithms.g, round((end - start), 2)))
        

    def __reset(self):
        self.__puzzle.reset()
        self.__puzzle.update_puzzle()
        
