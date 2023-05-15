import time
import nPuzzle

# Input texts adapted from the example user interface shown in the project description.

# Determining functions
def select_default_puzzle():
    print("Type in the number representing which default puzzle to use: \
1 - Depth 0, 2 - Depth 2, 3 - D4, 4 - D8, 5 - D12, 6 - D16, 7 - D20, 8 - D24")
    num_choice = 0
    while num_choice < 1 or num_choice > 8:
        choice = input("")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > 8:
            print("Invalid choice entered!")
            continue
        num_choice = int(choice)
    
    default_puzzle = [
        [1,2,3,4,5,6,7,8,0],
        [1,2,3,4,5,6,0,7,8],
        [1,2,3,5,0,6,4,7,8],
        [1,3,6,5,0,2,4,7,8],
        [1,3,6,5,0,7,4,8,2],
        [1,6,7,5,0,3,4,8,2],
        [7,1,2,4,8,5,6,3,0],
        [0,7,2,4,6,1,3,5,8]
    ][num_choice - 1]

    return (3, tuple(default_puzzle))
        

def enter_puzzle():
    print("""Enter your puzzle, using a zero to represent the blank. Please only enter \
valid 8-puzzles. Enter the puzzle demilimiting the numbers with a space. Type \
RETURN only when finished.""")
    puzzle = []
    row_idx = 0
    puzzle_size = 200
    row_text = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eigth"]

    while row_idx < puzzle_size:
        text = input(f"Enter the {row_text[row_idx]} row: ")
        text = text.strip().split(" ")

        if not all(map(lambda s: s.isdigit() and int(s) > -1 and int(s) < (puzzle_size * puzzle_size)\
                       and int(s) not in puzzle, text)):
            print("Invalid digits entered!")
            continue

        puzzle.extend(list(map(lambda s: int(s), text)))

        # Set puzzle size to number of entries
        if row_idx == 0:
            puzzle_size = len(puzzle)

        row_idx += 1

    return (puzzle_size, tuple(puzzle))

def select_puzzle():
    sel_choice = 0
    while sel_choice < 1:
        sel = input("Enter '1' to use a default puzzle or '2' to enter your own!\n")
        if len(sel) != 1 or not sel.isdigit() or int(sel) < 1 or int(sel) > 2:
            print("Invalid selection!")
            continue

        sel_choice = int(sel)

    if sel_choice == 1:
        return select_default_puzzle()
    else:
        return enter_puzzle()

def select_algorithm():
    algorithm_num = 0
    while algorithm_num < 1 or algorithm_num > 3:
        choice = input("Select algorithm. (1) for Uniform Cost Search, (2) for the \
Misplaced Tile Heuristic, or (3) the Manhattan Distance Heuristic.\n")
        if len(choice) != 1 or not choice.isdigit() or int(choice) < 1 or int(choice) > 3:
            print("Invalid selection!")
            continue

        algorithm_num = int(choice)

    return [nPuzzle.uniform_cost_heuristic, nPuzzle.misplaced_tile_heuristic,
             nPuzzle.manhattan_distance_heuristic][algorithm_num - 1]

def print_state(state: list[int], prefix=""):
    def stringify(s):
        return prefix + "[" + ",".join(map(str, s)) + "]"
    print(stringify(state[0:3]))
    print(stringify(state[3:6]))
    print(stringify(state[6:9]))

def get_solution_path(solution_state: nPuzzle.SearchNode): 
    solution_path = []
    solution_node: nPuzzle.SearchNode | None = solution_state.parent_node
    while (solution_node is not None):
        solution_path.append(solution_node)
        solution_node = solution_node.parent_node
    
    solution_path.reverse()
    return solution_path

# Main Program
print("Welcome to an 8-Puzzle Solver!")

puzzle_size, puzzle = select_puzzle()
algorithm = select_algorithm()

problem = nPuzzle.NPuzzle(puzzle_size, puzzle)

start_time = time.perf_counter()
solution, max_queue_size, nodes_expanded = nPuzzle.a_star_search(problem, algorithm)
end_time = time.perf_counter()
solution_path = get_solution_path(solution)
print("Initial State:")
print_state(puzzle)

for node in solution_path[1:]:
    print(f"The best state to expand with a g(n) = {node.path_cost} and h(n) = {node.heuristic_cost} is:")
    print_state(node.state)

print("Goal state!\n")
print(f"Solution depth was {solution.path_cost}")
print(f"Number of nodes expanded: {nodes_expanded}")
print(f"Max queue size: {max_queue_size}")
print(f"Execution Time: {(end_time - start_time)*1000:.4}ms")
