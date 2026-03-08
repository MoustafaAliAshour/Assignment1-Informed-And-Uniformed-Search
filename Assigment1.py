import time
import math
from collections import deque
from heapq import heappush, heappop
class PuzzleState:

    def __init__(self, board, parent=None, move=None, depth=0, cost=0):

        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

        # Find the position of the blank (0)
        self.blank_pos = self.board.index(0)

    def __eq__(self, other):
        """Check if two states are equal"""
        return self.board == other.board

    def __hash__(self):
        """Hash function for storing states in sets"""
        return hash(tuple(self.board))

    def __lt__(self, other):
        """Less than comparison for priority queue"""
        return False  # Will be overridden by priority in heapq

    def get_board_string(self):
        """Convert board to string for hashing"""
        return ''.join(map(str, self.board))

    def is_goal(self):
        """Check if this is the goal state"""
        return self.board == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def get_successors(self):
        """Generate all valid successor states"""
        successors = []
        row, col = self.blank_pos // 3, self.blank_pos % 3

        # Define possible moves: (direction, row_delta, col_delta)
        moves = [
            ('Up', -1, 0),
            ('Down', 1, 0),
            ('Left', 0, -1),
            ('Right', 0, 1)
        ]

        for move_name, dr, dc in moves:
            new_row, new_col = row + dr, col + dc

            # Check if move is valid
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_blank_pos = new_row * 3 + new_col

                # Create new board by swapping
                new_board = self.board.copy()
                new_board[self.blank_pos], new_board[new_blank_pos] = \
                    new_board[new_blank_pos], new_board[self.blank_pos]

                # Create new state
                new_state = PuzzleState(
                    new_board,
                    parent=self,
                    move=move_name,
                    depth=self.depth + 1,
                    cost=self.cost + 1
                )
                successors.append(new_state)

        return successors

    def display(self):
        """Display the puzzle state in a readable format"""
        print("┌───┬───┬───┐")
        for i in range(3):
            row = self.board[i*3:(i+1)*3]
            row_str = "│ " + " │ ".join(str(x) if x != 0 else " " for x in row) + " │"
            print(row_str)
            if i < 2:
                print("├───┼───┼───┤")
        print("└───┴───┴───┘")


def manhattan_distance(board):
    distance = 0
    for i in range(9):
        if board[i] != 0:  # Skip the blank tile
            current_row, current_col = i // 3, i % 3
            goal_row, goal_col = board[i] // 3, board[i] % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance


def euclidean_distance(board):

    distance = 0
    for i in range(9):
        if board[i] != 0:  # Skip the blank tile
            current_row, current_col = i // 3, i % 3
            goal_row, goal_col = board[i] // 3, board[i] % 3
            distance += math.sqrt((current_row - goal_row)**2 + (current_col - goal_col)**2)
    return distance


def get_solution_path(state):

    path = []
    while state.parent is not None:
        path.append(state.move)
        state = state.parent
    path.reverse()
    return path


def bfs(initial_state):
    start_time = time.time()

    # Initialize frontier as a queue (FIFO)
    frontier = deque([initial_state])
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        state = frontier.popleft()
        explored.add(state.get_board_string())

        if state.is_goal():
            end_time = time.time()
            path = get_solution_path(state)
            return {
                'path': path,
                'cost': len(path),
                'nodes_expanded': nodes_expanded,
                'search_depth': state.depth,
                'max_depth': max_depth,
                'running_time': end_time - start_time,
                'final_state': state
            }

        nodes_expanded += 1

        for successor in state.get_successors():
            if successor.get_board_string() not in explored:
                if successor not in frontier:
                    frontier.append(successor)
                    max_depth = max(max_depth, successor.depth)

    return None


