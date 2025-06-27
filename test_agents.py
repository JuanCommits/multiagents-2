#!/usr/bin/env python3
"""
Agent Testing Script

This script tests different agent combinations playing various games and generates
results and visualizations based on win percentages.
"""

import importlib
import itertools
import csv
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import config


class AgentTester:
    def __init__(self, agents_to_test=None, games_to_test=None, num_games=100):
        """
        Initialize the agent tester.
        
        Args:
            agents_to_test: List of agent names to test (from config.AGENTS)
            games_to_test: List of game names to test (from config.GAMES)
            num_games: Number of games to play for each combination
        """
        self.agents_to_test = agents_to_test or config.DEFAULT_AGENTS
        self.games_to_test = games_to_test or config.DEFAULT_GAMES
        self.num_games = num_games
        self.results = []
        
    def import_class(self, class_path: str):
        """Import a class from a string path."""
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    
    def create_agent(self, agent_name: str, game_instance, agent_id):
        """Create an agent instance."""
        agent_config = config.AGENTS[agent_name]
        agent_class = self.import_class(agent_config['class_path'])
        kwargs = agent_config['kwargs'].copy()
        return agent_class(game_instance, agent_id, **kwargs)
    
    def create_game(self, game_name: str):
        """Create a game instance."""
        game_config = config.GAMES[game_name]
        game_class = self.import_class(game_config['class_path'])
        kwargs = game_config['kwargs'].copy()
        return game_class(**kwargs)
    
    def play_game(self, game_instance, agent1, agent2):
        """
        Play a single game between two agents.
        
        Returns:
            Tuple of (winner_agent_id, game_length)
        """
        game_instance.reset()
        game_length = 0
        
        while not game_instance.game_over():
            current_agent_id = game_instance.agent_selection
            
            # Select the appropriate agent
            if current_agent_id == game_instance.agents[0]:
                agent = agent1
            else:
                agent = agent2
            
            # Get action from agent
            action = agent.action()
            
            # Make the move
            game_instance.step(action)
            game_length += 1
            
            # Safety check to prevent infinite loops
            if game_length > 1000:
                print(f"Warning: Game exceeded 1000 steps, terminating")
                break
        
        # Determine winner
        if game_instance.terminated():
            # Check rewards to determine winner
            rewards = game_instance.rewards
            if rewards[game_instance.agents[0]] > rewards[game_instance.agents[1]]:
                winner = game_instance.agents[0]
            elif rewards[game_instance.agents[1]] > rewards[game_instance.agents[0]]:
                winner = game_instance.agents[1]
            else:
                winner = None  # Draw
        else:
            winner = None  # Game was truncated
        
        return winner, game_length
    
    def test_agent_combination(self, game_name: str, agent1_name: str, agent2_name: str):
        """
        Test a specific agent combination on a specific game.
        
        Args:
            game_name: Name of the game to test
            agent1_name: Name of the first agent
            agent2_name: Name of the second agent
        """
        print(f"Testing {agent1_name} vs {agent2_name} on {game_name}...")
        
        wins_agent1 = 0
        wins_agent2 = 0
        draws = 0
        
        for game_num in tqdm(range(self.num_games)):
            # Create fresh instances for each game
            game_instance = self.create_game(game_name)
            agent1 = self.create_agent(agent1_name, game_instance, game_instance.agents[0])
            agent2 = self.create_agent(agent2_name, game_instance, game_instance.agents[1])
            
            winner, game_length = self.play_game(game_instance, agent1, agent2)
            
            if winner == game_instance.agents[0]:
                wins_agent1 += 1
            elif winner == game_instance.agents[1]:
                wins_agent2 += 1
            else:
                draws += 1
            
            # Progress indicator
            if (game_num + 1) % 20 == 0:
                print(f"  Completed {game_num + 1}/{self.num_games} games")
        
        # Calculate win percentages
        total_games = self.num_games
        win_pct_agent1 = (wins_agent1 / total_games) * 100
        win_pct_agent2 = (wins_agent2 / total_games) * 100
        draw_pct = (draws / total_games) * 100
        
        # Store results
        self.results.append({
            'game': game_name,
            'agent1': agent1_name,
            'agent2': agent2_name,
            'agent1_wins': wins_agent1,
            'agent2_wins': wins_agent2,
            'draws': draws,
            'total_games': total_games,
            'agent1_win_pct': win_pct_agent1,
            'agent2_win_pct': win_pct_agent2,
            'draw_pct': draw_pct
        })
        
        print(f"  Results: {agent1_name} {win_pct_agent1:.1f}% vs {agent2_name} {win_pct_agent2:.1f}% (Draws: {draw_pct:.1f}%)")
    
    def run_all_tests(self):
        """Run tests for all agent combinations on all games."""
        print("Starting agent testing...")
        print(f"Testing agents: {self.agents_to_test}")
        print(f"Testing games: {self.games_to_test}")
        print(f"Games per combination: {self.num_games}")
        print("-" * 50)
        
        for game_name in self.games_to_test:
            print(f"\nTesting game: {game_name}")
            print("=" * 30)
            
            # Test all agent combinations (order doesn't matter)
            agent_combinations = list(itertools.combinations(self.agents_to_test, 2))
            
            for agent1_name, agent2_name in agent_combinations:
                self.test_agent_combination(game_name, agent1_name, agent2_name)
        
        print("\n" + "=" * 50)
        print("All tests completed!")
    
    def save_results_to_csv(self, filename=None):
        """Save results to CSV file."""
        if filename is None:
            filename = config.RESULTS_FILE
        
        if not self.results:
            print("No results to save!")
            return
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = self.results[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
        
        print(f"Results saved to {filename}")
    
    def create_win_percentage_graph(self, filename=None):
        """Create a bar graph showing win percentages."""
        if filename is None:
            filename = config.GRAPH_FILE
        
        if not self.results:
            print("No results to graph!")
            return
        
        # Prepare data for plotting
        games = []
        combinations = []
        agent1_win_pcts = []
        agent2_win_pcts = []
        
        for result in self.results:
            games.append(result['game'])
            combination = f"{result['agent1']} vs {result['agent2']}"
            combinations.append(combination)
            agent1_win_pcts.append(result['agent1_win_pct'])
            agent2_win_pcts.append(result['agent2_win_pct'])
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        x = np.arange(len(combinations))
        width = 0.35
        
        # Create bars
        bars1 = ax.bar(x - width/2, agent1_win_pcts, width, label='Agent 1 Win %', alpha=0.8)
        bars2 = ax.bar(x + width/2, agent2_win_pcts, width, label='Agent 2 Win %', alpha=0.8)
        
        # Customize the plot
        ax.set_xlabel('Agent Combinations')
        ax.set_ylabel('Win Percentage (%)')
        ax.set_title('Agent Win Percentages by Game and Combination')
        ax.set_xticks(x)
        ax.set_xticklabels(combinations, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}%',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),  # 3 points vertical offset
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=8)
        
        # Add game labels
        for i, game in enumerate(games):
            ax.text(i, -5, game, ha='center', va='top', fontsize=10, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Graph saved to {filename}")
    
    def print_summary(self):
        """Print a summary of the results."""
        if not self.results:
            print("No results to summarize!")
            return
        
        print("\n" + "=" * 60)
        print("TESTING SUMMARY")
        print("=" * 60)
        
        # Group by game
        for game_name in self.games_to_test:
            game_results = [r for r in self.results if r['game'] == game_name]
            
            print(f"\nGame: {game_name}")
            print("-" * 40)
            
            for result in game_results:
                combination = f"{result['agent1']} vs {result['agent2']}"
                print(f"{combination:25} | {result['agent1_win_pct']:5.1f}% vs {result['agent2_win_pct']:5.1f}% | Draws: {result['draw_pct']:5.1f}%")


def main():
    """Main function to run the agent testing."""
    # You can customize which agents and games to test here
    # or use the defaults from config.py
    tester = AgentTester(
        agents_to_test=config.DEFAULT_AGENTS,
        games_to_test=config.DEFAULT_GAMES,
        num_games=config.NUM_GAMES_PER_COMBINATION
    )
    
    # Run all tests
    tester.run_all_tests()
    
    # Save results
    tester.save_results_to_csv()
    
    # Create graph
    tester.create_win_percentage_graph()
    
    # Print summary
    tester.print_summary()


if __name__ == "__main__":
    main() 