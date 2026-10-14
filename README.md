# AI Search Projects

## Overview

This repository brings together a set of small, self-contained agents for classic search, constraint-solving, and game-playing tasks. The projects explore how different problem structures call for different decision-making strategies—from random legal actions to recursive search, local constraint reasoning, and heuristic pathfinding.

The implementations were developed and tested as working agents against the associated game API. The source files are kept separate by environment so that each approach can be read and considered in its own context.

## Project Map

| Project | Files | Main approach |
|---|---|---|
| Tic-Tac-Toe | `Sources/Easy_XO_Project/First_X.py`, `First_O.py` | Random legal move selection and Minimax with alpha-beta bounds |
| Sudoku | `Sources/Sudoku/Easy.py`, `Medium.py`, `Hard.py` | Constraint satisfaction, recursive backtracking, and Minimum Remaining Values (MRV) |
| Minesweeper | `Sources/Minesweeper/10_10_10.py`, `30_30_30.py` | Local constraint deductions with a risk-based fallback |
| Othello | `Sources/Othello/Player_B_Random.py`, `Player_W_minimax.py` | Random legal moves and depth-limited Minimax with positional evaluation |
| Ultimate Tic-Tac-Toe | `Sources/Hard_XO_Project/FirstX_random.py`, `FirstO_montecarlo.py` | Random legal moves and Monte Carlo rollout evaluation |
| Firefighter Rescue | `Sources/Firefighter_Rescue/First.py`, `Second.py` | A* pathfinding and target selection, including a utility-based variant |

## Repository Structure

```text
Sources/
├── Easy_XO_Project/
├── Sudoku/
├── Minesweeper/
├── Othello/
├── Hard_XO_Project/
└── Firefighter_Rescue/
```

Each directory groups the agent implementations for one environment. File names identify the variant or player strategy.

## Approaches at a Glance

### Game-playing agents

The Tic-Tac-Toe and Othello projects contrast a simple randomized baseline with search-based decision making. The Minimax agents evaluate possible future states; where implemented, alpha-beta bounds can prune parts of the search tree without changing the Minimax decision. The Othello search also uses a positional evaluation to distinguish board locations.

Ultimate Tic-Tac-Toe adds a larger state space and the constraint that a move can determine the next sub-board. Its Monte Carlo agent compares candidate moves using repeated randomized playouts. This is rollout-based evaluation rather than a full Monte Carlo Tree Search implementation.

### Constraint solving

The Sudoku agents treat each empty cell as a variable whose values are restricted by its row, column, and 3 × 3 box. Backtracking explores legal assignments, while the MRV heuristic selects an unfilled cell with the fewest legal values to reduce unnecessary branching.

The Minesweeper agents reason from the numbered clues around each revealed cell. When local constraints do not force a move, they use a risk-based estimate to choose a fallback action.

### Pathfinding and rescue planning

The Firefighter Rescue agents use A* over a grid with four-directional movement. Walls and fire are treated as blocked cells, while smoke has a higher movement cost. The second variant additionally considers civilian reward and health when ranking reachable targets.

## Requirements

- Python 3
- The `requests` package
- Access to the associated game API
- A valid API key and session identifier for the target environment

Install the Python dependency with:

```bash
python -m pip install requests
```

## Configuration

The source files use `API_KEY`, `SESSION_ID`, and `BASE_URL` configuration values to communicate with the game service. The repository's credential placeholders are intentional: replace them locally with credentials issued for your own session before running an agent. Do not commit real API keys or private session identifiers to a public repository.

Different files may require different credentials or sessions depending on the environment and player role. Check the configuration block near the top of the selected file before launching it.

## Running an Agent

Run a script from the repository root using Python. For example:

```bash
python Sources/Easy_XO_Project/First_X.py
```

Choose the script that matches the environment and role you want to run. The agents poll the current session, act when it is their turn (where applicable), and stop when the API reports that the game has ended. Keep the process running while the agent is participating in a live session.

## Reading the Code

The comments are intended to explain the purpose of a function or a non-obvious algorithmic step, rather than restate every line. The implementations are intentionally presented as separate scripts so that the logic for each environment can be inspected without first navigating a larger framework.

## Scope and Reproducibility

These scripts are API-connected agents, not a standalone game simulator. Reproducing a run depends on the availability of the game service, a compatible session, and valid credentials. Results may also depend on the environment's initial state and, for randomized agents, the random choices made during a run.

The code documents the strategies used by these implementations; it does not claim that one strategy is universally optimal across all environments or configurations.
