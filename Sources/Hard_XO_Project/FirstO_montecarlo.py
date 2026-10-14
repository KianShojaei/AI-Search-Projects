import requests
import time
import random
import sys

API_KEY = "Add Your API Key"
SESSION_ID = "Add Your Session ID"
ROLE = "O"
BASE_URL = "https://agent.aiplayground.ir/api"

OPPONENT = "X" if ROLE == "O" else "O"


# Fetch the current Ultimate Tic-Tac-Toe session state.
def get_session():
    try:
        res = requests.get(f"{BASE_URL}/sessions/{SESSION_ID}/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Connection failure: {e}")
        time.sleep(1)
        return None


# Submit a move to the game API.
def play_move(row, col):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "action": "place",
        "row": row,
        "col": col
    }
    try:
        res = requests.post(f"{BASE_URL}/games/ultimate_tictactoe/move/", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error playing move: {e}")
        return None



# Determine the result of one small board, including a draw.
def check_grid_3x3(grid, br, bc):

    for cr in range(3):
        r = br * 3 + cr
        if grid[r][bc * 3] == grid[r][bc * 3 + 1] == grid[r][bc * 3 + 2] and grid[r][bc * 3] != "hidden":
            return grid[r][bc * 3]
    for cc in range(3):
        c = bc * 3 + cc
        if grid[br * 3][c] == grid[br * 3 + 1][c] == grid[br * 3 + 2][c] and grid[br * 3][c] != "hidden":
            return grid[br * 3][c]
    if grid[br * 3][bc * 3] == grid[br * 3 + 1][bc * 3 + 1] == grid[br * 3 + 2][bc * 3 + 2] and grid[br * 3][
        bc * 3] != "hidden":
        return grid[br * 3][bc * 3]
    if grid[br * 3][bc * 3 + 2] == grid[br * 3 + 1][bc * 3 + 1] == grid[br * 3 + 2][bc * 3] and grid[br * 3][
        bc * 3 + 2] != "hidden":
        return grid[br * 3][bc * 3 + 2]

    if all(grid[br * 3 + i][bc * 3 + j] != "hidden" for i in range(3) for j in range(3)):
        return "draw"
    return "hidden"


# Check whether a player has won across the 3x3 macro board.
def check_macro_winner(macro_grid):
    for r in range(3):
        if macro_grid[r][0] == macro_grid[r][1] == macro_grid[r][2] and macro_grid[r][0] not in ("hidden", "draw"):
            return macro_grid[r][0]
    for c in range(3):
        if macro_grid[0][c] == macro_grid[1][c] == macro_grid[2][c] and macro_grid[0][c] not in ("hidden", "draw"):
            return macro_grid[0][c]
    if macro_grid[0][0] == macro_grid[1][1] == macro_grid[2][2] and macro_grid[0][0] not in ("hidden", "draw"):
        return macro_grid[0][0]
    if macro_grid[0][2] == macro_grid[1][1] == macro_grid[2][0] and macro_grid[0][2] not in ("hidden", "draw"):
        return macro_grid[0][2]
    return None


# List legal cells under the current active-board constraint.
def get_valid_moves_local(grid, macro_grid, active_board):
    valid_cells = []
    if active_board is not None:
        br, bc = active_board
        for cr in range(3):
            for cc in range(3):
                r, c = br * 3 + cr, bc * 3 + cc
                if grid[r][c] == "hidden":
                    valid_cells.append((r, c))

    if not valid_cells:
        for br in range(3):
            for bc in range(3):
                if macro_grid[br][bc] == "hidden":
                    for cr in range(3):
                        for cc in range(3):
                            r, c = br * 3 + cr, bc * 3 + cc
                            if grid[r][c] == "hidden":
                                valid_cells.append((r, c))
    return valid_cells


# Apply one simulated move and calculate the next active small board.
def sim_step(grid, macro_grid, active_board, turn, move):
    r, c = move
    grid[r][c] = turn
    br, bc = r // 3, c // 3

    sub_winner = check_grid_3x3(grid, br, bc)
    if sub_winner != "hidden":
        macro_grid[br][bc] = sub_winner

    nr, nc = r % 3, c % 3
    if macro_grid[nr][nc] == "hidden":
        return (nr, nc)
    return None


# Simulate random continuations from a candidate move and score the outcome.
def playout(grid, macro_grid, active_board, starting_move, turn, player, opponent):
    sim_grid = [row[:] for row in grid]
    sim_macro = [row[:] for row in macro_grid]
    sim_active = active_board

    sim_active = sim_step(sim_grid, sim_macro, sim_active, turn, starting_move)
    curr_turn = "O" if turn == "X" else "X"

    max_steps = 35
    for _ in range(max_steps):
        winner = check_macro_winner(sim_macro)
        if winner:
            return 1 if winner == player else -1

        valid_moves = get_valid_moves_local(sim_grid, sim_macro, sim_active)
        if not valid_moves:
            break

        move = random.choice(valid_moves)
        sim_active = sim_step(sim_grid, sim_macro, sim_active, curr_turn, move)
        curr_turn = "O" if curr_turn == "X" else "X"

    winner = check_macro_winner(sim_macro)
    if winner == player:
        return 1
    elif winner == opponent:
        return -1
    return 0


# Compare candidates by aggregating repeated random playout results.
def find_best_move_mc(grid, macro_grid, active_board, valid_cells, player, opponent):
    best_score = -float('inf')
    best_move = None

    sim_count = 30
    for move in valid_cells:
        score = 0
        for _ in range(sim_count):
            score += playout(grid, macro_grid, active_board, move, player, player, opponent)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


# Evaluate legal moves with random playouts before submitting the selected move.
if __name__ == "__main__":
    print(f"Starting MONTE CARLO Ultimate Tic-Tac-Toe Agent for Player {ROLE} (Session: {SESSION_ID})")
    while True:
        data = get_session()
        if not data:
            continue

        state = data["state"]

        if state["game_over"]:
            winner = state.get("winner")
            if winner == ROLE:
                print("Game session complete! Outcome: WON")
            elif winner is None:
                print("Game session complete! Outcome: DRAW")
            else:
                print("Game session complete! Outcome: LOST")
            break

        if state["turn"] == ROLE:
            grid = state["grid"]
            macro_grid = state["macro_grid"]
            active_board = state["active_board"]

            valid_cells = []


            def is_board_open(br, bc):
                return macro_grid[br][bc] == "hidden"


            active_board_tuple = tuple(active_board) if active_board is not None else None

            if active_board is not None:
                br, bc = active_board[0], active_board[1]
                for cr in range(3):
                    for cc in range(3):
                        r, c = br * 3 + cr, bc * 3 + cc
                        if grid[r][c] == "hidden":
                            valid_cells.append((r, c))
            else:
                for br in range(3):
                    for bc in range(3):
                        if is_board_open(br, bc):
                            for cr in range(3):
                                for cc in range(3):
                                    r, c = br * 3 + cr, bc * 3 + cc
                                    if grid[r][c] == "hidden":
                                        valid_cells.append((r, c))

            if valid_cells:
                grid_copy = [row[:] for row in grid]
                macro_copy = [row[:] for row in macro_grid]

                best_move = find_best_move_mc(grid_copy, macro_copy, active_board_tuple, valid_cells, ROLE, OPPONENT)

                if best_move:
                    print(f"Monte Carlo Playout Selected: {ROLE} at Row {best_move[0]}, Col {best_move[1]}")
                    play_move(best_move[0], best_move[1])
                else:
                    target = random.choice(valid_cells)
                    play_move(target[0], target[1])
            else:
                print("No valid moves found.")

        time.sleep(0.5)