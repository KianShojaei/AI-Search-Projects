import requests
import time
import sys

API_KEY = "Add Your API Key"
SESSION_ID = "Add Your Session ID"
ROLE = "O"
BASE_URL = "https://agent.aiplayground.ir/api"

OPPONENT = "X" if ROLE == "X" else "X"


def get_session():
    try:
        res = requests.get(f"{BASE_URL}/sessions/{SESSION_ID}/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Connection failure: {e}")
        time.sleep(1)
        return None


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
        res = requests.post(f"{BASE_URL}/games/tictactoe/move/", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error playing move: {e}")
        return None


def check_winner(board):
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] and board[r][0] != "hidden":
            return board[r][0]
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] and board[0][c] != "hidden":
            return board[0][c]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "hidden":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "hidden":
        return board[0][2]
    return None


def minimax(board, depth, is_max, alpha, beta, player, opponent):
    winner = check_winner(board)
    if winner == player:
        return 10 - depth
    if winner == opponent:
        return depth - 10

    has_moves = any(board[r][c] == "hidden" for r in range(3) for c in range(3))
    if not has_moves:
        return 0

    if is_max:
        best = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == "hidden":
                    board[r][c] = player
                    val = minimax(board, depth + 1, False, alpha, beta, player, opponent)
                    board[r][c] = "hidden"
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == "hidden":
                    board[r][c] = opponent
                    val = minimax(board, depth + 1, True, alpha, beta, player, opponent)
                    board[r][c] = "hidden"
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best


def find_best_move(board, player, opponent):
    best_val = -float('inf')
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == "hidden":
                board[r][c] = player
                move_val = minimax(board, 0, False, -float('inf'), float('inf'), player, opponent)
                board[r][c] = "hidden"
                if move_val > best_val:
                    best_val = move_val
                    best_move = (r, c)
    return best_move


if __name__ == "__main__":
    print(f"Starting MINIMAX Agent for Player {ROLE} (Session: {SESSION_ID})")
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
            board_copy = [row[:] for row in grid]
            best_move = find_best_move(board_copy, ROLE, OPPONENT)

            if best_move:
                r, c = best_move
                print(f"Placing MINIMAX mark {ROLE} at Row {r}, Col {c}")
                play_move(r, c)
            else:
                print("No moves left.")

        time.sleep(0.5)
