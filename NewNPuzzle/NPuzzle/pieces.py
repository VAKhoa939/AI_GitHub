from tkinter import *
import random

class Coordinates:
    def __init__(self, row, column):
        self.row = row
        self.column = column

class Piece:
    def __init__(self, image, index):
        self.image = image
        self.index = index

class Pieces:
    def __init__(self, pieces, rows, columns, blank_row, blank_col):
        self.pieces = pieces
        self.rows = rows
        self.columns = columns
        self.blank_row = blank_row
        self.blank_col = blank_col
        self.g = 0


    def copy_pieces(self):
        new_pieces = []
        for i in range(self.rows):
            pieces_in_row = []
            for j in range(self.columns):
                 pieces_in_row.append(self.pieces[i][j])
            new_pieces.append(pieces_in_row)
        return Pieces(new_pieces, self.rows, self.columns, self.blank_row, self.blank_col)
    

    def compare_pieces(self, other):
        corrects = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.pieces[i][j].index == other.pieces[i][j].index:
                    corrects += 1
        if corrects == self.rows * self.columns:
            return True
        return False
    

    def get_neighbors(self):
        neighbors = []
        avail_moves = self.find_avail_moves()
        for move in avail_moves:
            curr_pieces = self.copy_pieces()
            curr_pieces.move(move)
            curr_pieces.g = self.g + 1
            neighbors.append(curr_pieces.copy_pieces())
        return neighbors


    def find_avail_moves(self):
        avail_moves = []
        if self.blank_row < 2:
            avail_moves.append(1)
        if self.blank_col > 0:
            avail_moves.append(2)
        if self.blank_row > 0:
            avail_moves.append(3)
        if self.blank_col < 2:
            avail_moves.append(4)
        return avail_moves
        

    def move_backward(self, move):
        if move > 2:
            backward_key = move - 2
        else:
            backward_key = move + 2
        self.move(backward_key)
        

    def move(self, key):
        if key == 1:
            self.__up()
        elif key == 2:
            self.__right()
        elif key == 3:
            self.__down()
        elif key == 4:
            self.__left()
        else:
            pass


    def __swap(self, a, b):
        self.pieces[a.row][a.column], self.pieces[b.row][b.column] = self.pieces[b.row][b.column], self.pieces[a.row][a.column]
        

    def __left(self):
        if (self.blank_col + 1) < self.columns:
            self.__swap(Coordinates(self.blank_row, self.blank_col), Coordinates(self.blank_row, self.blank_col + 1))
            self.blank_col += 1
        

    def __right(self):
        if (self.blank_col - 1) >= 0:
            self.__swap(Coordinates(self.blank_row, self.blank_col), Coordinates(self.blank_row, self.blank_col - 1))
            self.blank_col -= 1
        

    def __up(self):
        if (self.blank_row + 1) < self.rows:
            self.__swap(Coordinates(self.blank_row, self.blank_col), Coordinates(self.blank_row + 1, self.blank_col))
            self.blank_row += 1
        

    def __down(self):
        if (self.blank_row - 1) >= 0:
            self.__swap(Coordinates(self.blank_row, self.blank_col), Coordinates(self.blank_row - 1, self.blank_col))
            self.blank_row -= 1
