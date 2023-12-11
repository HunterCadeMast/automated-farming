import numpy as np
import random
from field import Field

# This initializes us out nodes and our actual tree
class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.field = Field()

# This performs a search of the tree's nodes to find the best outcome so far as the 'best_child_node'
def mcts_search(root, num_iterations):
    for iteration in range(num_iterations):
        node = root
        print(f"\nIteration {iteration + 1}:")
        while not is_terminal(node.state):
            if len(node.children) == 0:
                expand(node)
            node = select_child(node)
            print(f"Selected Action: {node.action}, Visits: {node.visits}, Value: {node.value}")
        if node.children:
            best_child_node = best_child(node)
        else:
            best_child_node = node
        print(f"Best Action in iteration {iteration + 1}: {best_child_node.action}")
        backpropagate(best_child_node)
    return best_child_node

# This involves updating the statistics in the already existing nodes based on the current state outcome
def backpropagate(node):
    reward = get_reward(node.state)
    while node is not None:
        node.visits += 1
        node.value += reward
        node = node.parent

# This comes up with new actions and creates children onto the tree
def expand(node):
    possible_actions = get_possible_actions(node.state)
    for action in possible_actions:
        new_state = take_action(node.state, action)
        new_node = Node(new_state, action=action, parent=node)
        node.children.append(new_node)

# This selects the information for a specific child node
def select_child(node):
    exploration_factor = 1.0
    total_visits = sum(child.visits for child in node.children)
    log_total_visits = np.log(total_visits) if total_visits > 0 else 1.0
    ucb_values = lambda child: (child.value / (child.visits + 1)) + exploration_factor * np.sqrt(log_total_visits / (child.visits + 1))
    return max(node.children, key = ucb_values)

# This selects the information for the best child node
def best_child(node):
    return max(node.children, key = lambda child: child.visits)

# This checks if you have fallen into a hole or reached the goal and ends the state
def is_terminal(state):
    return (env.harvested_count / env.total_tiles >= 0.95 or env.planted_count / env.total_tiles >= 0.95 or env.move_count >= 30)

# All possible actions from current position.
def get_possible_actions(state):
    legal_actions = []
    next_x, next_y = calculate_next_position(state)
    current_x = env.x
    current_y = env.y
    if env.get_tile_state(next_x, next_y) == 'Grown':
        legal_actions.append((next_x, next_y))
    elif env.get_tile_state(next_x, next_y) == 'Empty':
        legal_actions.append((next_x, next_y))
    elif env.get_tile_state(current_x + 1, current_y) == 'Grown':
        env.orientation = 'E'
        legal_actions.append((current_x + 1, current_y))
    elif env.get_tile_state(current_x - 1, current_y) == 'Grown':
        env.orientation = 'W'
        legal_actions.append((current_x - 1, current_y))
    elif env.get_tile_state(current_x, current_y + 1) == 'Grown':
        env.orientation = 'N'
        legal_actions.append((current_x, current_y + 1))
    elif env.get_tile_state(current_x, current_y - 1) == 'Grown':
        env.orientation = 'S'
        legal_actions.append((current_x, current_y - 1))
    elif env.get_tile_state(current_x + 1, current_y) == 'Empty':
        env.orientation = 'E'
        legal_actions.append((current_x + 1, current_y))
    elif env.get_tile_state(current_x - 1, current_y) == 'Empty':
        env.orientation = 'W'
        legal_actions.append((current_x - 1, current_y))
    elif env.get_tile_state(current_x, current_y + 1) == 'Empty':
        env.orientation = 'N'
        legal_actions.append((current_x, current_y + 1))
    elif env.get_tile_state(current_x, current_y - 1) == 'Empty':
        env.orientation = 'S'
        legal_actions.append((current_x, current_y - 1))
    elif env.get_tile_state(current_x + 1, current_y) == 'Harvested':
        env.orientation = 'E'
        legal_actions.append((current_x + 1, current_y))
    elif env.get_tile_state(current_x - 1, current_y) == 'Harvested':
        env.orientation = 'W'
        legal_actions.append((current_x - 1, current_y))
    elif env.get_tile_state(current_x, current_y + 1) == 'Harvested':
        env.orientation = 'N'
        legal_actions.append((current_x, current_y + 1))
    elif env.get_tile_state(current_x, current_y - 1) == 'Harvested':
        env.orientation = 'S'
        legal_actions.append((current_x, current_y - 1))
    elif env.get_tile_state(current_x + 1, current_y) == 'Planted':
        env.orientation = 'E'
        legal_actions.append((current_x + 1, current_y))
    elif env.get_tile_state(current_x - 1, current_y) == 'Planted':
        env.orientation = 'W'
        legal_actions.append((current_x - 1, current_y))
    elif env.get_tile_state(current_x, current_y + 1) == 'Planted':
        env.orientation = 'N'
        legal_actions.append((current_x, current_y + 1))
    elif env.get_tile_state(current_x, current_y - 1) == 'Planted':
        env.orientation = 'S'
        legal_actions.append((current_x, current_y - 1))
    elif env.is_obstacle_at(next_x, next_y):
        if try_turn_left(state):
            turn_left(state)
        elif try_turn_right(state):
            turn_right(state)
    elif env.is_approaching_edge(next_x, next_y):
        if try_turn_left(state):
            turn_left(state)
        elif try_turn_right(state):
            turn_right(state)
    elif not legal_actions:
        legal_actions = [(env.x, env.y)]
    return legal_actions

