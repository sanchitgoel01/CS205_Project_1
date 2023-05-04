from enum import IntEnum
import random

# Resources used:
# "The Blind Search and Heuristic Search lecture slides and notes annotated from lecture."
# Python documentation
# https://www.geeksforgeeks.org/queue-in-python/#
# https://en.wikipedia.org/wiki/A*_search_algorithm


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
    def __init__(self, n: int) -> None:
        self.size: int = n

    def create_rand_state(self) -> list[int]:
        capacity = self.size * self.size
        initial = [ i+1 for i in range(0, capacity)]
        initial[-1] = -1
        random.shuffle(initial)

        return initial
    
    def get_blank_idx(state: list[int]):
        return state.index(-1)
    
    def get_possible_operators(self, blank_idx: int) -> list[Operators]:
        blank_row = blank_idx / self.size
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

    def apply_operator(self, state: list[int], blank_idx: int,
                       operator: Operators) -> list[int]:
        new_blank_idx = blank_idx
        # Clone state
        new_state = state.copy()

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
        new_state[new_blank_idx] = -1
        new_state[blank_idx] = temp

        return new_state
    
    def is_goal_state(self, state: list[int]) -> bool:
        for i in range(0, ((self.size * self.size) - 1)):
            if (state[i] != i + 1):
                return False
        return True

def misplaced_tile_heuristic(problem: NPuzzle, state: list[int]) -> int:
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

def manhattan_distance_heuristic(problem: NPuzzle, state: list[int]):
    size = problem.size
    total_distance = 0
    for i in range(0, (size * size)):
        # Only distance for misplaced tiles
        if (state[i] == (i + 1) or state[i] == -1):
            continue

        # Compute difference between goal index and current index
        # Goal index = state[i] (e.g 8) - 1 (idx 7)
        idx_dif = abs(i - (state[i] - 1))
        total_distance += (idx_dif // size) + (idx_dif % size)

    return total_distance

# TODO Move to user interface
def print_state(state: list[int], prefix=""):
    stringify = lambda s: prefix + "[" + ",".join(map(str, s)) + "]"
    print(stringify(state[0:3]))
    print(stringify(state[3:6]))
    print(stringify(state[6:9]))

def print_operators(operators: list[Operators]):
    print("[" + ", ".join(map(lambda op: ["UP","DOWN","LEFT","RIGHT"][int(op) - 1], operators)) + "]")

# TESTING CODE
npuzzle = NPuzzle(3)
initial_state = npuzzle.create_rand_state()
print("Initial State: ")
print_state(initial_state, prefix="  ")
initial_state_blank = NPuzzle.get_blank_idx(initial_state)
possible_ops = npuzzle.get_possible_operators(initial_state_blank)
print("Operators: ")
print_operators(possible_ops)
new_state = npuzzle.apply_operator(initial_state, initial_state_blank, possible_ops[0])
print("New State:")
print_state(new_state, "  ")
misplaced_tiles = misplaced_tile_heuristic(npuzzle, new_state)
print(f"Misplaced Tiles: {misplaced_tiles}")
print(f"Manhattan Distance: {manhattan_distance_heuristic(npuzzle, new_state)}")