# AI Search Projects

A collection of Python agents exploring search, constraint satisfaction, game-playing, and pathfinding. The agents interact with a remote game API and use different decision-making strategies depending on the environment.

## Project Overview

| Project | Source files | Main approach |
|---|---|---|
| Easy Tic-Tac-Toe | `Sources/Easy_XO_Project/First_X.py`, `First_O.py` | Random play and Minimax search |
| Sudoku | `Sources/Sudoku/Easy.py`, `Medium.py`, `Hard.py` | Constraint satisfaction, backtracking, and the Minimum Remaining Values (MRV) heuristic |
| Minesweeper | `Sources/Minesweeper/10_10_10.py`, `30_30_30.py` | Local constraint deduction with a risk-based fallback |
| Othello | `Sources/Othello/Player_B_Random.py`, `Player_W_minimax.py` | Random legal moves and depth-limited Minimax with positional weights |
| Ultimate Tic-Tac-Toe | `Sources/Hard_XO_Project/FirstX_random.py`, `FirstO_montecarlo.py` | Random legal moves and Monte Carlo-style random playout evaluation |
| Firefighter Rescue | `Sources/Firefighter_Rescue/First.py`, `Second.py` | A* pathfinding, with nearest-target selection or utility-based target selection |

## Repository Structure

```text
AI-Search-Projects/
├── Sources/
│   ├── Easy_XO_Project/
│   ├── Sudoku/
│   ├── Minesweeper/
│   ├── Othello/
│   ├── Hard_XO_Project/
│   └── Firefighter_Rescue/
└── README.md
```

## How the Agents Work

### Tic-Tac-Toe
- The random agent selects an empty cell at random.
- The Minimax agent evaluates candidate moves by recursively exploring possible game states.

### Sudoku
The Sudoku agents build a local board from the session state and solve it using constraint checks, recursive backtracking, and the MRV heuristic. They then submit values for the remaining cells through the API.

### Minesweeper
The agents derive constraints from revealed numbered cells and use those constraints to identify safe cells or likely mines. If the available deductions do not determine a move, they estimate relative risk to select a fallback cell.

### Othello
One agent chooses randomly from the server-provided legal moves. The other evaluates board positions using a positional-weight matrix and searches ahead with depth-limited Minimax and alpha-beta pruning.

### Ultimate Tic-Tac-Toe
The random agent chooses among legal cells while respecting the active small-board rule. The second agent evaluates candidate moves through repeated random playouts. This is a rollout-based Monte Carlo evaluation approach; it is not a full Monte Carlo Tree Search implementation.

### Firefighter Rescue
Both agents use A* to find paths while avoiding walls and fire and assigning a higher movement cost to smoke. One prioritizes the nearest reachable civilian; the other ranks reachable civilians with a utility score that accounts for reward, path length, and urgency.

## Requirements

- Python 3
- `requests` package
- Access to the compatible game API and a valid session

Install the Python dependency:

```bash
python -m pip install requests
```

## Configuration

The source files use two configuration values:

- `API_KEY`: your API access key
- `SESSION_ID`: the game session identifier

For safety, the repository versions use placeholders instead of real credentials. Set these values locally before running an agent. Do not commit real API keys, session identifiers, or other secrets to a public repository.

## Running an Agent

Run the desired script from the repository root. For example:

```bash
python Sources/Easy_XO_Project/First_X.py
```

Choose a script that matches the game and role configured for your session. Each agent polls its session and submits actions when it is that agent's turn.

## Scope and Notes

- The repository is a set of separate agents and experiments, not a single application.
- The scripts expect the response structure and endpoints of the compatible game API.
- The agents use different approaches so their behavior can be explored and compared.
- Comments in the source files explain the intent of key functions and decision-making steps. The documentation changes are intended to clarify the existing implementations, not redesign their algorithms.
