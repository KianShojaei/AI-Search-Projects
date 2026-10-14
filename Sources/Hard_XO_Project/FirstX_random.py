# Random-move agent for Ultimate Tic-Tac-Toe.
# Candidate cells are constrained by the active sub-board when the rules require one.
import requests
import time
import random
import sys

API_KEY = "Add Your API Key"
SESSION_ID = "Add Your Session ID"
ROLE = "X"
BASE_URL = "https://agent.aiplayground.ir/api"


# Retrieve the current Ultimate Tic-Tac-Toe session state.
def get_session():
    try:
        res = requests.get(f"{BASE_URL}/sessions/{SESSION_ID}/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Connection failure: {e}")
        time.sleep(1)
        return None


# Submit a selected cell to the game API.
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


# Poll the session and act only when the configured player has the turn.
if __name__ == "__main__":
    print(f"Starting RANDOM Ultimate Tic-Tac-Toe agent for Player {ROLE} (Session: {SESSION_ID})")
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

            # Build the legal candidate list for the current active-board state.
            valid_cells = []


            def is_board_open(br, bc):
                return macro_grid[br][bc] == "hidden"


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
                target = random.choice(valid_cells)
                print(f"Placing RANDOM mark {ROLE} at {target}")
                play_move(target[0], target[1])
            else:
                print("No valid moves found.")

        time.sleep(0.5)