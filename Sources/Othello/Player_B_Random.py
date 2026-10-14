import requests
import time
import random
import sys

API_KEY = "othello_B_158d942ed0b4465bbd7720dcfa9889a8"
SESSION_ID = "cd14c732-606c-41ff-9b88-9f529298c4c3"
ROLE = "B"
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
        res = requests.post(f"{BASE_URL}/games/othello/move/", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error playing move: {e}")
        return None


if __name__ == "__main__":
    print(f"Starting RANDOM Othello Agent for Player {ROLE} (Session: {SESSION_ID})")
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
                target = random.choice(valid_moves)
                print(f"Placing RANDOM disc {ROLE} at {target}")
                play_move(target[0], target[1])
            else:
                print("No valid moves available. Passing...")

        time.sleep(0.5)
