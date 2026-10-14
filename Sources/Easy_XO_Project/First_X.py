import requests
import time
import random
import sys

API_KEY = "tictactoe_X_7f865bd0ccfe4e27b9cc58946056de43"
SESSION_ID = "c5438c1c-0500-4beb-bc28-0edb3f2f0649"
ROLE = "X"
BASE_URL = "https://agent.aiplayground.ir/api"


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


if __name__ == "__main__":
    print(f"Starting RANDOM Agent for Player {ROLE} (Session: {SESSION_ID})")
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
            empty_cells = []
            for r in range(3):
                for c in range(3):
                    if grid[r][c] == "hidden":
                        empty_cells.append((r, c))

            if empty_cells:
                target = random.choice(empty_cells)
                print(f"Placing RANDOM mark {ROLE} at {target}")
                play_move(target[0], target[1])

        time.sleep(0.5)
