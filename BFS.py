import queue
import pygame
import random
import math

pygame.init()  # initiates pygame

COLORS = {
    'grey': (177, 177, 177),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'black': (0, 0, 0),
    'yellow': (228, 222, 0),
    'light_blue': (133, 138, 229)
}

# menu actions
START = False
RESET = False
DRAW = False
REMOVE = False
STARTPOINT = False
ENDPOINT = False
CLEAR = False


def get_int(string):
    '''
        returns only the integer value of the string
        params: string
        returns: string
    '''
    return ''.join([s for s in string if s.isnumeric()])


def blit_text(surface, text, pos, font, color=COLORS['black']):
    '''
        blit a text word by word and ensures that the words are inside the surface
        params: surface, text, pos, font, color
        returns: None
    '''
    box_margin = 14     # ensures that the words are in the box
    words = text.split()  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for word in words:
        word_surface = font.render(word, 0, color)
        word_width, word_height = word_surface.get_size()
        if x + word_width > max_width - box_margin:
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        surface.blit(word_surface, (x, y))
        x += word_width + space
    x = pos[0]  # Reset the x.
    y += word_height  # Start on new row.


#   menu creator
class Menu:
    def __init__(self, x=370, y=30, height=25, width=70, menu_cells=8, order='col'):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.menu_cells = menu_cells
        self.margin = 3
        self.text_margin = 5
        self.order = order
        self.box_width = 120
        self.box_height = 100
        self.box_x = self.x
        self.box_y = (self.y + self.margin) * self.menu_cells - self.margin * 2
        self.description_box = (self.box_x, self.box_y, self.box_width, self.box_height)  # dimensions of description_box to draw

    def create_menu(self):
        '''
            creates a menu list
            params: self
            returns: list
        '''
        menu = [0 for _ in range(self.menu_cells)]
        return menu

    def draw_menu(self, surface, menu, menu_text):
        '''
            draws the menu on the surface
            params: surface, menu
            returns: None
        '''
        # ______________________________ menu action colors ________________________________________________________

        for j in range(len(menu)):
            if menu[j] == 1:
                color = COLORS['green']
            elif menu[j] == 'hover':
                color = COLORS['red']
            elif menu[j] == 'activated':
                color = COLORS['red']
            else:
                color = COLORS['white']

            # ______________________________ col based menu _______________________________________________________

            if self.order == 'col':
                pygame.draw.rect(surface, color,
                                 (self.x, self.y +
                                  (self.height + self.margin) * j, self.width, self.height))
                surface.blit(menu_text[j], (self.text_margin +
                             self.x, self.y + (self.height + self.margin)
                              * j + self.text_margin))

            # ______________________________ row based menu _______________________________________________________

            elif self.order == 'row':
                pygame.draw.rect(surface, color, (self.x + (self.width + self.margin) * j,
                                                  self.y, self.width, self.height))

                surface.blit(menu_text[j], (self.text_margin + self.x + (self.width + self.margin) * j,
                                            self.y + self.text_margin))

        # ______________________________ draw the description box ______________________________________________

        pygame.draw.rect(surface, COLORS['white'], self.description_box)

        # ______________________________ description box texts _________________________________________________

        run_description = 'click here to run the algorithm'
        stop_description = 'click here to stop the algorithm'
        reset_description = 'click here to reset the program and keep the current walls'
        draw_description = 'click here to draw walls'
        remove_description = 'click here to remove a wall, start or end points'
        start_description = 'click here to draw a starting point'
        end_description = 'click here to draw an end point'
        clear_description = 'click here to clear the grid including the walls'

        menu_description = [run_description, stop_description, reset_description, draw_description,
                            remove_description, start_description, end_description, clear_description]
        dbox_font = pygame.font.SysFont('arial', 15)

        # ______________________________ blit the descriptions in the box ______________________________________

        for j in range(len(menu)):
            if menu[j] == 'hover':
                blit_text(surface, menu_description[j], (self.box_x + self.margin, self.box_y + self.margin), dbox_font)

    def menu_mouse_action(self, event, menu):
        '''
            clicking on the menu action
            params: menu, mouse_pos
            returns: None
        '''
        pos = pygame.mouse.get_pos()
        pos_x, pos_y = pos
        if self.order == 'col':
            menu_x = (pos_x - self.x)//self.width
            menu_y = (pos_y - self.y)//(self.height + self.margin)
            if 0 <= menu_x < 1 and 0 <= menu_y < len(menu):
                for j, item in enumerate(menu):
                    if j == menu_y:
                        menu[j] = 'hover'
                    else:
                        menu[j] = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu[menu_y] = 'clicked'
                elif event.type == pygame.MOUSEBUTTONUP:
                    if menu_y == 0 or menu_y == 1:
                        menu[menu_y] = 0

        if self.order == 'row':
            menu_x = (pos_x - self.x) // (self.width + self.margin)
            menu_y = (pos_y - self.y) // self.height
            if 0 <= menu_x < len(menu) and 0 <= menu_y < 1:
                for j, item in enumerate(menu):
                    if j == menu_x:
                        menu[j] = 'hover'
                    else:
                        menu[j] = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu[menu_x] = 'clicked'
                elif event.type == pygame.MOUSEBUTTONUP:
                    if menu_x == 0 or menu_x == 1:
                        menu[menu_x] = 0