# Calculate next position.
def calculate_next_position(state):
    next_x = env.x
    next_y = env.y
    if env.orientation == 'N':
        next_y += 1
    elif env.orientation == 'S':
        next_y -= 1
    elif env.orientation == 'W':
        next_x -= 1
    elif env.orientation == 'E':
        next_x += 1
    return next_x, next_y

# Changes orientation to the left.
def turn_left(state):
    if env.orientation == 'N':
        env.orientation = 'W'
    elif env.orientation == 'S':
        env.orientation = 'E'
    elif env.orientation == 'E':
        env.orientation = 'N'
    elif env.orientation == 'W':
        env.orientation = 'S'

# Changes orientation to the right.
def turn_right(state):
    if env.orientation == 'N':
        env.orientation = 'E'
    elif env.orientation == 'S':
        env.orientation = 'W'
    elif env.orientation == 'E':
        env.orientation = 'S'
    elif env.orientation == 'W':
        env.orientation = 'N'

# Checks if a left turn is available.
def try_turn_left(state):
    given_x = env.x
    given_y = env.y
    new_orientation = env.orientation  # Store the current orientation
    turn_left(state)
    if new_orientation == 'N':
        given_x -= 1
    elif new_orientation == 'S':
        given_x += 1
    elif new_orientation == 'W':
        given_y -= 1
    elif new_orientation == 'E':
        given_y += 1
    valid_move = env.is_within_bounds(given_x, given_y) and not env.is_obstacle_at(given_x, given_y)
    if not valid_move:
        turn_left(state)
    return valid_move

# Checks if a right turn is available.
def try_turn_right(state):
    given_x = env.x
    given_y = env.y
    new_orientation = env.orientation  # Store the current orientation
    turn_right(state)
    if new_orientation == 'N':
        given_x += 1
    elif new_orientation == 'S':
        given_x -= 1
    elif new_orientation == 'W':
        given_y += 1
    elif new_orientation == 'E':
        given_y -= 1
    valid_move = env.is_within_bounds(given_x, given_y) and not env.is_obstacle_at(given_x, given_y)
    if not valid_move:
        turn_right(state)  # Revert the turn if it's not a valid move
    return valid_move

# Checks if vehicle is approaching edge.
def is_approaching_edge(next_x, next_y):
    return (next_x >= env.width or next_y >= env.height)

# This performs whatever action is given
def take_action(state, action):
    next_x, next_y = action
    if env.previous_state == 'Harvested':
        env.set_tile_state(env.x, env.y, 'Harvested')
        env.move_count += 1
    elif env.previous_state == 'Planted':
        env.set_tile_state(env.x, env.y, 'Planted')
        env.move_count += 1
    elif env.full_state == 'Grown':
        env.change_to_harvested(env.x, env.y)
    elif env.full_state == 'Empty':
        env.change_to_planted(env.x, env.y)
    env.previous_state = env.get_tile_state(next_x, next_y)
    env.set_vehicle_position(next_x, next_y)
    env.x, env.y = next_x, next_y
    env.visited_states.add((next_x, next_y))
    env.print_field()
    print('\n')
    return action[0], action[1]

# Recieves reward.
def get_reward(state):
    if (env.harvested_count / env.total_tiles >= 0.95 or env.planted_count / env.total_tiles >= 0.95):
        return 1.0
    elif env.is_obstacle_at(env.x, env.y):
        return -1.0
    else:
        return 0.0
# Sets up environment
env = Field()
root_node = Node(env)
num_iterations = 1
best_action_node = mcts_search(root_node, num_iterations)
best_action = best_action_node.action if best_action_node else None
print("Final Best Action:", best_action)