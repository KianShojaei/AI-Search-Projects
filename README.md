# AI Search Projects

A collection of Python agents exploring search, constraint satisfaction, game-playing, and pathfinding. Each script is a separate agent intended to interact with a compatible remote game API.

## Project Overview

| Project | Agents | Main approach |
|---|---|---|
| Easy Tic-Tac-Toe | `First_X.py`, `First_O.py` | Random play and Minimax search |
| Sudoku | `Easy.py`, `Medium.py`, `Hard.py` | Constraint satisfaction, backtracking, and the Minimum Remaining Values (MRV) heuristic |
| Minesweeper | `10_10_10.py`, `30_30_30.py` | Local constraint deduction with a risk-based fallback |
| Othello | `Player_B_Random.py`, `Player_W_minimax.py` | Random legal moves and depth-limited Minimax with positional weights |
| Ultimate Tic-Tac-Toe | `FirstX_random.py`, `FirstO_montecarlo.py` | Random legal moves and Monte Carlo-style random playout evaluation |
| Firefighter Rescue | `First.py`, `Second.py` | A* pathfinding with different target-selection strategies |

## Repository Structure

```text
AI-Search-Projects/
├── Sources/
│   ├── Easy_XO_Project/
│   │   ├── First_X.py
│   │   └── First_O.py
│   ├── Sudoku/
│   │   ├── Easy.py
│   │   ├── Medium.py
│   │   └── Hard.py
│   ├── Minesweeper/
│   │   ├── 10_10_10.py
│   │   └── 30_30_30.py
│   ├── Othello/
│   │   ├── Player_B_Random.py
│   │   └── Player_W_minimax.py
│   ├── Hard_XO_Project/
│   │   ├── FirstX_random.py
│   │   └── FirstO_montecarlo.py
│   └── Firefighter_Rescue/
│       ├── First.py
│       └── Second.py
├── requirements.txt
├── LICENSE
└── README.md
```

## How the Agents Work

### Tic-Tac-Toe
The random agent selects an available cell at random. The Minimax agent recursively evaluates possible game states to choose a move.

### Sudoku
The Sudoku agents construct a board from the session state and solve it using constraint checks, recursive backtracking, and the MRV heuristic before submitting values through the API. The three filenames represent separate difficulty/session variants; they are kept as distinct entry points.

### Minesweeper
The agents derive constraints from revealed numbered cells to identify safe cells or likely mines. When deductions do not determine a move, they use estimated risk to choose a fallback cell. The two filenames are retained as separate entry points for different board/session settings.

### Othello
One agent chooses randomly from server-provided legal moves. The other evaluates positions using a positional-weight matrix and depth-limited Minimax with alpha-beta pruning.

### Ultimate Tic-Tac-Toe
The random agent chooses a legal cell while respecting the active small-board rule. The second agent evaluates candidate moves using repeated random playouts. This is a rollout-based Monte Carlo evaluation approach, not a full Monte Carlo Tree Search implementation.

### Firefighter Rescue
Both agents use A* to find paths while avoiding walls and fire and assigning a higher movement cost to smoke. One prioritizes the nearest reachable civilian; the other ranks targets using a utility score that accounts for reward, path length, and urgency.

## Requirements

- Python 3
- A compatible game API endpoint and a valid session
- The Python dependency listed in `requirements.txt`

Install the dependency from the repository root:

```bash
python -m pip install -r requirements.txt
```

## Configuration

The scripts currently use `API_KEY` and `SESSION_ID` configuration values in their source files. The public versions contain placeholders rather than working credentials.

Before running an agent, make a local copy or edit your local working tree and replace the placeholders with credentials for your own compatible API session. **Do not commit real keys, session IDs, access tokens, or other secrets.** Keep personal credentials out of screenshots and logs as well.

## Running an Agent

Run a script from the repository root. For example:

```bash
python Sources/Easy_XO_Project/First_X.py
```

Choose the script that matches the game, player role, and session configuration. Each agent communicates with the remote API and submits actions when it is that agent's turn. A valid API key alone is not sufficient if the session, endpoint, or expected response format differs from the one the script was written for.

## Validation and Scope

The source files are independent experiments rather than one unified application. Their comments and this README document the existing implementations; they do not imply that the algorithms have been redesigned.

The repository's automated check validates Python syntax. It does not call the game API or prove that a remote session is available. End-to-end behavior depends on the compatible service and session credentials.

## License

See [LICENSE](LICENSE) for the terms that apply to this repository.
