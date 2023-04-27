from queue import Queue

# Resources used:
# "The Blind Search and Heuristic Search lecture slides and notes annotated from lecture."
# Python documentation
# https://www.geeksforgeeks.org/queue-in-python/#

# Must implement
# 1) Uniform Cost Search (A* with no hill climbing)
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

def uniform_cost_search(initial_state):
    nodes = Queue(0)
    nodes.put(initial_state)

    while True:
        if nodes.empty():
            return []
        
        node = nodes.get()

        # Check if node is goal state
        if IS_GOAL_STATE(node):
            return node

        EXPAND_NODES(node, problem.OPERATOR)

