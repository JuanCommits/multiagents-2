# Agent Testing Script

This script tests different agent combinations playing various games and generates results and visualizations based on win percentages.

## Features

- Tests all agent combinations (order doesn't matter) on specified games
- Configurable agents and games through `config.py`
- Saves results to CSV file
- Generates bar graphs showing win percentages
- Provides detailed summary of results

## Files

- `test_agents.py` - Main testing script
- `config.py` - Configuration file for agents and games
- `requirements.txt` - Python dependencies
- `agent_testing_results.csv` - Output CSV file (generated after running)
- `agent_testing_results.png` - Output graph (generated after running)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script with default configuration:
```bash
python test_agents.py
```

This will:
- Test random vs minimax agents on tic-tac-toe and nocca nocca
- Play 100 games for each combination
- Save results to `agent_testing_results.csv`
- Generate a bar graph saved as `agent_testing_results.png`

### Customization

Edit `config.py` to customize:

1. **Available Agents**: Add new agents to the `AGENTS` dictionary with their class paths and kwargs
2. **Available Games**: Add new games to the `GAMES` dictionary with their class paths and kwargs
3. **Default Testing**: Modify `DEFAULT_AGENTS` and `DEFAULT_GAMES` lists
4. **Number of Games**: Change `NUM_GAMES_PER_COMBINATION`
5. **Output Files**: Modify `RESULTS_FILE` and `GRAPH_FILE`
6. **Agent/Game Parameters**: Modify the `kwargs` dictionaries to pass specific parameters to agents and games

### Example Configuration

```python
# Test only random agent vs minimax on tic-tac-toe
DEFAULT_AGENTS = ['random', 'minimax']
DEFAULT_GAMES = ['tictactoe']
NUM_GAMES_PER_COMBINATION = 50
```

## Output

### CSV Results

The CSV file contains columns:
- `game`: Name of the game
- `agent1`, `agent2`: Names of the agents tested
- `agent1_wins`, `agent2_wins`, `draws`: Raw win counts
- `total_games`: Total number of games played
- `agent1_win_pct`, `agent2_win_pct`, `draw_pct`: Win percentages

### Graph

The bar graph shows:
- Win percentages for each agent combination
- Grouped by game
- Clear labels and legends
- Value annotations on bars

## Adding New Agents

1. Create your agent class inheriting from `base.agent.Agent`
2. Implement the `action()` method
3. Add the agent to `config.py`:
```python
AGENTS = {
    'random': {
        'class_path': 'agents.agent_random.RandomAgent',
        'kwargs': {}
    },
    'minimax': {
        'class_path': 'agents.minimax.MiniMax',
        'kwargs': {
            'depth': 10  # Search depth for minimax
        }
    },
    'my_agent': {
        'class_path': 'agents.my_agent.MyAgent',
        'kwargs': {
            'param1': 'value1',
            'param2': 'value2'
        }
    }
}
```

## Adding New Games

1. Create your game class inheriting from `base.game.AlternatingGame`
2. Implement required methods (`reset()`, `step()`, `available_actions()`, etc.)
3. Add the game to `config.py`:
```python
GAMES = {
    'tictactoe': {
        'class_path': 'games.tictactoe.tictactoe.TicTacToe',
        'kwargs': {}
    },
    'nocca_nocca': {
        'class_path': 'games.nocca_nocca.nocca_nocca.NoccaNocca',
        'kwargs': {
            'max_steps': 100
        }
    },
    'my_game': {
        'class_path': 'games.my_game.my_game.MyGame',
        'kwargs': {
            'param1': 'value1',
            'param2': 'value2'
        }
    }
}
```

## Troubleshooting

- **Import Errors**: Make sure all agent and game modules are in the correct directories
- **Game Hangs**: The script has a safety limit of 1000 steps per game
- **Missing Dependencies**: Install all packages from `requirements.txt`

## Example Output

```
Starting agent testing...
Testing agents: ['random', 'minimax']
Testing games: ['tictactoe', 'nocca_nocca']
Games per combination: 100
--------------------------------------------------

Testing game: tictactoe
==============================
Testing random vs minimax on tictactoe...
  Completed 20/100 games
  Completed 40/100 games
  Completed 60/100 games
  Completed 80/100 games
  Completed 100/100 games
  Results: random 12.0% vs minimax 88.0% (Draws: 0.0%)

Testing game: nocca_nocca
==============================
Testing random vs minimax on nocca_nocca...
  Completed 20/100 games
  Completed 40/100 games
  Completed 60/100 games
  Completed 80/100 games
  Completed 100/100 games
  Results: random 45.0% vs minimax 55.0% (Draws: 0.0%)

==================================================
All tests completed!
Results saved to agent_testing_results.csv
Graph saved to agent_testing_results.png 