def dfs(initial_state):

    start_time = time.time()

    # Initialize frontier as a stack (LIFO)
    frontier = [initial_state]
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        state = frontier.pop()
        explored.add(state.get_board_string())

        if state.is_goal():
            end_time = time.time()
            path = get_solution_path(state)
            return {
                'path': path,
                'cost': len(path),
                'nodes_expanded': nodes_expanded,
                'search_depth': state.depth,
                'max_depth': max_depth,
                'running_time': end_time - start_time,
                'final_state': state
            }

        nodes_expanded += 1
        max_depth = max(max_depth, state.depth)

        # Add successors in reverse order to maintain left-to-right exploration
        successors = state.get_successors()
        for successor in reversed(successors):
            if successor.get_board_string() not in explored:
                frontier.append(successor)

    return None  # No solution found


def iterative_dfs(initial_state, max_depth_limit=50):

    start_time = time.time()
    total_nodes_expanded = 0

    for depth_limit in range(max_depth_limit + 1):
        result = depth_limited_search(initial_state, depth_limit)
        total_nodes_expanded += result['nodes_expanded']

        if result['found']:
            end_time = time.time()
            path = get_solution_path(result['state'])
            return {
                'path': path,
                'cost': len(path),
                'nodes_expanded': total_nodes_expanded,
                'search_depth': result['state'].depth,
                'max_depth': depth_limit,
                'running_time': end_time - start_time,
                'final_state': result['state']
            }

    return None  # No solution found


def depth_limited_search(initial_state, depth_limit):

    frontier = [initial_state]
    explored = set()
    nodes_expanded = 0

    while frontier:
        state = frontier.pop()

        if state.is_goal():
            return {
                'found': True,
                'state': state,
                'nodes_expanded': nodes_expanded
            }

        if state.depth < depth_limit:
            explored.add(state.get_board_string())
            nodes_expanded += 1

            successors = state.get_successors()
            for successor in reversed(successors):
                if successor.get_board_string() not in explored:
                    frontier.append(successor)

    return {
        'found': False,
        'state': None,
        'nodes_expanded': nodes_expanded
    }


def a_star(initial_state, heuristic='manhattan'):

    start_time = time.time()

    # Choose heuristic function
    if heuristic == 'manhattan':
        h_func = manhattan_distance
    else:
        h_func = euclidean_distance

    # Priority queue: (f_score, counter, state)
    # Counter ensures FIFO ordering for equal f_scores
    counter = 0
    initial_h = h_func(initial_state.board)
    frontier = [(initial_h, counter, initial_state)]
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    # Track best g_score for each state
    g_scores = {initial_state.get_board_string(): 0}

    while frontier:
        f_score, _, state = heappop(frontier)

        if state.is_goal():
            end_time = time.time()
            path = get_solution_path(state)
            return {
                'path': path,
                'cost': len(path),
                'nodes_expanded': nodes_expanded,
                'search_depth': state.depth,
                'max_depth': max_depth,
                'running_time': end_time - start_time,
                'final_state': state,
                'heuristic': heuristic
            }

        state_string = state.get_board_string()
        if state_string in explored:
            continue

        explored.add(state_string)
        nodes_expanded += 1
        max_depth = max(max_depth, state.depth)

        for successor in state.get_successors():
            successor_string = successor.get_board_string()

            if successor_string not in explored:
                g = successor.cost
                h = h_func(successor.board)
                f = g + h

                # Only add if this path is better
                if successor_string not in g_scores or g < g_scores[successor_string]:
                    g_scores[successor_string] = g
                    counter += 1
                    heappush(frontier, (f, counter, successor))

    return None  # No solution found


def print_solution(result, algorithm_name):

    print("\n" + "="*60)
    print(f"SOLUTION USING {algorithm_name}")
    print("="*60)

    if result is None:
        print("No solution found!")
        return

    print(f"\nPath to Goal: {result['path']}")
    print(f"Cost of Path: {result['cost']}")
    print(f"Nodes Expanded: {result['nodes_expanded']}")
    print(f"Search Depth: {result['search_depth']}")
    print(f"Max Search Depth: {result['max_depth']}")
    print(f"Running Time: {result['running_time']:.6f} seconds")

    if 'heuristic' in result:
        print(f"Heuristic Used: {result['heuristic'].capitalize()}")

    print("\nFinal State:")
    result['final_state'].display()


