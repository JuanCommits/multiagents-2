# Configuration file for agent testing
# Define the agents and games to test

# Available agents (import paths and kwargs)
# Each agent has a 'class_path' (string) and 'kwargs' (dict) for constructor parameters
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
    }
}

# Available games (import paths and kwargs)
# Each game has a 'class_path' (string) and 'kwargs' (dict) for constructor parameters
GAMES = {
    'tictactoe': {
        'class_path': 'games.tictactoe.tictactoe.TicTacToe',
        'kwargs': {}
    },
    #'nocca_nocca': {
    #    'class_path': 'games.nocca_nocca.nocca_nocca.NoccaNocca',
    #    'kwargs': {
    #        'max_steps': 100  # Maximum steps before truncation
    #    }
    #}
}

# Default configuration - agents and games to test
DEFAULT_AGENTS = ['random', 'minimax']
DEFAULT_GAMES = ['tictactoe']

# Number of games to play for each agent combination
NUM_GAMES_PER_COMBINATION = 10

# Output file for results
RESULTS_FILE = 'agent_testing_results.csv'

# Graph output file
GRAPH_FILE = 'agent_testing_results.png' 