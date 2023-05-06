import nPuzzle

# Input texts adapted from the example user interface shown in the project description.

# Determining functions
def select_default_puzzle():
    return tuple([1,2,3,4,5,6,0,7,8])

def enter_puzzle():
    print("""Enter your puzzle, using a zero to represent the blank. Please only enter \
valid 8-puzzles. Enter the puzzle demilimiting the numbers with a space. Type \
RETURN only when finished.""")
    puzzle = []
    row_idx = 0
    row_text = ["first", "second", "third"]

    while row_idx < 3:
        text = input(f"Enter the {row_text[row_idx]} row: ")
        text = text.strip().split(" ")

        if not all(map(lambda s: s.isdigit() and int(s) > -1 and int(s) < 9 and int(s) not in puzzle, text)):
            print("Invalid digits entered!")
            continue

        puzzle.extend(list(map(lambda s: int(s), text)))
        row_idx += 1

    return tuple(puzzle)

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
        choice = input("Select algorithm. (1) for Uniform Cost Search, (2) for the\
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
puzzle = select_puzzle()
algorithm = select_algorithm()

problem = nPuzzle.NPuzzle(3, puzzle)

solution, max_queue_size, nodes_expanded = nPuzzle.a_star_search(problem, algorithm)
solution_path = get_solution_path(solution)
print("Initial State:")
print_state(solution_path[0].state)

for node in solution_path[1:]:
    print(f"The best state to expand with a g(n) = {node.path_cost} and h(n) = {node.heuristic_cost} is:")
    print_state(node.state)

print("Goal state!\n")
print(f"Solution depth was {solution.path_cost}")
print(f"Number of nodes expanded: {nodes_expanded}")
print(f"Max queue size: {max_queue_size}")
