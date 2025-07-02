from base.game import AlternatingGame, AgentID, ActionType
from base.agent import Agent
from math import log, sqrt
import numpy as np
from typing import Callable

class MCTSNode:
    def __init__(self, parent: 'MCTSNode', game: AlternatingGame, action: ActionType):
        self.parent = parent
        self.game = game
        self.action = action
        self.children = []
        self.explored_children = 0
        self.visits = 0
        self.value = 0
        self.cum_rewards = np.zeros(len(game.agents))
        self.agent = self.game.agent_selection

def ucb(node: MCTSNode, agent_idx: int, C=sqrt(2)) -> float:
    if node.visits == 0 or node.parent.visits == 0:
        return float('inf')
    return node.cum_rewards[agent_idx] / node.visits + C * sqrt(log(node.parent.visits)/node.visits)

def uct(node: MCTSNode, agent: AgentID) -> MCTSNode:
    agent_idx = node.game.agent_name_mapping[agent]
    child = max(node.children, key=lambda x: ucb(x, agent_idx))
    return child

class MonteCarloTreeSearch(Agent):
    def __init__(
        self, 
        game: AlternatingGame, 
        agent: AgentID, 
        simulations: int = 100, 
        rollouts: int = 10,
        selection: Callable[[MCTSNode, AgentID], MCTSNode] = uct,
        action_selection_mode: str ='max_count',
        verbose: bool = False
    ) -> None:
        """
        Parameters:
            game: alternating game associated with the agent
            agent: agent id of the agent in the game
            simulations: number of MCTS simulations (default: 100)
            rollouts: number of MC rollouts (default: 10)
            selection: tree search policy (default: uct)
            action_selection_mode: action selection mode (default: max_count) (max_count: max visits, max_value: max value)
            verbose: print debug information (default: False)
        """
        super().__init__(game=game, agent=agent)
        self.simulations = simulations
        self.rollouts = rollouts
        self.selection = selection
        self.action_selection_mode = action_selection_mode
        self.verbose = verbose
        self.agent = agent
        
    def action(self) -> ActionType:
        a, _ = self.mcts()
        return a

    def mcts(self) -> (ActionType, float):

        root = MCTSNode(parent=None, game=self.game, action=None)
        self._generate_root_children(root)

        for i in range(self.simulations):

            node = root
            node.game = self.game.clone()

            if self.verbose:
                print(i)
                node.game.render()

            # selection
            if self.verbose:
                print('selection')
            node = self.select_node(node=node)

            # expansion
            if self.verbose:
                print('expansion')
            self.expand_node(node)

            # rollout
            if self.verbose:
                print('rollout')
            rewards = self.rollout(node)

            #update values / Backprop
            if self.verbose:
                print('backprop')
            self.backprop(node, rewards)

        if self.verbose:
            print('root childs')
            for child in root.children:
                print(child.action, child.cum_rewards / child.visits)

        action, value = self.action_selection(root)

        return action, value

    def _generate_root_children(self, root: MCTSNode) -> None:
        for action in self.game.available_actions():
            child_game = self.game.clone()
            child_game.step(action)
            child_node = MCTSNode(parent=root, game=child_game, action=action)
            root.children.append(child_node)

    def backprop(self, node: MCTSNode, rewards: np.ndarray) -> None:
        curr_node = node
        while curr_node.parent:
            curr_node.visits += 1
            curr_node.cum_rewards += rewards if curr_node.agent == self.agent else -rewards
            curr_node = curr_node.parent

    def rollout(self, node: MCTSNode) -> np.ndarray:
        u = np.zeros(len(self.game.agents))
        curr_node = node
        game = curr_node.game.clone()
        while not game.game_over():
            random_action = np.random.choice(game.available_actions())
            game.step(random_action)
            u += [game.rewards[agent] for agent in game.agents]
        return u

    def select_node(self, node: MCTSNode) -> MCTSNode:
        curr_node = node
        while curr_node.children:
            if curr_node.explored_children < len(curr_node.children):
                return curr_node.children[curr_node.explored_children]
            curr_node = self.selection(curr_node, self.agent)
        return curr_node

    def expand_node(self, node: MCTSNode) -> None:
        if not node.game.game_over():
            node.parent.explored_children += 1
            for action in node.game.available_actions():
                child_game = node.game.clone()
                child_game.step(action)
                child_node = MCTSNode(parent=node, game=child_game, action=action)
                node.children.append(child_node)

    def action_selection(self, node: MCTSNode) -> (ActionType, float):
        action: ActionType = None
        value: float = 0
        if self.action_selection_mode == 'max_count':
            action = max(node.children, key=lambda x: x.visits).action
        elif self.action_selection_mode == 'max_value':
            action = max(node.children, key=lambda x: x.value).action
        return action, value
