# Sudoku-solving agent for the Easy configuration. It models the puzzle as a constraint-satisfaction problem and uses backtracking with the Minimum Remaining Values heuristic.
# API credentials and session identifiers are configured below.

import requests
import time
import sys

API_KEY = "Add Your API Key"
SESSION_ID = "Add Your Session ID"
BASE_URL = "https://agent.aiplayground.ir/api"


# Retrieve the current session state from the game API. A failed request is reported and returns None so the main loop can retry.
# Retrieve the current puzzle state from the game API.
def get_session():
    try:
        res = requests.get(f"{BASE_URL}/sessions/{SESSION_ID}/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Connection failure: {e}")
        time.sleep(1)
        return None


# Submit one action to the game API and return the decoded response when the request succeeds.
# Submit a value for a selected cell.
def play_move(row, col, value):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "action": "place",
        "row": row,
        "col": col,
        "value": int(value)
    }
    try:
        res = requests.post(f"{BASE_URL}/games/sudoku/move/", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error playing move: {e}")
        return None


# Check whether a candidate Sudoku value conflicts with its row, column, or 3 × 3 box.
# Check the row, column, and containing 3 × 3 box for conflicts.
def is_valid(board, row, col, val):
    for c in range(9):
        if board[row][c] == val:
            return False

    for r in range(9):
        if board[r][col] == val:
            return False

    # Locate the 3 × 3 box containing the candidate cell.
    # Find the top-left coordinates of the cell's 3 × 3 subgrid.
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == val:
                return False

    return True


# Choose an unfilled Sudoku cell with the fewest currently legal values (Minimum Remaining Values).
# Select an empty cell with the fewest legal candidate values.
def get_mrv_cell(board):
    min_remaining = 10
    best_cell = None

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                legal_count = 0
                for val in range(1, 10):
                    if is_valid(board, r, c, val):
                        legal_count += 1

                if legal_count < min_remaining:
                    min_remaining = legal_count
                    best_cell = (r, c)

    return best_cell


# Solve the Sudoku constraint-satisfaction problem with recursive backtracking.
# Solve the puzzle recursively, undoing assignments when a branch fails.
def solve_csp(board):
    # Branch on the most constrained empty cell before exploring values.
    # Branch on the most constrained unfilled cell first.
    cell = get_mrv_cell(board)
    if not cell:
        return True

    r, c = cell
    for val in range(1, 10):
        if is_valid(board, r, c, val):
            board[r][c] = val
            if solve_csp(board):
                return True
            board[r][c] = 0

    return False




# Read the live puzzle, solve a local copy, and submit the missing values.
if __name__ == "__main__":
    print(f"Starting CSP-Sudoku agent for Session: {SESSION_ID}")

    solved_board = None

    while True:
        data = get_session()
        if not data:
            continue

        state = data["state"]
        grid = state["grid"]

        if state["game_over"]:
            if state.get("victory"):
                print("Congratulations! SUDOKU solved successfully with 0 strikes!")
            else:
                print(f"Game Over. Strikes: {state['strikes']}/{state['max_strikes']}")
            break

        local_board = []
        for r in range(9):
            row_vals = []
            for c in range(9):
                val_str = grid[r][c]
                if val_str == "hidden":
                    row_vals.append(0)
                else:
                    row_vals.append(int(val_str))
            local_board.append(row_vals)

        if solved_board is None:
            print("Analyzing clues and solving Sudoku board locally using CSP Backtracking + MRV...")
            board_to_solve = [row[:] for row in local_board]

            if solve_csp(board_to_solve):
                solved_board = board_to_solve
                print("Sudoku solved locally! Starting sequential placement...")
            else:
                print("Error: Could not solve Sudoku board locally. Check the clues.")
                sys.exit(1)

        placed = False
        for r in range(9):
            for c in range(9):
                if grid[r][c] == "hidden":
                    correct_value = solved_board[r][c]
                    print(
                        f"Placing Correct Value {correct_value} at Row {r}, Col {c} (Current Strikes: {state['strikes']})")
                    play_move(r, c, correct_value)
                    placed = True
                    break
            if placed:
                break

        time.sleep(0.4)
