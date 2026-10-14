# Random Tic-Tac-Toe agent. The agent polls the game session and chooses uniformly from the currently hidden cells when it is its turn.
# API credentials and session identifiers are configured below.

import requests
import time
import random
import sys

API_KEY = "Add Your API Key"
SESSION_ID = "Add Your Session ID"
ROLE = "X"
BASE_URL = "https://agent.aiplayground.ir/api"


# Retrieve the current session state from the game API. A failed request is reported and returns None so the main loop can retry.
# Retrieve the current game state; report request failures so the loop can retry.
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
# Submit the selected cell to the game API.
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


# Poll the session and act only when it is this agent's turn.
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
            # Collect cells that have not been played yet.
            empty_cells = []
            for r in range(3):
                for c in range(3):
                    if grid[r][c] == "hidden":
                        empty_cells.append((r, c))

            if empty_cells:
                # No strategic scoring is applied: every available cell has equal selection chance.
                # This baseline gives every available cell an equal chance of selection.
                target = random.choice(empty_cells)
                print(f"Placing RANDOM mark {ROLE} at {target}")
                play_move(target[0], target[1])

        time.sleep(0.5)
