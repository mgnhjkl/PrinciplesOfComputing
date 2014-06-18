"""
Clone of 2048 game.
"""

import poc_2048_gui  
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    newline = []
    num_of_nonezero = 0;
    for index in range(len(line)):
        if line[index] != 0:
            newline.append(line[index])
            num_of_nonezero += 1
    while len(newline) != len(line):
        newline.append(0)
    for index in range(num_of_nonezero - 1):
        if newline[index] == newline[index+1]:
            newline[index] = 2 * newline[index]
            newline[index+1] = 0
    newline = push_left(newline)
    return newline

def push_left(line):
    """
    push the none zero tiles to left in the list
    """
    newline = []
    for index in range(len(line)):
        if line[index] != 0:
            newline.append(line[index])
    while len(newline) != len(line):
        newline.append(0)
    return newline

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    grid_width = 0
    grid_height = 0
    grid = []
    init_tile_indices = {}
    
    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.reset()
        self.init_tile_indices[UP] = [(0, col) for col in range(self.grid_width) ]
        self.init_tile_indices[DOWN] = [(self.grid_height - 1, col) for col in range(self.grid_width)]
        self.init_tile_indices[LEFT] = [(row, 0) for row in range(self.grid_height)]
        self.init_tile_indices[RIGHT] = [(row, self.grid_width - 1) for row in range(self.grid_height)]
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = [[0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]  
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_output = ""
        for row in range(self.grid_height):  
            for col in range(self.grid_width):  
                grid_output += str(self.grid[row][col]) + " "
            grid_output += "\n"
        return grid_output

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        row = 0
        col = 0
        lenth = 0
        if direction <= 2:
            lenth = self.grid_height
        else:
            lenth = self.grid_width
        for init_tile_indice in self.init_tile_indices.get(direction):
            tmp_list = []
            row = init_tile_indice[0]
            col = init_tile_indice[1]
            # step 1
            for dummy_index in range(lenth):
                tmp_list.append(self.get_tile(row, col))
                row += OFFSETS.get(direction)[0]
                col += OFFSETS.get(direction)[1]
            # step 2
            tmp_list = merge(tmp_list)
            # step 3
            row = init_tile_indice[0]
            col = init_tile_indice[1]
            for index in range(lenth):
                self.set_tile(row, col, tmp_list[index])
                row += OFFSETS.get(direction)[0]
                col += OFFSETS.get(direction)[1]
        self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zero_list = []
        row = 0
        col = 0
        new_num = 0
        lenth = self.grid_height
        for init_tile_indice in self.init_tile_indices.get(UP):
            row = init_tile_indice[0]
            col = init_tile_indice[1]
            for dummy_index in range(lenth):
                if self.get_tile(row, col) == 0:
                    zero_list.append((row, col))
                row += OFFSETS.get(UP)[0]
                col += OFFSETS.get(UP)[1]
        if (len(zero_list) != 0):
            new_num = random.randint(0, len(zero_list) - 1)
            if random.random() < 0.1:
                self.set_tile(zero_list[new_num][0], zero_list[new_num][1], 4)
            else:
                self.set_tile(zero_list[new_num][0], zero_list[new_num][1], 2)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))