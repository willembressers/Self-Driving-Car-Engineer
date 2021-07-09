# ----------
# User Instructions:
# 
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 0],
		[0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
		 [ 0, -1], # go left
		 [ 1, 0 ], # go down
		 [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def optimum_policy(grid,goal,cost):
	wall = 99
	x_max = len(grid)
	y_max = len(grid[0])

	# initialize an empty grid
	value = [[wall for col in range(y_max)] for row in range(x_max)]
	policy = [[' ' for col in range(y_max)] for row in range(x_max)]

	# set the goal
	value[goal[0]][goal[1]] = 0
	policy[goal[0]][goal[1]] = '*'

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

					# loop over all actions
					for action_id, action in enumerate(delta):

						# get the coordinates of the adjacent cell
						x_adjacent = x + action[0]
						y_adjacent = y + action[1]

						# check if we're still within the grid
						if (x_adjacent >= 0 and x_adjacent < x_max) and (y_adjacent >= 0 and y_adjacent < y_max):

							# ensure the adjacent cell is not a wall
							if grid[x_adjacent][y_adjacent] == 0:

								# determine the value of the adjacent cell
								adjacent_value = value[x_adjacent][y_adjacent] + cost
								
								# now get the smallest value from the adjacent cells
								if adjacent_value < value[x][y]:
									value[x][y] = adjacent_value
									policy[x][y] = delta_name[action_id]
									repeat = True

	return policy 

# print('='*80)
# print('INPUT')
# print('='*80)

# # print it
# for row in grid:
# 	print(row)

# print('='*80)
# print('POLICY')
# print('='*80)

# print it
for row in optimum_policy(grid,goal,cost):
	print(row)	