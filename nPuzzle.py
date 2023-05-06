from enum import IntEnum
import functools
import heapq
from typing import Callable

# Resources used:
# "The Blind Search and Heuristic Search lecture slides and notes annotated from lecture."
# Python documentation
# https://www.geeksforgeeks.org/queue-in-python/#
# https://en.wikipedia.org/wiki/A*_search_algorithm
# https://stackoverflow.com/questions/5824382/enabling-comparison-for-classes


# Must implement
# 1) Uniform Cost Search (A* with no heuristic)
# 2) A* with the Misplaced Tile heuristic.
# 3) A* with the Manhattan Distance heuristic.

# function general-search(problem, QUEUEING-FUNCTION)
#    nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
#    loop do
#       if EMPTY(nodes) then return "failure"
#       node = REMOVE-FRONT(nodes)
#       if problem.GOAL-TEST(node.STATE) succeeds then return node
#       nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
#    end

class Operators(IntEnum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class NPuzzle:
    blank_elem = 0

    def __init__(self, n: int, initial_state: tuple[int]) -> None:
        self.size: int = n
        self.initial_state = initial_state
    
    def get_blank_idx(state: tuple[int]):
        return state.index(NPuzzle.blank_elem)
    
    def get_possible_operators(self, blank_idx: int) -> list[Operators]:
        blank_row = blank_idx // self.size
        blank_col = blank_idx % self.size

        operators = []
        if (blank_row > 0):
            operators.append(Operators.UP)

        if (blank_row < (self.size - 1)):
            operators.append(Operators.DOWN)

        if (blank_col > 0):
            operators.append(Operators.LEFT)

        if (blank_col < (self.size - 1)):
            operators.append(Operators.RIGHT)
        
        return operators

    def apply_operator(self, state: tuple[int], blank_idx: int,
                       operator: Operators) -> tuple[int]:
        new_blank_idx = blank_idx
        # Clone state
        new_state = list(state)

        match operator:
            case Operators.UP:
                new_blank_idx -= self.size
            case Operators.DOWN:
                new_blank_idx += self.size
            case Operators.RIGHT:
                new_blank_idx += 1
            case Operators.LEFT:
                new_blank_idx -= 1
        
        # Swap what's in the new blank index
        temp = new_state[new_blank_idx]
        new_state[new_blank_idx] = NPuzzle.blank_elem
        new_state[blank_idx] = temp

        return tuple(new_state)
    
    def is_goal_state(self, state: tuple[int]) -> bool:
        for i in range(0, ((self.size * self.size) - 1)):
            if (state[i] != i + 1):
                return False
        return True

def misplaced_tile_heuristic(problem: NPuzzle, state: tuple[int]) -> int:
        size = problem.size
        misplaced_tiles = 0

        # Goal state is just an array of [1, 2,...,size - 1]
        # Last element should be - 1
        # However, by checking if last element == size
        # we can avoid another if-statement
        # Even the correct state will have 1 misplaced tile count
        # so subtract 1
        for i in range(0, (size * size)):
            if (state[i] != (i + 1)):
                misplaced_tiles += 1
        
        return misplaced_tiles - 1

def manhattan_distance_heuristic(problem: NPuzzle, state: tuple[int]):
    size = problem.size
    total_distance = 0
    for i in range(0, (size * size)):
        # Only distance for misplaced tiles
        if (state[i] == (i + 1) or state[i] == NPuzzle.blank_elem):
            continue

        curr_row = i // size
        curr_col = i % size
        # Goal index = state[i] (e.g 8) - 1 (idx 7)
        goal_idx = state[i] - 1
        goal_row = goal_idx // size
        goal_col = goal_idx % size

        # Compute difference between goal index and current index
        total_distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)

    return total_distance

def uniform_cost_heuristic(problem: NPuzzle, state: tuple[int]):
    return 0

@functools.total_ordering
class SearchNode:
    def __init__(self, path_cost: int, heuristic_cost: int,
                 parent_node, state: tuple[int]):
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.parent_node = parent_node
        self.state = state
    
    def __eq__(self, other) -> bool:
        return self.path_cost == other.path_cost and \
            self.heuristic_cost == other.path_cost and \
            self.parent_node == other.parent_node and \
            self.state == other.state

    def __gt__(self, other) -> bool:
        return (self.heuristic_cost + self.path_cost) >\
              (other.heuristic_cost + other.path_cost)

def a_star_search(problem: NPuzzle, heuristic_func: Callable[[NPuzzle, tuple[int]], int]) -> SearchNode:
    nodes: list[SearchNode] = []
    max_heap_size = 0
    nodes_expanded = 1

    heapq.heapify(nodes)

    repeated_nodes: set[tuple[int]] = set()

    initial_node = SearchNode(0, heuristic_func(problem, problem.initial_state), None, problem.initial_state)
    heapq.heappush(nodes, initial_node)

    while True:
        nodes_length = len(nodes)
        if nodes_length > max_heap_size:
            max_heap_size = nodes_length

        if nodes_length == 0:
            return (SearchNode(0, 0, None, ()), max_heap_size, nodes_expanded)

        top_node = heapq.heappop(nodes)
        if problem.is_goal_state(top_node.state):
            return (top_node, max_heap_size, nodes_expanded)

        repeated_nodes.add(top_node.state)
        blank_idx = NPuzzle.get_blank_idx(top_node.state)
        nodes_expanded += 1

        operators = problem.get_possible_operators(blank_idx)
        for operator in operators:
            new_state = problem.apply_operator(top_node.state, blank_idx, operator)
            if (new_state in repeated_nodes):
                continue

            heuristic = heuristic_func(problem, new_state)
            new_path_cost = top_node.path_cost + 1
            new_node = SearchNode(new_path_cost, heuristic, top_node, new_state)
            heapq.heappush(nodes, new_node)