#   grids creator
class Grid:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.x = 30
        self. y = 30
        self.rows = 30
        self.cols = 30
        self.width = 10
        self.height = 10
        self.margin = 1
        self.removing = False
        self.drawing = False
        self.drag_start = False
        self.drag_end = False

    def create_grid(self):
        '''
            creates the grid matrix
            params: self
            returns: grid matrix
        '''
        grid = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        grid[self.start[1]][self.start[0]] = 'S'
        grid[self.end[1]][self.end[0]] = 'E'
        return grid

    def draw_grid(self, surface, GRID):
        '''
            draws the grid
            params : surface, color
            return : None
        '''

        global color
        for j, row in enumerate(GRID):
            for i, char in enumerate(GRID[j]):
                '''
                    coloring the matrix according to the values
                    0 : empty blocks
                    1 : visited block
                    2 : backtracked block
                    S : starting point
                    E : ending point
                    # : wall (not valid)
                    P : pointer
                    H : head of the algo 
                '''
                if GRID[j][i] == 0:
                    color = COLORS['white']
                elif GRID[j][i] == 1:
                    color = COLORS['green']
                elif GRID[j][i] == 2:
                    color = COLORS['red']
                elif GRID[j][i] == 'P':
                    color = COLORS['yellow']
                elif GRID[j][i] == 'H':
                    color = COLORS['light_blue']
                elif GRID[j][i] == 'S':
                    color = COLORS['red']
                elif GRID[j][i] == 'E':
                    color = COLORS['blue']
                elif GRID[j][i] == '#':
                    color = COLORS['black']

                pygame.draw.rect(surface, color,
                                 (self.x + (self.width + self.margin) * i,
                                  self.y + (self.height + self.margin) * j,
                                  self.width, self.height))

    def grid_actions(self, grid, event):
        '''
            grid drawing actions
            params: grid
            returns: None
        '''
        pos = pygame.mouse.get_pos()
        pos_x, pos_y = pos
        grid_x = (pos_x - self.x) // (self.width + self.margin)
        grid_y = (pos_y - self.y) // (self.height + self.margin)
        if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
            if event.type == pygame.MOUSEBUTTONDOWN:

                if DRAW:
                    self.drawing = True

                if REMOVE:
                    self.removing = True

                if STARTPOINT:
                    if not any(['S' in row for row in grid]):
                        grid[grid_y][grid_x] = 'S'

                if ENDPOINT:
                    if not any(['E' in row for row in grid]):
                        grid[grid_y][grid_x] = 'E'

                # _________________________________drag and drop end ________________________________

            if self.drag_end:
                for j, row in enumerate(grid):
                    for i, char in enumerate(row):
                        if char == 'E':
                            grid[j][i] = 0
                if not grid[grid_y][grid_x] == 'S':
                    if not grid[grid_y][grid_x] == '#':
                        grid[grid_y][grid_x] = 'E'

                # _________________________________drag and drop start ________________________________

            if self.drag_start:
                for j, row in enumerate(grid):
                    for i, char in enumerate(row):
                        if char == 'S':
                            grid[j][i] = 0
                if not grid[grid_y][grid_x] == 'E':
                    if not grid[grid_y][grid_x] == '#':
                        grid[grid_y][grid_x] = 'S'

    def get_pos(self):
        '''
            gets the mouse position in the grid
            params: self
            returns: grid_x, grid_y
        '''
        pos = pygame.mouse.get_pos()
        pos_x, pos_y = pos
        grid_x = (pos_x - self.x) // (self.width + self.margin)
        grid_y = (pos_y - self.y) // (self.height + self.margin)
        return grid_x, grid_y

    def wall_drawer(self, grid, event):
        '''
        drawing function that toggles the drawing on the surface while clicking
        params:None
        returns:None
        '''
        grid_x, grid_y = self.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            self.drawing= False
        if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
            if self.drawing:
                grid[grid_y][grid_x] = '#'

    def wall_remover(self, grid, event):
        '''
        drawing function that toggles the drawing on the surface while clicking
        params:None
        returns:None
        '''
        grid_x, grid_y = self.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            self.removing = False
        if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
            if self.removing:
                grid[grid_y][grid_x] = 0

    def cell_drag(self, grid, event):
        '''
            drag and drop the cells 'End and Start'
            params: grid, event
            returns: None
        '''

        grid_x, grid_y = self.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:

            if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
                if grid[grid_y][grid_x] == 'S':
                    self.drag_start = True
                elif grid[grid_y][grid_x] == 'E':
                    self.drag_end = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag_start = False
            self.drag_end = False

    @staticmethod
    def clean_grid(grid):
        '''
            static method
            cleans the grid and gets it ready for the next run
            params: grid
            returns: grid
        '''
        for j, row in enumerate(grid):
            for i, char in enumerate(row):
                if char in [1, 2, 'P', 'H']:
                    grid[j][i] = 0
        return grid

    @staticmethod
    def clear_grid(grid):
        '''
            static method
            clears everything in the grid, except for the start and end points
            params: grid
            returns: grid
        '''
        for j, row in enumerate(grid):
            for i, char in enumerate(row):
                if not char == 'S' and not char == 'E':
                    grid[j][i] = 0
        return grid


