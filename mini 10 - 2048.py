"""
Clone of 2048 game.
"""

#import poc_2048_gui
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
    new_array = [0] * len(line)
    final_array = [0] * len(line)
    array_indice = 0
    
    # this <for> shifts numbers to the left
    for dummy_item in line:
        if dummy_item != 0:
            new_array[array_indice] = dummy_item
            array_indice += 1
    
    # following <for> combines all number pairs, once each
    array_indice = 0
    for dummy_item in new_array:        
        if array_indice + 1 >= len(new_array):
            next_item = 0
        else:
            next_item = new_array[array_indice + 1]
        
        # this conditional adds the pairs and assigns them to list positions
        if dummy_item != 0:           
            if dummy_item == next_item:
                total = dummy_item + next_item
                final_array[array_indice] = total
                array_indice += 1
                new_array.remove(next_item)
                new_array.append(0)
            else:   
                # have to increment array_indice because if there's no addition
                # index position becomes occupied by unpaired number
                final_array[array_indice] = dummy_item
                array_indice += 1
    return final_array

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid_change = False
        self.reset()
        
        self._start_tiles = {UP: [], 
                           DOWN: [], 
                           LEFT: [],
                           RIGHT: []}
        
        self._start_tiles[UP] = list((0,col) for col in range(self.get_grid_width()))
        self._start_tiles[DOWN] = list((self.get_grid_height()-1,col) for col in range(self.get_grid_width()))
        self._start_tiles[LEFT] = list((row,0) for row in range(self.get_grid_height()))
        self._start_tiles[RIGHT] = list((row,self.get_grid_width()-1) for row in range(self.get_grid_height()))

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._game_grid = []
        for dummy_row in range(self.get_grid_height()):
            dummy_list = []
            for dummy_col in range(self.get_grid_width()):
                dummy_list.append(0)
            self._game_grid.append(dummy_list)
        
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        placeholder = ""
        for dummy_row in self._game_grid:
            placeholder += str(dummy_row) + "\n"
        return placeholder

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        given_tiles = self._start_tiles[direction]
        tiles_movement = OFFSETS[direction]
        
        for start_cell in given_tiles:
            temp_col_row = []
            temp_value_list = []
			merged_values = []
            dummy_indice = 0
            
			#compute rows for UP/DOWN direction based on start_cell and tiles_movement
            if direction == 1 or direction == 2:
                for step in range(self.get_grid_height()):
                    row = start_cell[0] + step * tiles_movement[0]
                    col = start_cell[1] + step * tiles_movement[1]
                    temp_col_row.append((row, col))
                    temp_value_list.append(self._game_grid[row][col])
            
			#compute cols for LEFT/RIGHT direction based on start_cell and tiles_movement			
            elif direction == 3 or direction == 4:
                for step in range(self.get_grid_width()):
                    row = start_cell[0] + step * tiles_movement[0]
                    col = start_cell[1] + step * tiles_movement[1]
                    temp_col_row.append((row, col))
                    temp_value_list.append(self._game_grid[row][col])
            
			#merge row or col values
            merged_values = merge(temp_value_list)

			#return cell values to row or col
            for mod_cell in temp_col_row:
                self._game_grid[mod_cell[0]][mod_cell[1]] = merged_values[dummy_indice]
                dummy_indice += 1
            
            if merged_values != temp_value_list:
                self._grid_change = True
        
		#introduce a new tile if change ocurred
        if self._grid_change == True:
            self.new_tile()
            self._grid_change = False

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        _start_tile_value_list = [2] * 9 + [4]
        random_tile_value = random.choice(_start_tile_value_list)
        
        random_row = random.choice(range(self.get_grid_height()))
        random_col = random.choice(range(self.get_grid_width()))
            
        if self.get_tile(random_row, random_col) == 0:
            self.set_tile(random_row, random_col, random_tile_value)
        else:
            self.new_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._game_grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._game_grid[row][col]


#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

"""
Test
"""
obj = TwentyFortyEight(4,4)
poc_2048_gui.run_gui(obj) #uncomment the import poc_2048 line at the beginning
print obj
obj.set_tile(0, 0, 2)
obj.set_tile(0, 1, 0) 
obj.set_tile(0, 2, 0) 
obj.set_tile(0, 3, 0) 
obj.set_tile(1, 0, 0) 
obj.set_tile(1, 1, 2) 
obj.set_tile(1, 2, 0) 
obj.set_tile(1, 3, 0) 
obj.set_tile(2, 0, 0) 
obj.set_tile(2, 1, 0) 
obj.set_tile(2, 2, 2) 
obj.set_tile(2, 3, 0) 
obj.set_tile(3, 0, 0) 
obj.set_tile(3, 1, 0) 
obj.set_tile(3, 2, 0) 
obj.set_tile(3, 3, 2) 