import math
import sys

#we start by defining our initial states
initial_state = [1, 2, 3, 4, 5, 6, 0, 7, 8] #let 0 be b -the blank tile
#initial_state = [4, 5, 1, 0, 6, 2, 3,  7, 8]
#initial_state = [2, 1, 3, 4, 5, 0, 6, 8, 7]
#initial_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
#initial_state = [4, 5, 0, 6, 1, 8, 7, 2, 3]

#initial states for 15 puzzle game
#initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 13, 14, 15]
#initial_state = [5, 1, 2, 3, 9, 6, 7, 4, 13, 10, 11, 8, 14, 0, 15, 12]
#initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 11, 13, 14, 12, 0]
#initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 12, 13, 11, 0]
#initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11, 13, 15, 0, 14]


goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
#goal_state for 15puzzle
#goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]


#The reachability check - to see if goal state can be reached from initial state
def check_solvability(state):
  # Count the number of inversions in the state
  inversion = 0
  for i in range(len(state)):
    for j in range(i + 1, len(state)):
      # Skip the empty space
      if state[i] == 0 or state[j] == 0:
        continue
      # Increment the inversions if the tiles are in reverse order
      if state[i] > state[j]:
        inversion += 1
  # Return True if the number of inversions is even, False otherwise
  return inversion % 2 == 0
#if it returns false print not solvable
if check_solvability(initial_state) != True:
  print('The initial state is not solvable')
  sys.exit(1) # exit with status 1, indicating an error

def is_solvable(state):
  # Count the number of inversions in the state
  inversions = 0
  for i in range(len(state)):
    if state[i] != 0: #'b'
      for j in range(i + 1, len(state)):
        if state[j] != 0 and state[i] > state[j]: #'b'
          inversions += 1
  # A state is solvable if the number of inversions is even
  return inversions % 2 == 0
if is_solvable(initial_state) != True:
  print('The initial state is not solvable')
  sys.exit(1) # exit with status 1, indicating an error


#we now define the heuristics
#heuristics 1 - the missing tile heuristics
def missing_tileheu(initial_state):
    missingtile = 0
    for i in range(len(initial_state)):
        if initial_state[i] != goal_state[i]:
            missingtile += 1
    return missingtile


#heuristics 2 - manhattan distance
def manhattanheu(initial_state):
  # The heuristic is the sum of the distances of each tile from its goal position
  # The distance is measured by the number of moves along the rows and columns
  distance = 0
  for i in range(len(initial_state)):
    if initial_state[i] != 0:
      # Find the row and column of the current tile
      row = i // math.sqrt(len(goal_state))
      col = i % math.sqrt(len(goal_state))
      # Find the row and column of the goal position of the tile
      #goal_row = (initial_state[i] - 1) // 3
      #goal_col = (initial_state[i] - 1) % 3
      goal_index = goal_state.index(initial_state[i])
      goal_row = goal_index // math.sqrt(len(goal_state))
      goal_col = goal_index % math.sqrt(len(goal_state))
      # Add the absolute difference of the rows and columns to the distance
      distance += abs(row - goal_row) + abs(col - goal_col)
  return distance