def visualize_solution(initial_state, moves):

    print("\n" + "="*60)
    print("STEP-BY-STEP SOLUTION")
    print("="*60)

    state = initial_state
    print(f"\nInitial State (Step 0):")
    state.display()

    for i, move in enumerate(moves, 1):
        # Find the successor with the matching move
        successors = state.get_successors()
        state = next(s for s in successors if s.move == move)

        print(f"\nStep {i}: Move {move}")
        state.display()


def main():
    """Main function to run the 8-puzzle solver"""

    # Example initial states for testing
    # Easy puzzle (3 moves)
    easy_puzzle = [1, 2, 5, 3, 4, 0, 6, 7, 8]

    # Medium puzzle
    medium_puzzle = [0, 1, 3, 4, 2, 5, 7, 8, 6]

    # Hard puzzle
    hard_puzzle = [6, 4, 7, 8, 5, 0, 3, 2, 1]

    # You can change this to test different puzzles
    print("Select a puzzle:")
    print("1. Easy (3 moves)")
    print("2. Medium")
    print("3. Hard")
    print("4. Custom")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == '1':
        initial_board = easy_puzzle
    elif choice == '2':
        initial_board = medium_puzzle
    elif choice == '3':
        initial_board = hard_puzzle
    else:
        print("Enter the puzzle as 9 comma-separated numbers (0 for blank):")
        print("Example: 1,2,5,3,4,0,6,7,8")
        input_str = input("Puzzle: ").strip()
        initial_board = [int(x.strip()) for x in input_str.split(',')]

    initial_state = PuzzleState(initial_board)

    print("\nInitial Puzzle State:")
    initial_state.display()

    # Select algorithm
    print("\n" + "="*60)
    print("Select Algorithm:")
    print("1. BFS (Breadth-First Search)")
    print("2. DFS (Depth-First Search)")
    print("3. Iterative DFS")
    print("4. A* with Manhattan Distance")
    print("5. A* with Euclidean Distance")
    print("6. Run All Algorithms")

    algo_choice = input("\nEnter your choice (1-6): ").strip()

    if algo_choice == '1':
        result = bfs(initial_state)
        print_solution(result, "BFS")
        if result:
            visualize_solution(initial_state, result['path'])

    elif algo_choice == '2':
        result = dfs(initial_state)
        print_solution(result, "DFS")
        if result:
            visualize_solution(initial_state, result['path'])

    elif algo_choice == '3':
        result = iterative_dfs(initial_state)
        print_solution(result, "Iterative DFS")
        if result:
            visualize_solution(initial_state, result['path'])

    elif algo_choice == '4':
        result = a_star(initial_state, 'manhattan')
        print_solution(result, "A* (Manhattan Distance)")
        if result:
            visualize_solution(initial_state, result['path'])

    elif algo_choice == '5':
        result = a_star(initial_state, 'euclidean')
        print_solution(result, "A* (Euclidean Distance)")
        if result:
            visualize_solution(initial_state, result['path'])

    elif algo_choice == '6':
        algorithms = [
            ('BFS', lambda: bfs(initial_state)),
            ('DFS', lambda: dfs(initial_state)),
            ('Iterative DFS', lambda: iterative_dfs(initial_state)),
            ('A* (Manhattan)', lambda: a_star(initial_state, 'manhattan')),
            ('A* (Euclidean)', lambda: a_star(initial_state, 'euclidean'))
        ]

        results = []
        for name, algo_func in algorithms:
            print(f"\nRunning {name}...")
            result = algo_func()
            print_solution(result, name)
            if result:
                results.append((name, result))

        # Comparison table
        print("\n" + "="*60)
        print("ALGORITHM COMPARISON")
        print("="*60)
        print(f"{'Algorithm':<20} {'Cost':<8} {'Nodes':<10} {'Depth':<8} {'Time (s)':<12}")
        print("-"*60)
        for name, result in results:
            print(f"{name:<20} {result['cost']:<8} {result['nodes_expanded']:<10} "
                  f"{result['search_depth']:<8} {result['running_time']:<12.6f}")


if __name__ == "__main__":
    main()