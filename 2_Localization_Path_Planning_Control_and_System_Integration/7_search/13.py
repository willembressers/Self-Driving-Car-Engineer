# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. Note that the 'v' should be 
# lowercase. '*' should mark the goal cell.
#
# You may assume that all test cases for this function
# will have a path from init to goal.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):
    g = 0
    x = init[0]
    y = init[1]
    counter = 0
    
    # copy the array
    closed = [[0 for value in row] for row in grid]
    expand = [[-1 for value in row] for row in grid]
    actions = [[-1 for value in row] for row in grid]
    policy = [[' ' for value in row] for row in grid]
    
    # flag the first cell
    closed[x][y] = 1
    opened = [[g, x, y]]

    # define some break conditions
    finshed = False
    resign = False
    
    # now loop indefenitly
    while finshed is False and resign is False:
    
        # check if the opened array is empty
        if len(opened) == 0:
            resign = True
            print("Couldn't make it")
        
        else:
            # get the element with the smallest g value
            opened.sort()
            opened.reverse()
            current = opened.pop()
            g = current[0]
            x = current[1]
            y = current[2]
            
            # keep track on where we are
            expand[x][y] = counter
            counter += 1
            
            # are we there yet
            if x == goal[0] and y == goal[1]:
                finshed = True
                path = current
                print("FOUND IT")
            
            # we didn't found the goal so lets keep looking
            else:
                
                # loop over the actions
                for i, action in enumerate(delta):
                    new_x = x + action[0]
                    new_y = y + action[1]
                    
                    # check if we're still within the grid
                    if (new_x >= 0 and new_x < len(grid)) and (new_y >= 0 and new_y < len(grid[0])):
                        
                        # check if new element is already closed
                        if closed[new_x][new_y] == 0:
                        
                            # check if new element is not blocked
                            if grid[new_x][new_y] == 0:
                                
                                # determine the new g value
                                new_g = g + cost
                                
                                # append it to the list for the next round
                                opened.append([new_g, new_x, new_y])
                                
                                # flag the current element as closed
                                closed[new_x][new_y] = 1
                                
                                # keep track on the action we take
                                actions[new_x][new_y] = i
    
    # get the goal coordinates
    x = goal[0]
    y = goal[1]
    
    # flag the goal
    policy[x][y] = '*'

    # loop backwards (from goal to init)
    while x !=init[0] or y != init[1]:
        
        # get the previous coordinates
        x_prev = x - delta[actions[x][y]][0]
        y_prev = y - delta[actions[x][y]][1]
        
        # get some action
        policy[x_prev][y_prev] = delta_name[actions[x][y]]
        
        # go on
        x = x_prev
        y = y_prev
                                
    return policy # make sure you return the shortest path

# print it
for row in search(grid,init,goal,cost):
    print(row)