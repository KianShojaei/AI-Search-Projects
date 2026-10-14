# AI Search Projects

A collection of Python projects developed for an Artificial Intelligence course, exploring search algorithms, constraint satisfaction, game-playing strategies, and pathfinding through small interactive agents. The projects cover board games, constraint-based puzzles, hidden-information reasoning, and a rescue scenario.

Rather than presenting one large framework, this repository keeps each agent as a separate, readable experiment. That makes it easier to inspect a strategy in context and compare different approaches without hiding them behind a shared abstraction.

## At a glance

| Project | Agents | Main ideas |
|---|---|---|
| Easy Tic-Tac-Toe | `First_X.py`, `First_O.py` | Random action selection and Minimax |
| Sudoku | `Easy.py`, `Medium.py`, `Hard.py` | Constraint satisfaction, backtracking, and Minimum Remaining Values (MRV) |
| Minesweeper | `10_10_10.py`, `30_30_30.py` | Local constraint deduction and risk-based fallback choices |
| Othello | `Player_B_Random.py`, `Player_W_minimax.py` | Random legal moves and depth-limited Minimax with positional evaluation |
| Ultimate Tic-Tac-Toe | `FirstX_random.py`, `FirstO_montecarlo.py` | Legal random moves and Monte Carlo-style random rollouts |
| Firefighter Rescue | `First.py`, `Second.py` | A* pathfinding and alternative target-selection strategies |

## What I wanted to explore

These projects look at a few complementary questions:

- **Search and planning:** How can an agent choose an action by looking ahead or finding a low-cost path?
- **Constraints and inference:** How can an agent use the information already available to narrow down valid choices?
- **Decision-making under uncertainty:** What can an agent do when its deductions do not determine a single safe move?
- **Evaluation and trade-offs:** How do simple baselines compare with strategies that spend more effort evaluating possible outcomes?

The implementations are intentionally kept as individual scripts. The goal is to make each approach inspectable, rather than to suggest that every agent uses the same architecture or has the same level of sophistication.

## How the agents work

### Tic-Tac-Toe

The two agents provide a straightforward contrast: one selects an available move at random, while the Minimax agent evaluates possible game states recursively. This offers a compact example of the difference between choosing a legal action and choosing one based on future outcomes.

### Sudoku

The Sudoku agents represent the puzzle as a constraint-satisfaction problem. They check candidate values against the board, use recursive backtracking to explore assignments, and apply the Minimum Remaining Values (MRV) heuristic to prioritize cells with fewer available candidates. The `Easy.py`, `Medium.py`, and `Hard.py` files are retained as separate difficulty/session entry points.

### Minesweeper

These agents use the numbers revealed around a cell to derive local constraints and identify moves that can be inferred from the current board. When the available deductions do not settle the next move, they fall back to a risk-based choice. The two scripts remain separate entry points for their respective board/session settings.

### Othello

The random agent chooses from the legal moves provided by the game service. The other agent uses a positional-weight matrix to evaluate board states and applies depth-limited Minimax with alpha-beta pruning. Together, they offer a useful contrast between a simple baseline and a search-based strategy.

### Ultimate Tic-Tac-Toe

The random agent selects a legal move while respecting the active small-board rule. The second agent evaluates candidate moves through repeated random playouts. This is a rollout-based Monte Carlo evaluation approach; it should not be confused with a full Monte Carlo Tree Search (MCTS) implementation.

### Firefighter Rescue

Both agents use A* to plan routes through a grid, avoiding walls and fire while assigning a higher movement cost to smoke. They differ in how they choose whom to rescue: one prioritizes the nearest reachable civilian, while the other uses a utility score that considers reward, route length, and urgency.

## Repository layout

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
├── .github/
│   └── workflows/
│       └── python-check.yml
├── requirements.txt
├── LICENSE
└── README.md
```

## Getting started

### Requirements

- Python 3
- Access to a compatible game API
- A valid session for the game you want to run
- The dependency listed in `requirements.txt`

Install the dependency from the repository root:

```bash
python -m pip install -r requirements.txt
```

### Configure an agent

The scripts use `API_KEY` and `SESSION_ID` configuration values. The public repository is intended to contain placeholders, not active credentials.

Before running a script, update the configuration in your local working copy with credentials for a compatible API session. Keep real API keys, session IDs, and access tokens out of commits, screenshots, and logs.

### Run an example

From the repository root, run:

```bash
python Sources/Easy_XO_Project/First_X.py
```

Choose the script that matches your game, player role, and session. Each agent communicates with the remote service and submits an action when appropriate. A valid key by itself does not guarantee a successful run: the endpoint, session state, and API response format must also match what the script expects.

## Validation and limitations

A GitHub Actions workflow runs a Python syntax check on pushes and pull requests. This helps catch syntax errors, but it does **not** verify game strategy, contact the remote API, or guarantee that an external session is available.

The scripts are separate implementations, not a unified package. This README describes the approaches present in the code; it does not claim that the algorithms have been rebuilt or benchmarked under a common evaluation setup. End-to-end results depend on the compatible service and session configuration.

## License

See [LICENSE](LICENSE) for the terms that apply to this repository.