#   main search algorithm
class Search:
    def __init__(self, start, end, grid):
        self.start = start     # initialising the value of the start point
        self.end = end      # initialising the value of the end point
        self.frontier = queue.Queue()
        self.frontier.put(self.start)
        self.visited = []
        self.backtrack = {}
        self.GRID = grid
        self.unseen = {}
        self.unvisited = {}
        self.started = False
        self.cell = self.get_start()
        self.counter = 0
        self.start_searching = False


    def search_init(self):  # when we find the starting point we initiate
        self.start = self.get_start()
        self.end = self.get_end()
        self.visited = []
        self.backtrack = {}
        self.counter = 0
        self.cell = self.get_start()
        self.frontier.queue.clear()
        self.frontier.put(self.start)

    def get_start(self):
        '''
            find the start point in the matrix
            params: self
            returns: tuple
        '''
        start = (0, 0)
        for j, row in enumerate(self.GRID):
            if 'S' in row:
                for i, char in enumerate(row):
                    if char == 'S':
                        start = (i, j)
        return start

    def get_end(self):
        '''
           find the end point in the matrix
           params: self
           returns: tuple
       '''
        end = (0, 0)
        for j, row in enumerate(self.GRID):
            if 'E' in row:
                for i, char in enumerate(row):
                    if char == 'E':
                        end = (i, j)
        return end

    def get_cell(self, move, cell):
        '''
            searches for the cell in the matrix
            params: tuple
            returns: tuple
            L: left
            R: right
            D: down
            U: up
        '''
        i, j = cell
        for letter in move:
            if letter == 'L':
                i -= 1
            elif letter == 'R':
                i += 1
            elif letter == 'D':
                j += 1
            elif letter == 'U':
                j -= 1

        result_cell = (i, j)
        return result_cell

    def valid_move(self, cell, char='#'):
        '''
            checks if the cell is valid (not out of index, not a wall, and not in visited list)
            params: tuple cell
            returns: boolean
        '''

        if cell in self.visited or cell in self.frontier.queue:  # excluding visited cells gave 10 x more performance
            return False
        if 0 <= cell[1] < len(self.GRID) and 0 <= cell[0] < len(self.GRID[cell[1]]):
            if not self.GRID[cell[1]][cell[0]] == char:
                return True
        return False


    # def maze_valid_move(self, cell):
    #     '''
    #         checks if the cell is valid (not out of index, not a wall, and not in visited list)
    #         params: tuple cell
    #         returns: boolean
    #     '''
    #     if cell in self.maze:
    #         return False
    #     if 0 <= cell[1] < len(self.GRID) and 0 <= cell[0] < len(self.GRID[cell[1]]):
    #         if not self.GRID[cell[1]][cell[0]] == 0:
    #             return True
    #     return False

    def is_start(self):
        '''
            finds if there is a start in the grid
            paras: self
            returns: None
        '''
        if any(['S' in row for row in self.GRID]):
            return True
        else:
            return False

    def is_end(self):
        '''
            finds if there is an end in the grid
            paras: self
            returns: None
        '''
        if any(['E' in row for row in self.GRID]):
            return True
        else:
            return False

    def found_path(self):
        '''
            checks if the cell is the end of the path
            params: tuple cell
            returns: boolean
        '''
        end = self.get_end()
        if end in self.visited:
                    return True
        return False

    def bck_path(self):     # TODO: realtime backtrack
        '''
            finds the most effiecient backtrack pathfor move in ['L', 'U', 'R', 'D']:
                    if self.valid_move(self.get_cell(move)):
            params: self
            returns: list of tuples (path) from end to start
        '''
        start = self.get_start()
        end = self.get_end()
        path = [end]
        while True:
            end = self.backtrack[end]
            path.append(end)
            if end == start:
                return path

    def search(self):
        '''
            main search algorithm 'breadth first algorithm'
            params: self
            returns nothing
        '''
        # find and animate the search algorithm
        if not self.found_path() and not self.frontier.empty():
            self.cell = self.frontier.get()             # get cell from queue
            self.visited.append(self.cell)              # add the cell to the visited

            if self.GRID[self.cell[1]][self.cell[0]] == 0:
                self.GRID[self.cell[1]][self.cell[0]] = 1

            # ________________________________ queue appending __________________________________

            for move in ['L', 'U', 'R', 'D']:
                put = self.get_cell(move, self.cell)               # moves to append to queue
                if self.valid_move(put):                # validate
                    self.frontier.put(put)              # add validated moves to queue
                    self.backtrack[put] = self.cell     # add to backtrack
            self.counter = 0                            # counter for animation purposes

        elif self.found_path():

            # ________________________________ backtracking ___________________________________

            # draw the backtrack path (animated)
            path = self.bck_path()                      # get the path from bck

            if 0 <= self.counter < len(path):           # animation stuff
                pos = path[self.counter]                # extra animation stuff

                if self.GRID[pos[1]][pos[0]] == 1:      # coloring
                    self.GRID[pos[1]][pos[0]] = 2
                self.counter += 1

        elif self.frontier.empty() and not self.found_path():   # no path to find
            # TODO: blit path cannot be found
            print('path cannot be found')

    def init_dijkstra(self):
        '''
            initiates dijkstras search algorithm
            param: None
            returns: None

        '''
        # reset the values
        self.start = self.get_start()
        self.end = self.get_end()
        self.visited = []
        self.backtrack = {}
        self.counter = 0

        # rreset the weights and the start/end
        for j, row in enumerate(self.GRID):
            for i, _ in enumerate(row):
                self.unseen[(i, j)] = {move: 1 for move in ['L', 'U', 'R', 'D'] if self.valid_move(self.get_cell(move, (i, j)))}

        for node in self.unseen:
            if node == self.start:
                self.unvisited[node] = 0
            else:
                self.unvisited[node] = math.inf


    def dijkstra(self): #TODO: organize
        ''' 
            main dijkstras algorithm, default weights are 1
            params: None
            returns: None
        '''
        if not self.found_path():
            min_node = (None, math.inf)
            for node in self.unvisited: # get the node with the min value 
                if node not in self.visited:
                    if self.unvisited[node] < min_node[1]:
                        min_node = (node, self.unvisited[node])
                        # we can change the color here
            
            if min_node[0] == None: # no path
                print('path cannot be found')
                #TODO: blit path cannot be found
            else:

                for child, weight in self.unseen[min_node[0]].items():
                    child_node = self.get_cell(child, min_node[0])
                    if self.unvisited[child_node] > min_node[1] + weight:
                        self.unvisited[child_node] = min_node[1] + weight
                        self.backtrack[child_node] = min_node[0]
                        
                        if self.GRID[child_node[1]][child_node[0]] in [0, 'H']: # animation for the head of the algorithm
                            self.GRID[child_node[1]][child_node[0]] = 'P'

                self.visited.append(min_node[0])
                node = min_node[0]
                if self.GRID[node[1]][node[0]] in [0, 'H', 'P']:
                    self.GRID[node[1]][node[0]] = 1
                self.unseen.pop(min_node[0])
            
        elif self.found_path:
            path = self.bck_path()                      # get the path from bck

            if 0 <= self.counter < len(path):           # animation stuff
                pos = path[self.counter]                # extra animation stuff

                if self.GRID[pos[1]][pos[0]] == 1:      # coloring
                    self.GRID[pos[1]][pos[0]] = 2
                self.counter += 1


            

    def maze_generator(self, run):  # counter will do a 2 step count

        '''
            generate a maze matrix
            params: animation counter
            returns: None
        '''
        # we need to pass 2 counters to the main loop, one for the rows and one for the and one for the maximum number
        # of wall tiles in the map
        if run.wall_count <= run.max_walls:
            cell = random.randint(0, len(self.GRID[0]) - 1)  # 0 for the first row but we can change it -1 for index

            if run.row_counter < len(self.GRID):
                # change the value of the grid if not start or end
                if not self.GRID[run.row_counter][cell] == 'S' and not self.GRID[run.row_counter][cell] == 'E':
                    grid_cell = (cell, run.row_counter)
                    if grid_cell not in run.walls:
                        run.walls.append(grid_cell)     # to make
                        run.wall_count += 1             # sure we are counting all the walls because we are using random
                    self.GRID[run.row_counter][cell] = '#'
                run.row_counter += 1
            else:
                run.row_counter = 0                     # grid counter
        else:
            run.generate = False                        # when done


