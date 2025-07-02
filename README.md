# Multi-Agents Project

This repository contains implementations of various game-playing agents and their corresponding game environments. The project focuses on different AI algorithms and strategies for game playing.

## Project Structure

### Agents
- **Random Agent** (`agents/agent_random.py`) - A simple random move generator
- **Minimax Agent** (`agents/minimax.py`) - Implementation of the minimax algorithm
- **MCTS Agent** (`agents/mcts.py`) - Monte Carlo Tree Search implementation
- **Counterfactual Regret Agent** (`agents/counterfactualregret.py`) - Counterfactual Regret Minimization
- **Input Agent** (`agents/input_agent.py`) - Human input agent for testing

### Games
- **Kuhn Poker** (`games/kuhn.py`) - Simplified poker variant
- **Tic-Tac-Toe** (`games/tictactoe/`) - Classic 3x3 game
- **Nocca Nocca** (`games/nocca_nocca/`) - Custom game implementation

### Notebooks
- **KuhnPoker.ipynb** - Interactive notebook for Kuhn Poker experiments
- **TicTacToe.ipynb** - Interactive notebook for Tic-Tac-Toe experiments  
- **Nocca_Nocca.ipynb** - Interactive notebook for Nocca Nocca experiments

## Reports

Detailed analysis and reports are available in the following Jupyter notebooks:

- **ReporteKhunPoker.ipynb** - Comprehensive report on Kuhn Poker experiments and agent performance analysis
- **ReporteMCTS.ipynb** - Detailed report on Monte Carlo Tree Search experiments

These reports contain:
- Performance comparisons between different agents
- Algorithm analysis and optimization results
- Experimental data and visualizations
- Conclusions and insights from the experiments

## License

This project is licensed under the terms specified in the LICENSE file. 