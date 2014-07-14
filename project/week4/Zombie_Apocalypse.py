"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
#import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []

    def __str__(self):
        string = ""
        string += str(poc_grid.Grid)
        string += "Humans: " + str(self._human_list)
        string +="Zombies: "+ str(self._zombie_list)
        return string
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = [[0 for dummy_col in range(self._grid_width)] 
                    for dummy_row in range(self._grid_height)]
        infi = self._grid_height * self._grid_width
        distance_field = [[infi for dummy_col in range(self._grid_width)]
                            for dummy_row in range(self._grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            entity_list = self._human_list
        elif entity_type == ZOMBIE:
            entity_list = self._zombie_list

        for entity in entity_list:
            boundary.enqueue(entity)
            visited[entity[0]][entity[1]] = FULL
            distance_field[entity[0]][entity[1]] = 0

        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            for neighbor_cell in self.four_neighbors(current_cell[0], current_cell[1]):
                if visited[neighbor_cell[0]][neighbor_cell[1]] == EMPTY and self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    visited[neighbor_cell[0]][neighbor_cell[1]] = FULL
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = min(distance_field[neighbor_cell[0]][neighbor_cell[1]], distance_field[current_cell[0]][current_cell[1]] + 1)
                    boundary.enqueue(neighbor_cell)
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        tmp_humans = []
        for human in self.humans():
            moves = self.eight_neighbors(human[0], human[1])
            moves.append((human[0], human[1]))
            max_move = max_distance_move(moves, zombie_distance)
            tmp_humans.append(max_move)
        self._human_list = tmp_humans
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        tmp_zombies = []
        for zombie in self.zombies():
            moves = self.four_neighbors(zombie[0], zombie[1])
            moves.append((zombie[0], zombie[1]))
            min_move = min_distance_move(moves, human_distance)
            tmp_zombies.append(min_move)
        self._zombie_list = tmp_zombies
        
def max_distance_move(moves, distance):
    """
    Find max_distance_move
    """
    dist = distance[moves[0][0]][moves[0][1]]
    max_move = moves[0]
    for move in moves:
        if distance[move[0]][move[1]] > dist:
            dist = distance[move[0]][move[1]]
            max_move = move
    return max_move
def min_distance_move(moves, distance):
    """
    Find min_distance_move
    """
    dist = distance[moves[0][0]][moves[0][1]]
    min_move = moves[0]
    for move in moves:
        if distance[move[0]][move[1]] < dist:
            dist = distance[move[0]][move[1]]
            min_move = move
    return min_move

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))
