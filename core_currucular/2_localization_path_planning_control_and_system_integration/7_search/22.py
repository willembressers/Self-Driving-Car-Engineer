# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):
    wall = 99
    x_max = len(grid)
    y_max = len(grid[0])

    # initialize an empty grid
    value = [[wall for col in range(y_max)] for row in range(x_max)]
    policy2D = [[' ' for col in range(y_max)] for row in range(x_max)]

    # set the goal
    value[goal[0]][goal[1]] = 0
    policy2D[goal[0]][goal[1]] = '*'

    # flag for the infinate loop
    repeat = True

    # loop until .. 
    while repeat:
        
        # by default break the infinate loop
        repeat = False

        # loop over all cells
        for x in range(x_max):
            for y in range(y_max):

                # ensure the current cell is not a wall
                if grid[x][y] == 0:
                    pass

                    # loop over all actions
                    # for action_id, action in enumerate(forward):

                    #     # get the coordinates of the adjacent cell
                    #     x_adjacent = x + action[0]
                    #     y_adjacent = y + action[1]

                    #     # check if we're still within the grid
                    #     if (x_adjacent >= 0 and x_adjacent < x_max) and (y_adjacent >= 0 and y_adjacent < y_max):

                    #         # ensure the adjacent cell is not a wall
                    #         if grid[x_adjacent][y_adjacent] == 0:

                    #             # determine the value of the adjacent cell
                    #             adjacent_value = value[x_adjacent][y_adjacent] + cost
                                
                    #             # now get the smallest value from the adjacent cells
                    #             if adjacent_value < value[x][y]:
                    #                 value[x][y] = adjacent_value
                    #                 policy2D[x][y] = delta_name[action_id]
                    #                 repeat = True

    return policy2D

print('='*80)
print('INPUT')
print('='*80)

# print it
for row in grid:
  print(row)

print('='*80)
print('POLICY')
print('='*80)

# print it
for row in optimum_policy2D(grid,init,goal,cost):
    print(row)  