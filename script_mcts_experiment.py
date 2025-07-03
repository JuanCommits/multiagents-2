import json
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from games.tictactoe.tictactoe import TicTacToe
from games.nocca_nocca.nocca_nocca import NoccaNocca

from base.agent import Agent
from base.game import AlternatingGame

from agents.minimax import MiniMax
from agents.agent_random import RandomAgent
from agents.mcts import MonteCarloTreeSearch as MCTS


def create_agents(
    agents: list[dict],
    game: AlternatingGame,
    verbose: bool = False
) -> dict[str, Agent]:
    if isinstance(game, TicTacToe):
        agent_names = ["X", "O"]
    elif isinstance(game, NoccaNocca):
        agent_names = ["Black", "White"]
    else:
        raise ValueError(f"Game {game} not supported")

    created_agents = {}
    for agent in agents:
        agent_name = agent_names.pop(0)
        if agent["type"] == "random":
            created_agents[agent_name] = RandomAgent(
                game=game,
                agent=agent_name,
                name=agent.get("name", f"{agent_name}_random")
            )
        elif "mcts" in agent["type"]:
            created_agents[agent_name] = MCTS(
                game=game,
                agent=agent_name,
                verbose=verbose,
                name=agent.get("name", f"{agent_name}_mcts"),
                **agent.get("params", {})
            )
        elif "minimax" in agent["type"]:
            created_agents[agent_name] = MiniMax(
                game=game,
                agent=agent_name,
                name=agent.get("name", f"{agent_name}_minimax"),
                **agent.get("params", {})
            )
    return created_agents


def play_game(g: AlternatingGame, agents: dict[str, Agent], verbose: bool = False):
    g.reset()
    moves = 0
    while not g.done():
        action = agents[g.agent_selection].action()
        if verbose:
            print(f"Agent {g.agent_selection} plays {action}")
        g.step(action)
        if verbose:
            g.render()
        moves += 1
    rewards = [g.reward(agent) for agent in g.agents]
    if verbose:
        print(rewards)
    return rewards, moves


def play_multiple_games(
    g: AlternatingGame,
    agents: dict[str, Agent],
    agent_types: list[str] = None,
    niter: int = 2000,
    verbose: str = 'None',
    use_tqdm: bool = True
) -> tuple[dict[str, float], dict[str, float], int, float]:
    values = dict(map(lambda a: (agents[a].name, []), g.agents))
    moves = []
    rec = range(niter)
    if use_tqdm:
        rec = tqdm(range(niter), desc="Playing games")
    for _ in rec:
        _, game_moves = play_game(g, agents, verbose=verbose=='all')
        for agent in g.agents:
            values[agents[agent].name].append(g.reward(agent))
            moves.append(game_moves)
    
    cum_rewards = {agent.name: sum(values[agent.name]) for agent in agents.values()}
    wins = {agent.name: values[agent.name].count(1) for agent in agents.values()}
    draws = values[agents[g.agents[0]].name].count(0)
    avg_moves = sum(moves)/len(moves)

    if verbose == 'all' or verbose == 'outer':
        print(" ")
        print(f"""Comparing agents: {', '.join([
            agents[a].name for a in g.agents
        ])} with {niter} iterations""")
        print("Results:")
        print('--------------------------------')
        print(' - Cum rewards:', ", ".join([
            f"{agents[a].name}: {cum_rewards[agents[a].name]}" for a in g.agents
        ]))
        print(' - Wins       :', ", ".join([
            f"{agents[a].name}: {wins[agents[a].name]}" for a in g.agents
        ]))
        print(' - Draws      :', draws)
        print(' - Avg moves  :', avg_moves)
        print('--------------------------------')
        print(" ")
    return cum_rewards, wins, draws, avg_moves


def compare_agents(
    agents_to_compare: list[str],
    n_iters: int = 2000,
    step: int = None,
    verbose: bool = False,
    game_name: str = 'tic-tac-toe',
    game_max_steps: int = 100,
    use_tqdm: bool = True,
    use_tqdm_on_games: bool = False
) -> dict[str, float]:

    assert len(agents_to_compare) == 2, "Only 2 agents can be compared"
    if step is None:
        step = n_iters

    if game_name == 'tic-tac-toe' or game_name == 'tictactoe':
        game = TicTacToe()
    elif game_name == 'nocca-nocca' or game_name == 'nocca_nocca':
        game = NoccaNocca(max_steps=game_max_steps)
    else:
        raise ValueError(f"Game {game_name} not supported")

    agents = create_agents(agents_to_compare, game)
    
    results = {
        'cum_rewards': { 
            agent.name :
                [] for agent in agents.values()
        },
        'wins': {
            agent.name :
                [] for agent in agents.values()
        },
        'draws': [],
        'avg_moves': []
    }

    if use_tqdm:
        rec = tqdm(range(0, n_iters, step), desc="Playing games")
    else:
        rec = range(0, n_iters, step)

    for _ in rec:
        g_cum_rewards, g_wins, g_draws, g_avg_moves = play_multiple_games(
            game,
            agents,
            niter=step,
            agent_types=agents_to_compare,
            verbose=verbose,
            use_tqdm=use_tqdm_on_games
        )
        for agent in agents.values():
            results['cum_rewards'][agent.name].append(g_cum_rewards[agent.name])
            results['wins'][agent.name].append(g_wins[agent.name])
        results['draws'].append(g_draws)
        results['avg_moves'].append(g_avg_moves)

    return results