#heuristics 3 - euclidean distance
def euclidean_distanceheu(initial_state):
  # Initialize the distance to zero
  distance = 0
  # Loop through each tile in the state
  for i in range(len(initial_state)):
    # Skip the empty space
    if initial_state[i] == 0:
      continue
    # Find the correct position of the tile in the goal state
    j = goal_state.index(initial_state[i])
    # Add the squared distance to the total distance
    distance += (i // math.sqrt(len(goal_state)) - j // math.sqrt(len(goal_state))) ** 2 + (i % math.sqrt(len(goal_state)) - j % math.sqrt(len(goal_state))) ** 2
  # Return the square root of the total distance
  return math.sqrt(distance)

## Define a function that generates the possible moves for a given state, by swapping the empty space with one of its adjacent tiles
def generate_moves(state):
  # Find the index of the empty space
  i = state.index(0)
  # Define the possible directions to move the empty space
  directions = [-3, 3, -1, 1]#down, up, left, right
  # Check the boundaries and edges
  if i < 3:
    directions.remove(-3)
  if i > 5:
    directions.remove(3)
  if i % 3 == 0:
    directions.remove(-1)
  if i % 3 == 2:
    directions.remove(1)
  # Generate the new states by swapping the empty space with the adjacent tiles
  moves = []
  for d in directions:
    new_state = state.copy()
    new_state[i], new_state[i + d] = new_state[i + d], new_state[i]
    moves.append(new_state)
  return moves



#this defines move generation for 15 puzzle. check replit
def generate_moves15(state):
  # Find the index of the empty space
  i = state.index(0)
  # Define the possible directions to move the empty space
  directions = [-4, 4, -1, 1]
  # Check the boundaries and edges
  if i < 4:
    directions.remove(-4)
  if i > 12:
    directions.remove(4)
  if i % 4 == 0:
    directions.remove(-1)
  if i % 4 == 3:
    directions.remove(1)
  # Generate the new states by swapping the empty space with the adjacent tiles
  moves = []
  for d in directions:
    new_state = state.copy()
    #new_state[i], new_state[i + d] = new_state[i + d], new_state[i]
    if 0 <= i + d < len(new_state):
      new_state[i], new_state[i + d] = new_state[i + d], new_state[i]

    moves.append(new_state)
  return moves


# Define a function that implements the A* algorithm, using a priority queue to store the states to be explored, ordered by their cost
def astar_missing_tileheu():
  # Create a priority queue to store the states to be explored, ordered by their cost
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the cost
  queue.append((initial_state, 0, missing_tileheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Repeat until the queue is empty or the goal state is found
  while queue:
    # Pop the state with the lowest cost from the queue
    state, moves, _ = queue.pop(0)
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves(state):
        # Calculate the cost of the move, which is the number of moves plus the heuristic value
        cost = moves + 1 + missing_tileheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, cost))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the cost
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None



# Define a function that implements the A* algorithm, using a priority queue to store the states to be explored, ordered by their cost
def astar_missing_tileheu15():
  # Create a priority queue to store the states to be explored, ordered by their cost
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the cost
  queue.append((initial_state, 0, missing_tileheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Repeat until the queue is empty or the goal state is found
  while queue:
    # Pop the state with the lowest cost from the queue
    state, moves, _ = queue.pop(0)
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves15(state):
        # Calculate the cost of the move, which is the number of moves plus the heuristic value
        cost = moves + 1 + missing_tileheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, cost))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the cost
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None



# Define a function that implements the A* algorithm, using a priority queue to store the states to be explored, ordered by their cost
def astar_manhattanheu():
  # Create a priority queue to store the states to be explored, ordered by their cost
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the cost
  queue.append((initial_state, 0, manhattanheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Repeat until the queue is empty or the goal state is found
  while queue:
    # Pop the state with the lowest cost from the queue
    state, moves, _ = queue.pop(0)
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves(state):
        # Calculate the cost of the move, which is the number of moves plus the heuristic value
        cost = moves + 1 + manhattanheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, cost))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the cost
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None



# Define a function that implements the A* algorithm, using a priority queue to store the states to be explored, ordered by their cost
def astar_manhattanheu15():
  # Create a priority queue to store the states to be explored, ordered by their cost
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the cost
  queue.append((initial_state, 0, manhattanheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Repeat until the queue is empty or the goal state is found
  while queue:
    # Pop the state with the lowest cost from the queue
    state, moves, _ = queue.pop(0)
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves15(state):
        # Calculate the cost of the move, which is the number of moves plus the heuristic value
        cost = moves + 1 + manhattanheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, cost))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the cost
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None



# Define a function that implements the A* algorithm, using a priority queue to store the states to be explored, ordered by their cost
def astar_euclidean_distanceheu():
  # Create a priority queue to store the states to be explored, ordered by their cost
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the cost
  queue.append((initial_state, 0, euclidean_distanceheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Repeat until the queue is empty or the goal state is found
  while queue:
    # Pop the state with the lowest cost from the queue
    state, moves, _ = queue.pop(0)
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves(state):
        # Calculate the cost of the move, which is the number of moves plus the heuristic value
        cost = moves + 1 + euclidean_distanceheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, cost))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the cost
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None


# Define a function that implements the A* algorithm, using a priority queue to store the states to be explored, ordered by their cost
def astar_euclidean_distanceheu15():
  # Create a priority queue to store the states to be explored, ordered by their cost
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the cost
  queue.append((initial_state, 0, euclidean_distanceheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Repeat until the queue is empty or the goal state is found
  while queue:
    # Pop the state with the lowest cost from the queue
    state, moves, _ = queue.pop(0)
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves15(state):
        # Calculate the cost of the move, which is the number of moves plus the heuristic value
        cost = moves + 1 + euclidean_distanceheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, cost))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the cost
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None



# Define a function that implements the GBFS algorithm, using a priority queue to store the states to be explored, ordered by their heuristic value
def gbfs_missing_tileheu():
  # Create a priority queue to store the states to be explored, ordered by their heuristic value
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the priority
  queue.append((initial_state, 0, missing_tileheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Create a variable to store the maximum number of steps
  max_steps = 4000
  # Create a variable to store the current number of steps
  current_steps = 0
  # Repeat until the queue is empty or the goal state is found or max steps reached
  while queue:
    # Pop the state with the lowest priority from the queue
    state, moves, _ = queue.pop(0)
    # Increment the current number of steps
    current_steps += 1
    # Mark the state as visited
    visited.add(tuple(state))
    if current_steps >= max_steps:
      # Stop the algorithm and print a message to the user
      print('The algorithm reached the maximum number of steps without finding a solution')
      return None, None
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves(state):
        # Calculate the priority of the move, which is the heuristic value
        priority = missing_tileheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, priority))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the priority
          queue.sort(key=lambda x:(x[2], x[1]))
  # Return None if no solution is found
  return None, None


# Define a function that implements the GBFS algorithm, using a priority queue to store the states to be explored, ordered by their heuristic value
def gbfs_missing_tileheu15():
  # Create a priority queue to store the states to be explored, ordered by their heuristic value
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the priority
  queue.append((initial_state, 0, missing_tileheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Create a variable to store the maximum number of steps
  max_steps = 4000
  # Create a variable to store the current number of steps
  current_steps = 0
  # Repeat until the queue is empty or the goal state is found or max steps reached
  while queue:
    # Pop the state with the lowest priority from the queue
    state, moves, _ = queue.pop(0)
    # Increment the current number of steps
    current_steps += 1
    # Mark the state as visited
    visited.add(tuple(state))
    if current_steps >= max_steps:
      # Stop the algorithm and print a message to the user
      print('The algorithm reached the maximum number of steps without finding a solution')
      return None, None
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves15(state):
        # Calculate the priority of the move, which is the heuristic value
        priority = missing_tileheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, priority))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the priority
          queue.sort(key=lambda x:(x[2], x[1]))
  # Return None if no solution is found
  return None, None




# Define a function that implements the GBFS algorithm, using a priority queue to store the states to be explored, ordered by their heuristic value
def gbfs_manhattanheu():
  # Create a priority queue to store the states to be explored, ordered by their heuristic value
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the priority
  queue.append((initial_state, 0, manhattanheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Create a variable to store the maximum number of steps
  max_steps = 4000
  # Create a variable to store the current number of steps
  current_steps = 0
  # Repeat until the queue is empty or the goal state is found
  while queue:
    # Pop the state with the lowest priority from the queue
    state, moves, _ = queue.pop(0)
    # Increment the current number of steps
    current_steps += 1
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the current number of steps is equal to or greater than the maximum number of steps
    if current_steps >= max_steps:
      # Stop the algorithm and print a message to the user
      print('The algorithm reached the maximum number of steps without finding a solution')
      return None, None
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves(state):
        # Calculate the priority of the move, which is the heuristic value
        priority = manhattanheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, priority))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the priority
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None


# Define a function that implements the GBFS algorithm, using a priority queue to store the states to be explored, ordered by their heuristic value
def gbfs_manhattanheu15():
  # Create a priority queue to store the states to be explored, ordered by their heuristic value
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the priority
  queue.append((initial_state, 0, manhattanheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Create a variable to store the maximum number of steps
  max_steps = 4000
  # Create a variable to store the current number of steps
  current_steps = 0
  # Repeat until the queue is empty or the goal state is found
  while queue:
    # Pop the state with the lowest priority from the queue
    state, moves, _ = queue.pop(0)
    # Increment the current number of steps
    current_steps += 1
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the current number of steps is equal to or greater than the maximum number of steps
    if current_steps >= max_steps:
      # Stop the algorithm and print a message to the user
      print('The algorithm reached the maximum number of steps without finding a solution')
      return None, None
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves15(state):
        # Calculate the priority of the move, which is the heuristic value
        priority = manhattanheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, priority))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the priority
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None



# Define a function that implements the GBFS algorithm, using a priority queue to store the states to be explored, ordered by their heuristic value
def gbfs_euclidean_distanceheu():
  # Create a priority queue to store the states to be explored, ordered by their heuristic value
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the priority
  queue.append((initial_state, 0, euclidean_distanceheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Create a variable to store the maximum number of steps
  max_steps = 4000
  # Create a variable to store the current number of steps
  current_steps = 0
  # Repeat until the queue is empty or the goal state is found or the maximum number of steps is reached
  while queue:
    # Pop the state with the lowest priority from the queue
    state, moves, _ = queue.pop(0)
    # Increment the current number of steps
    current_steps += 1
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the current number of steps is equal to or greater than the maximum number of steps
    if current_steps >= max_steps:
      # Stop the algorithm and print a message to the user
      print('The algorithm reached the maximum number of steps without finding a solution')
      return None, None
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves(state):
        # Calculate the priority of the move, which is the heuristic value
        priority = euclidean_distanceheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, priority))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the priority
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None



# Define a function that implements the GBFS algorithm, using a priority queue to store the states to be explored, ordered by their heuristic value
def gbfs_euclidean_distanceheu15():
  # Create a priority queue to store the states to be explored, ordered by their heuristic value
  queue = []
  # Add the initial state to the queue, with zero moves and heuristic value as the priority
  queue.append((initial_state, 0, euclidean_distanceheu(initial_state)))
  # Create a dictionary to store the previous states and moves
  prev = {}
  # Create a set to store the visited states
  visited = set()
  # Create a variable to store the maximum number of steps
  max_steps = 4000
  # Create a variable to store the current number of steps
  current_steps = 0
  # Repeat until the queue is empty or the goal state is found or the maximum number of steps is reached
  while queue:
    # Pop the state with the lowest priority from the queue
    state, moves, _ = queue.pop(0)
    # Increment the current number of steps
    current_steps += 1
    # Mark the state as visited
    visited.add(tuple(state))
    # Check if the current number of steps is equal to or greater than the maximum number of steps
    if current_steps >= max_steps:
      # Stop the algorithm and print a message to the user
      print('The algorithm reached the maximum number of steps without finding a solution')
      return None, None
    # Check if the state is the goal state
    if state == goal_state:
      # Return the path from the initial state to the goal state by tracing back the previous states
      path = []
      while state != initial_state:
        path.append(state)
        state, move = prev[tuple(state)]
      path.append(initial_state)
      path.reverse()
      return path, moves
    # Otherwise, generate the possible moves for the state
    else:
      for move in generate_moves15(state):
        # Calculate the priority of the move, which is the heuristic value
        priority = euclidean_distanceheu(move)
        # Add the move to the queue, if it has not been visited before
        if tuple(move) not in visited:
          queue.append((move, moves + 1, priority))
          # Store the previous state and move
          prev[tuple(move)] = (state, move)
          # Sort the queue by the priority
          queue.sort(key=lambda x: (x[2], x[1]))
  # Return None if no solution is found
  return None, None



# Test the code with different initial states and goal states
# for 8 puzzle
path, moves = astar_missing_tileheu()
if path:
  print(f"Average number of steps by A* missing tiles heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by A* missing tiles heuristics.")

path, moves = astar_manhattanheu()
if path:
  print(f"Average number of steps by A* manhattan heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by A* manhattan heuristics.")
   
path, moves = astar_euclidean_distanceheu()
if path:
  print(f"Average number of steps by A* euclidean heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by A* euclidean heuristics.")
  
   
path, moves = gbfs_missing_tileheu()
if path:
  print(f"Average number of steps by GBFS missing tiles heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by GBFS missing tiles heuristics.")

path, moves = gbfs_manhattanheu()
if path:
  print(f"Average number of steps by GBFS manhattan heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by GBFS manhattan heuristics.")
  
path, moves = gbfs_euclidean_distanceheu()
if path:
  print(f"Average number of steps by GBFS euclidean heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by GBFS euclidean heuristics.")
  
  
'''
#for 15 puzzle
  
path, moves = astar_missing_tileheu15()
if path:
  print(f"Average number of steps by A* missing tiles heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by A* missing tiles heuristics.")

path, moves = astar_manhattanheu15()
if path:
  print(f"Average number of steps by A* manhattan heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by A* manhattan heuristics.")
   
path, moves = astar_euclidean_distanceheu15()
if path:
  print(f"Average number of steps by A* euclidean heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by A* euclidean heuristics.")
  
   
path, moves = gbfs_missing_tileheu15()
if path:
  print(f"Average number of steps by GBFS missing tiles heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by GBFS missing tiles heuristics.")

path, moves = gbfs_manhattanheu15()
if path:
  print(f"Average number of steps by GBFS manhattan heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by GBFS manhattan heuristics.")
  
path, moves = gbfs_euclidean_distanceheu15()
if path:
  print(f"Average number of steps by GBFS euclidean heuristics is {moves}:")
  for state in path:
    print(state)
else:
  print("No solution found by GBFS euclidean heuristics.")
'''



print(manhattanheu(initial_state))
print(check_solvability(initial_state))

print(is_solvable(initial_state))

