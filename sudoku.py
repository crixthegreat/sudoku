#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2020/2/25 12:54:42

import random
import copy
from const import const

class Sudoku():


    def __init__(self, block_width=3, block_height=3):

        # generate a sudoku with blocks whose width is block_width, height block_height
        # every block have (width X height) numbers

        self.max_number = block_width * block_height
        self.width = self.height = self.max_number

        self.block_width = block_width
        self.block_height = block_height
        
        self.matrix = []
        self.fixed_pos = []
        
        self.initial_matrix()


    def initial_matrix(self):
        '''initialise the matrix
        1. generate a standard sudoku matrix
        2. randomize the rows and columns (in a single block)
        3. hidden 1/3 numbers to be solve
        '''

        # e.g. [1, 2, 3, 4, 5, 6, 7, 8, 9]
        _ = [number+1 for number in range(self.max_number)]
        
        # generate standard sudoku
        for block_no in range(self.max_number):
            start_number = block_no//self.block_height + 1 + (block_no % self.block_height) * self.block_width
            # rotate the number list from start number
            block = _[start_number - 1:] + _[:start_number - 1]
            self.matrix.append(block)

        # now randomize the sudoku
        # It remains a valid sudoku when swaping the rows or columns in a single block

        # swap the rows
        row_no = []
        for block in range(self.block_width):
            no_in_block = []
            for no in range(self.block_height):
                no_in_block.append(no + self.block_height * block)
            random.shuffle(no_in_block)
            row_no.append(no_in_block)
        
        random.shuffle(row_no)
        row_no = [_ for __ in row_no for _ in __]

        # swap the column
        column_no = []
        for block in range(self.block_height):
            no_in_block = []
            for no in range(self.block_width):
                no_in_block.append(no + self.block_width * block)
            random.shuffle(no_in_block)
            column_no.append(no_in_block)
        
        random.shuffle(column_no)
        column_no = [_ for __ in column_no for _ in __]

        # swap the blocks in rows
        block_row = [_ for _ in range(self.block_width)]
        random.shuffle(block_row)

        _row_no = row_no[:]
        row_no = []
        for block_no in block_row:
            for _no in range(self.block_height):
                row_no.append(_row_no[block_no * self.block_height + _no])

        # swap the blocks in columns
        block_column = [_ for _ in range(self.block_height)]
        random.shuffle(block_column)

        _column_no = column_no[:]
        column_no = []
        for block_no in block_column:
            for _no in range(self.block_width):
                column_no.append(_column_no[block_no * self.block_width + _no]) 

        # now get the number from the original matrix to 
        # set the value for the randomized matrix
        
        original_row = 0
        _matrix = copy.deepcopy(self.matrix)
        for row in row_no:
            original_column = 0
            for column in column_no:
                block_no, index = self.get_block_pos((row, column))
                self.matrix[block_no][index] = self.get_number(_matrix, (original_row, original_column))
                original_column += 1
            original_row += 1


        # now hidden some numbers

        hidden_number_count = random.randrange(int(self.max_number ** 2 / 4), int(self.max_number ** 2 * 3 / 4))
        number_pos = [(row, column) for row in range(self.max_number) for column in range(self.max_number)]
        random.shuffle(number_pos)
        hidden_number_pos = number_pos[:hidden_number_count]
        self.fixed_pos = number_pos[hidden_number_count:]

        for pos in hidden_number_pos:
            self.set_number(pos, None)


    def get_number(self, matrix, pos):

        '''get the number from a matrix in position: pos
        '''
        
        block_no, index = self.get_block_pos(pos)
        return matrix[block_no][index]


    def get_matrix_pos(self, block_no, index):
        '''Return the pos of the matrix from the block_no and the index
        '''

        row = block_no//self.block_height * self.block_height + index // self.block_width
        column = block_no % self.block_height * self.block_width + index % self.block_width
        
        #wip       
        return (row, column)


    def get_block_pos(self, pos):
    
        row, column = pos

        block_no = row // self.block_height * self.block_height  + column // self.block_width
        index = row % self.block_height * self.block_width + column % self.block_width

        return block_no, index
    

    def set_number(self, pos, number):

        '''set the value of the position: pos of the matrix of sudoku
        '''
        
        if number and (number<1 or number>self.max_number):
            raise Exception('wrong number {} in {}'.format(number, pos))

        if pos in self.fixed_pos:
            return None
        
        block_no, index = self.get_block_pos(pos)
        self.matrix[block_no][index] = number


    def judge_win(self):

        '''judge solved or not
        '''

        for block in self.matrix:
            if len(set(filter(None, block))) != self.max_number:
                return  False

        return True

