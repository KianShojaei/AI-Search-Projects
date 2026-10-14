# Search-based Othello agent using Minimax and a positional evaluation function.
import requests
import time
import sys

API_KEY = "Add Your API Key"
SESSION_ID = "Add Your Session ID"
ROLE = "W"
BASE_URL = "https://agent.aiplayground.ir/api"

OPPONENT = "B" if ROLE == "W" else "W"

WEIGHTS = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, 5, 1, 1, 5, -2, 10],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [10, -2, 5, 1, 1, 5, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]


# Retrieve the current board and turn information.
def get_session():
    try:
        res = requests.get(f"{BASE_URL}/sessions/{SESSION_ID}/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Connection failure: {e}")
        time.sleep(1)
        return None


# Submit a selected move to the game API.
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
        res = requests.post(f"{BASE_URL}/games/othello/move/", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error playing move: {e}")
        return None



# Apply a legal move and flip the opponent's captured pieces.
def execute_move(board, row, col, color):
    new_board = [r[:] for r in board]
    new_board[row][col] = color
    opponent = "W" if color == "B" else "B"

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        cells_to_flip = []
        while 0 <= r < 8 and 0 <= c < 8 and new_board[r][c] == opponent:
            cells_to_flip.append((r, c))
            r += dr
            c += dc
        if 0 <= r < 8 and 0 <= c < 8 and new_board[r][c] == color:
            for fr, fc in cells_to_flip:
                new_board[fr][fc] = color
    return new_board


# Enumerate moves that capture at least one opposing piece under Othello rules.
def get_valid_moves(board, color):
    opponent = "W" if color == "B" else "B"
    valid = []
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for r in range(8):
        for c in range(8):
            if board[r][c] != "hidden":
                continue
            possible = False
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                cells_to_flip = []
                while 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == opponent:
                    cells_to_flip.append((nr, nc))
                    nr += dr
                    nc += dc
                if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == color:
                    if cells_to_flip:
                        possible = True
                        break
            if possible:
                valid.append((r, c))
    return valid


def evaluate_board(board, player, opponent):
    score = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                score += WEIGHTS[r][c]
            elif board[r][c] == opponent:
                score -= WEIGHTS[r][c]
    return score


# Search the game tree to the configured depth, alternating maximizing and minimizing turns.
def minimax(board, depth, is_max, alpha, beta, player, opponent):
    if depth == 0:
        return evaluate_board(board, player, opponent)

    current_color = player if is_max else opponent
    valid_moves = get_valid_moves(board, current_color)

    if not valid_moves:
        other_color = opponent if is_max else player
        if not get_valid_moves(board, other_color):
            return evaluate_board(board, player, opponent)
        return minimax(board, depth - 1, not is_max, alpha, beta, player, opponent)

    if is_max:
        best = -float('inf')
        for r, c in valid_moves:
            next_board = execute_move(board, r, c, player)
            val = minimax(next_board, depth - 1, False, alpha, beta, player, opponent)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for r, c in valid_moves:
            next_board = execute_move(board, r, c, opponent)
            val = minimax(next_board, depth - 1, True, alpha, beta, player, opponent)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def find_best_move(board, valid_moves, player, opponent):
    best_val = -float('inf')
    best_move = None
    depth = 3

    for r, c in valid_moves:
        next_board = execute_move(board, r, c, player)
        move_val = minimax(next_board, depth - 1, False, -float('inf'), float('inf'), player, opponent)
        if move_val > best_val:
            best_val = move_val
            best_move = (r, c)
    return best_move


# Select a move from the live position and handle turns reported by the API.
if __name__ == "__main__":
    print(f"Starting MINIMAX Othello Agent for Player {ROLE} (Session: {SESSION_ID})")
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
            valid_moves = state.get("valid_moves", [])
            if valid_moves:
                moves_tuples = [tuple(m) for m in valid_moves]
                grid = state["grid"]
                board_copy = [row[:] for row in grid]

                best_move = find_best_move(board_copy, moves_tuples, ROLE, OPPONENT)

                if best_move:
                    print(f"Minimax Algorithm Selected: {ROLE} at Row {best_move[0]}, Col {best_move[1]}")
                    play_move(best_move[0], best_move[1])
                else:
                    target = valid_moves[0]
                    play_move(target[0], target[1])
            else:
                print("No valid moves available. Passing...")

        time.sleep(0.5)