#   Core function
class Core:
    def __init__(self):
        # frames
        self.time = pygame.time.Clock()
        self.fps = 60

# __________________________________________window section__________________________________________________

        self.win_w = 500
        self.win_h = 500
        self.window = pygame.display.set_mode((self.win_w, self.win_h))

# __________________________________________Menus section___________________________________________________

        self.RightMenu = Menu()
        self.right_menu = self.RightMenu.create_menu()
        self.LowerMenu = Menu(30, 370, 25, 100, 3, order='row')
        self.lower_menu = self.LowerMenu.create_menu()

        # ____________________right menu cells ________________________

        self.font = pygame.font.Font('freesansbold.ttf', 15)
        self.menu_run = self.font.render('Run', True, COLORS['black'])
        self.menu_reset = self.font.render('Reset', True, COLORS['black'])
        self.menu_draw = self.font.render('Draw', True, COLORS['black'])
        self.menu_remove = self.font.render('Remove', True, COLORS['black'])
        self.menu_start = self.font.render('Start', True, COLORS['black'])
        self.menu_end = self.font.render('End', True, COLORS['black'])
        self.menu_stop = self.font.render('Stop', True, COLORS['black'])
        self.menu_clear = self.font.render('Clear', True, COLORS['black'])
        self.menu_text = [self.menu_run, self.menu_stop, self.menu_reset, self.menu_draw,
                          self.menu_remove, self.menu_start, self.menu_end, self.menu_clear]

        # ____________________lower menu cells ________________________

        self.menu_generate = self.font.render('Generate', True, COLORS['black'])
        # self.menu_reset = self.font.render('Reset', True, COLORS['black'])
        # self.menu_draw = self.font.render('Draw', True, COLORS['black'])
        # self.menu_remove = self.font.render('Remove', True, COLORS['black'])
        self.lower_menu_text = [self.menu_generate, self.menu_stop, self.menu_reset, self.menu_draw]

        # ____________________lower menu actions ______________________

        self.generate = False

