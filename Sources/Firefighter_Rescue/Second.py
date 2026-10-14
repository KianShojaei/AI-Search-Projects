# Utility-based Firefighter Rescue agent using A* routes and civilian information.
# Target selection considers reward, path length, and the civilian's remaining health.
import requests
import time
import sys
import heapq

API_KEY = "Add Your API Key"
SESSION_ID = "Add Your Session ID"
BASE_URL = "https://agent.aiplayground.ir/api"


# Retrieve the current rescue-grid state from the API.
def get_session():
    try:
        res = requests.get(f"{BASE_URL}/sessions/{SESSION_ID}/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Connection failure: {e}")
        time.sleep(1)
        return None


# Submit one movement action to the game API.
def play_move(row, col):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "action": "move",
        "row": row,
        "col": col
    }
    try:
        res = requests.post(f"{BASE_URL}/games/firefighter/move/", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error executing move to ({row}, {col}): {e}")
        return None



# Find a route using Manhattan distance and the movement costs assigned to grid cells.
def a_star(grid, start, goal):
    R, C = 20, 20
    open_set = []
    h_start = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    heapq.heappush(open_set, (h_start, 0, start, [start]))

    visited = {}

    while open_set:
        f, g, curr, path = heapq.heappop(open_set)

        if curr == goal:
            return path

        if curr in visited and visited[curr] <= g:
            continue
        visited[curr] = g

        r, c = curr
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                cell_type = grid[nr][nc]

                if cell_type in ("wall", "fire"):
                    continue

                # Smoke remains traversable but increases the cost of entering a cell.
                step_cost = 2.0 if cell_type == "smoke" else 1.0
                next_g = g + step_cost
                next_h = abs(nr - goal[0]) + abs(nc - goal[1])
                next_f = next_g + next_h

                if (nr, nc) not in visited or next_g < visited[(nr, nc)]:
                    heapq.heappush(open_set, (next_f, next_g, (nr, nc), path + [(nr, nc)]))

    return None



# Reassess civilian priorities and execute one movement action per turn.
if __name__ == "__main__":
    print(f"Starting UTILITY-BASED Firefighter Rescue Agent (Session: {SESSION_ID})")

    while True:
        data = get_session()
        if not data:
            continue

        state = data["state"]

        if state["game_over"]:
            print(f"Game over! Outcome: {'VICTORY' if state['victory'] else 'DEFEAT'}")
            print(f"Final Score: {state['score']}")
            break

        agent_pos = tuple(state["agent_pos"])
        grid = state["grid"]
        civilians = state["civilians"]

        active_civilians = []
        for pos_str, info in civilians.items():
            if info["alive"] and not info["saved"]:
                r_str, c_str = pos_str.split(",")
                active_civilians.append((
                    int(r_str),
                    int(c_str),
                    info["reward"],
                    info["health"]
                ))

        best_path = None
        best_utility = -float('inf')

        for tr, tc, reward, health in active_civilians:
            path = a_star(grid, agent_pos, (tr, tc))
            if path:
                path_len = len(path) - 1

                if path_len >= health:
                    continue

                # Lower remaining health increases the urgency component of the score.
                urgency = 100.0 / (health + 1.0)
                utility = (reward / (path_len + 1.0)) * urgency

                if utility > best_utility:
                    best_utility = utility
                    best_path = path

        if best_path and len(best_path) > 1:
            next_step = best_path[1]
            print(
                f"Utility Optimization: Targeting civilian at {best_path[-1]} with Utility Score: {best_utility:.2f}. Next step: {next_step}")
            play_move(next_step[0], next_step[1])
        else:
            print("No viable or reachable civilians! Executing safety fallback...")
            r, c = agent_pos
            safe_moves = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 20 and 0 <= nc < 20:
                    cell_type = grid[nr][nc]
                    if cell_type not in ("wall", "fire"):
                        safe_moves.append(((nr, nc), cell_type))

            if safe_moves:
                safe_moves.sort(key=lambda x: 0 if x[1] == "empty" else 1)
                next_step = safe_moves[0][0]
                print(f"Safety First: Moving to adjacent cell {next_step}")
                play_move(next_step[0], next_step[1])
            else:
                print("Trapped! Waiting...")
                play_move(agent_pos[0], agent_pos[1])

        time.sleep(0.4)