def plot_results(results, save_path=None, show=True):
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Game Results Analysis', fontsize=16, fontweight='bold')

    plot_cumulative_rewards(results['cum_rewards'], ax1)
    plot_wins(results['wins'], ax2)
    plot_avg_moves(results['avg_moves'], ax3)
    plot_overall_performance(results['wins'], results['cum_rewards'], ax4)

    
    if save_path:
        plt.savefig(save_path)
    if show:
        plt.tight_layout()
        plt.show()


# Plot 1: Cumulative Rewards over time
def plot_cumulative_rewards(cum_rewards, ax):
    agents = list(cum_rewards.keys())
    colors = ['red', 'blue']
    markers = ['o', 's']
    
    for i, agent in enumerate(agents):
        x_points = range(len(cum_rewards[agent]))
        ax.plot(x_points, cum_rewards[agent], f'{markers[i]}-', label=agent, color=colors[i], linewidth=2, markersize=8)
    
    ax.set_title('Cumulative Rewards Over Time')
    ax.set_xlabel('Game Batch')
    ax.set_ylabel('Cumulative Reward')
    ax.legend()
    ax.grid(True, alpha=0.3)


# Plot 2: Wins comparison
def plot_wins(wins, ax):
    agents = list(wins.keys())
    colors = ['red', 'blue']
    
    x = np.arange(len(wins[agents[0]]))
    width = 0.35
    
    for i, agent in enumerate(agents):
        offset = -width/2 if i == 0 else width/2
        ax.bar(x + offset, wins[agent], width, label=agent, color=colors[i], alpha=0.7)
    
    ax.set_title('Wins per Game Batch')
    ax.set_xlabel('Game Batch')
    ax.set_ylabel('Number of Wins')
    ax.set_xticks(x)
    ax.legend()
    ax.grid(True, alpha=0.3)


# Plot 3: Average moves per game
def plot_avg_moves(avg_moves, ax):
    x_points = range(len(avg_moves))
    ax.plot(x_points, avg_moves, 'o-', color='green', linewidth=2, markersize=8)
    ax.set_title('Average Moves per Game')
    ax.set_xlabel('Game Batch')
    ax.set_ylabel('Average Number of Moves')
    ax.grid(True, alpha=0.3)


# Plot 4: Overall performance comparison
def plot_overall_performance(all_wins, all_rewards, ax):
    total_wins = {agent: sum(wins) for agent, wins in all_wins.items()}
    total_rewards = {agent: sum(rewards) for agent, rewards in all_rewards.items()}

    agents = list(total_wins.keys())
    wins_data = list(total_wins.values())
    rewards_data = list(total_rewards.values())

    x_pos = np.arange(len(agents))
    width = 0.35

    ax_twin = ax.twinx()

    bars1 = ax.bar(x_pos - width/2, wins_data, width, label='Total Wins', color='orange', alpha=0.7)
    bars2 = ax_twin.bar(x_pos + width/2, rewards_data, width, label='Total Rewards', color='purple', alpha=0.7)

    ax.set_title('Overall Performance Summary')
    ax.set_xlabel('Agent')
    ax.set_ylabel('Total Wins', color='orange')
    ax_twin.set_ylabel('Total Rewards', color='purple')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(agents)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', color='orange', fontweight='bold')

    for bar in bars2:
        height = bar.get_height()
        ax_twin.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', color='purple', fontweight='bold')

    ax.grid(True, alpha=0.3)
    ax.grid(True, alpha=0.3)


def complete_comparison(
    agents_to_compare: list[dict],
    game_name: str,
    n_iters: int,
    step: int,
    game_max_steps: int = 100,
    use_tqdm: bool = True,
    use_tqdm_on_games: bool = False,
    save_path: str = None,
    show_plot: bool = False
) -> dict:
    results = compare_agents(
        agents_to_compare=agents_to_compare,
        n_iters=n_iters,
        step=step,
        game_name=game_name,
        game_max_steps=game_max_steps,
        use_tqdm=use_tqdm,
        use_tqdm_on_games=use_tqdm_on_games,
    )
    plot_results(
        results,
        save_path=save_path,
        show=show_plot
    )
    return results


def read_experiments_from_config(config_path: str) -> list[dict]:
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config


def run_experiments(config: dict):
    for experiment in config:
        try:
            complete_comparison(
                agents_to_compare=experiment['agents_to_compare'],
                game_name=experiment['game_name'],
                n_iters=experiment['n_iters'],
                step=experiment['step'],
                game_max_steps=experiment.get('game_max_steps', 100),
                use_tqdm_on_games=experiment.get('use_tqdm_on_games', False),
                save_path=experiment.get('save_path', None)
            )
        except Exception as e:
            print(f"Error running experiment: {e}")
            continue


if __name__ == "__main__":
    # Take the config file from the command line with the argument --config
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    args = parser.parse_args()
    print(f"Running experiments from config: {args.config}")
    config = read_experiments_from_config(args.config)
    run_experiments(config)
    print("Experiments completed!")