# __________________________________________MISC section___________________________________________________

        self.Grid = Grid((0, 0), (7, 7))
        self.grid = self.Grid.create_grid()
        self.search = Search((0, 0), (7, 7), self.grid)
        self.text = '0'
        self.max_walls = 250
        self.walls = []
        self.wall_count = 0
        self.row_counter = 0
        self.active_box = False
        self.text_margin_x, self.text_margin_y = 6, 1
        self.start_dijkstra = False



    def generation_init(self):
        self.walls = []
        self.wall_count = 0
        self.row_counter = 0

    def input_box(self, event, pos, width, height):
        '''
            draws an input box that can take a value from the user
            paras: event, pos, width, height
            returns: None
        '''
        m_pos = pygame.mouse.get_pos()
        box = pygame.Rect(*pos, width, height)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if box.collidepoint(*m_pos):                # collision check
                self.active_box = not self.active_box
                if self.active_box:
                    self.text = ''                      # start with nothing when its activated

            else:
                self.active_box = False

        if self.active_box:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:        # return deactivates the box
                    self.active_box = False

                if event.key == pygame.K_BACKSPACE:     # backspace action
                    self.text = self.text[:-1]

                self.text += get_int(event.unicode)

                if not self.text == '':                 # make sure that an int is passed
                    self.max_walls = int(self.text)
                else:
                    self.max_walls = 0                  # start with 0 if you pass in nothing
                    self.text = ''

                max_possible_walls = len(self.grid) * len(self.grid[0])
                if int(self.max_walls) > max_possible_walls:      # max walls is the number of cells in the grid
                    self.text = str(max_possible_walls)     # TODO: blit a warning for max number
                    self.max_walls = int(self.text)

        else:
            self.text = str(self.max_walls)             # display the number of max walls

    def draw_input_box(self, pos, width, height):
        '''
            draws the input box, updates the self.text value
            params: tuple, width, height
            returns: None
        '''
        box = pygame.Rect(*pos, width, height)
        pygame.draw.rect(self.window, COLORS['white'], box)
        font = pygame.font.SysFont('Arial', 15)
        text_surface = font.render(self.text, True, COLORS['black'])
        self.window.blit(text_surface, (pos[0] + self.text_margin_x, pos[1] + self.text_margin_y))

    def right_menu_click(self):

        '''
            right menu action, it does all the functions for the right menu when clicked
            params: None
            returns: None
            _____________________________________________________________________________
            menu actions:
            0: start
            1: stop
            2: reset: cleans the map and keeps the walls
            3: draw
            4: remove
            5: draw the start point
            6: draw the end point
            7: clear: clears the whole map including walls
        '''

        global START, RESET, DRAW, REMOVE, STARTPOINT, ENDPOINT, CLEAR     # TODO: fix global variables, and
        if self.right_menu[0] == 'clicked':                                         # and comment out sections
            START = True
            start = self.search.get_start()
            end = self.search.get_end()
            self.search.__init__(start, end, run.grid)
            self.grid = self.Grid.clean_grid(self.grid)
            RESET = False
            self.right_menu[0] = 1
        if self.right_menu[1] == 'clicked':
            START = False
            self.start_dijkstra = False
            self.right_menu[1] = 1
        if self.right_menu[2] == 'clicked':
            START = False
            RESET = True
            self.start_dijkstra = False
            self.right_menu[2] = 1
        else:
            RESET = False
        if self.right_menu[3] == 'clicked':
            DRAW = True
            REMOVE = False
            STARTPOINT = False
            ENDPOINT = False
            self.right_menu[3] = 1
        if self.right_menu[4] == 'clicked':
            DRAW = False
            REMOVE = True
            STARTPOINT = False
            ENDPOINT = False
            self.right_menu[4] = 1
        if self.right_menu[5] == 'clicked':
            STARTPOINT = True
            DRAW = False
            REMOVE = False
            ENDPOINT = False
            self.right_menu[5] = 1
        if self.right_menu[6] == 'clicked':
            DRAW = False
            REMOVE = False
            STARTPOINT = False
            ENDPOINT = True
            self.right_menu[6] = 1
        if self.right_menu[7] == 'clicked':
            CLEAR = True
            START = False
            RESET = False
            DRAW = False
            REMOVE = False
            STARTPOINT = False
            ENDPOINT = False
            self.right_menu[7] = 1
        else:
            CLEAR = False

    def lower_menu_click(self):
        '''
            lower menu actions
            params: self
            returns: None
        '''
        if self.lower_menu[0] == 'clicked':
            self.generation_init()
            self.grid = self.Grid.clear_grid(self.grid)
            self.generate = True
            self.lower_menu[0] = 1
        if self.lower_menu[1] == 'clicked':
            self.grid = self.Grid.clean_grid(self.grid)
            self.search.init_dijkstra()
            self.start_dijkstra = True
            self.lower_menu[1] = 1

    def redraw(self):
        '''
            redraws the frames
            params: search, grid
            returns: None
        '''
        self.window.fill(COLORS['grey'])
        self.RightMenu.draw_menu(self.window, self.right_menu, self.menu_text)
        self.LowerMenu.draw_menu(self.window, self.lower_menu, self.lower_menu_text)
        self.Grid.draw_grid(self.window, self.grid)
        # font = pygame.font.Font('freesansbold.ttf', 20)     # delete
        # copy_right = font.render('by Omar Salameh', True, COLORS['white'])  # delete
        # self.window.blit(copy_right, (150, 400)) #delete
        self.draw_input_box((30, 400), 40, 20)
        pygame.display.flip()

    def live_update_init(self):
        '''
            init for the live update effect
            params: self
            returns: None
        '''
        self.grid = self.Grid.clean_grid(self.grid)
        start = self.search.get_start()
        end = self.search.get_end()
        self.search.__init__(start, end, self.grid)
        self.search.init_dijkstra()

    def run(self):    # main loop and actions
        '''
            main loop
            params: search, grid
            returns: None
        '''
        global START
        run = True
        self.time.tick(self.fps)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # ___________________________ Menu run stuff ____________________________

                self.RightMenu.menu_mouse_action(event, self.right_menu)
                self.LowerMenu.menu_mouse_action(event, self.lower_menu)
                self.right_menu_click()
                self.lower_menu_click()

            # ___________________________ input box stuff ____________________________

                self.input_box(event, (30, 400), 40, 20)

            # ___________________________ Grid run stuff ____________________________

                self.Grid.cell_drag(self.grid, event)
                self.Grid.grid_actions(self.grid, event)

    # _____________________________________DRAW and REMOVE ________________________________________________

                if self.Grid.drawing:
                    self.Grid.wall_drawer(self.grid, event)

                if self.Grid.removing:
                    self.Grid.wall_remover(self.grid, event)

    # _____________________________________STAR RESET and CLEAR __________________________________________

            if START:
                if self.Grid.drawing or self.Grid.removing:
                    self.live_update_init()     # initiate the grid

                # give a live update when dragging the cells
                    while not self.search.found_path() and not self.search.frontier.empty():
                        self.search.search()
                        # updating = True
            # ________________________________drag and drop live effect ______________________________

                if self.search.is_start() and self.search.is_end():
                    if self.Grid.drag_start or self.Grid.drag_end:
                        self.live_update_init()  # initiate the grid

                        # give a live update when dragging the cells
                        while not self.search.found_path() and not self.search.frontier.empty():
                            self.search.search()

                    self.search.search()
                else:
                    START = False

            if RESET:
                self.grid = self.Grid.clean_grid(self.grid)
                start = self.search.get_start()
                end = self.search.get_end()
                self.search.__init__(start, end, self.grid)

            if CLEAR:
                self.grid = self.Grid.clear_grid(self.grid)
                start = self.search.get_start()
                end = self.search.get_end()
                self.search.__init__(start, end, self.grid)
                self.__init__()
    # ______________________________________maze generator_______________________________________________

            if self.generate:
                self.search.maze_generator(self)

    # ______________________________________redraw the frames ___________________________________________
            if self.start_dijkstra:
                START = False

                if self.Grid.drawing or self.Grid.removing:
                    self.live_update_init()     # initiate the grid

                # give a live update when dragging the cells
                    while not self.search.found_path():
                        self.search.dijkstra()
                        # updating = True

    # ________________________________drag and drop live effect ______________________________

                if self.search.is_start() and self.search.is_end():
                    if self.Grid.drag_start or self.Grid.drag_end:
                        self.live_update_init()  # initiate the grid

                        # give a live update when dragging the cells
                        while not self.search.found_path():
                            self.search.dijkstra()

                    self.search.dijkstra()
                else:
                    self.start_dijkstra = False
            
            self.redraw()


if __name__ == "__main__":
    run = Core()
    run.run()
