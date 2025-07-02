import numpy as np
from numpy import ndarray
from base.game import (
    AlternatingGame,
    AgentID,
    ObsType,
    ActionType
)
from base.agent import Agent

class Node():

    def __init__(self, game: AlternatingGame, obs: ObsType) -> None:
        self.game = game
        self.agent = game.agent_selection
        self.obs = obs
        self.num_actions = self.game.num_actions(self.agent)
        self.cum_regrets = np.zeros(self.num_actions)
        self.cum_policy = np.zeros(self.num_actions)
        self.curr_policy = np.full(self.num_actions, 1/self.num_actions)
        self.learned_policy = self.curr_policy.copy()
        self.niter = 1

    def regret_matching(
        self, 
        utility: np.ndarray, 
        node_utility: float, 
        probability: float
    ) -> None:
        self.cum_regrets += probability * (utility - node_utility)

    def update_learned_policy(
        self
    ) -> None:
        self.niter += 1
        self.cum_policy += self.curr_policy
        self.learned_policy = self.cum_policy / self.niter

    def update(
        self,
        utility: np.ndarray,
        node_utility: float,
        probability: float
    ) -> None:
        self.regret_matching(utility, node_utility, probability)
        regrets = np.maximum(self.cum_regrets, 0)
        if regrets.sum() > 0:
            self.curr_policy = regrets / regrets.sum()
        else:
            self.curr_policy = np.full(self.num_actions, 1/self.num_actions)

    def policy(
        self
    ) -> np.ndarray:
        return self.learned_policy

class CounterFactualRegret(Agent):

    def __init__(
        self,
        game: AlternatingGame,
        agent: AgentID,
        verbose: bool = False
    ) -> None:
        super().__init__(game, agent)
        self.verbose = verbose
        self.node_dict: dict[ObsType, Node] = {}

    def action(
        self
    ) -> ActionType:
        return self.choose_action(self.game, self.agent)

    def choose_action(
        self,
        game: AlternatingGame,
        agent: AgentID
    ) -> ActionType:
        try:
            if game.observe(agent) in self.node_dict:
                node = self.node_dict[game.observe(agent)]
                a = np.argmax(np.random.multinomial(1, node.policy(), size=1))
                return a
            else:
                #raise ValueError('Train agent before calling action()')
                if self.verbose:
                    print('Node does not exist. Playing random.')
                return np.random.choice(game.action_space(agent).n)
        except:
            node = self.node_dict[game.observe(agent)]
            if self.verbose:
                print(node.policy())
            raise ValueError('Node does not exist. Playing random.')
    
    def train(
        self,
        niter: int = 1000
    ) -> None:
        for _ in range(niter):
            _ = self.cfr()

    def cfr(
        self
    ) -> dict[AgentID, float]:
        game = self.game.clone()
        game.reset()
        utility: dict[AgentID, float] = dict()
        for agent in self.game.agents:
            probability = np.ones(game.num_agents)
            utility[agent] = self.cfr_rec(
                game=game.clone(),
                learning_agent=agent,
                probability=probability
            )

            for node in self.node_dict.values():
                node.update_learned_policy()

        return utility 

    def cfr_rec(
        self,
        game: AlternatingGame,
        learning_agent: AgentID,
        probability: ndarray
    ) -> float:
        if game.game_over():
            return game.reward(learning_agent)
        
        for agent in game.agents:
            if game.game_over():
                return game.reward(learning_agent)
            
            if agent == learning_agent:
                obs = game.observe(learning_agent)
                if obs not in self.node_dict:
                    self.node_dict[obs] = Node(game, obs)
                node = self.node_dict[obs]
                node_utility = 0
                curr_policy = node.curr_policy.copy()
                utility = np.zeros(node.num_actions)
                for action in game.available_actions():
                    game_clone = game.clone()
                    game_clone.step(action)
                    new_probability = probability.copy()
                    new_probability[game.agent_name_mapping[agent]] *= curr_policy[action]
                    utility[action] = self.cfr_rec(game_clone, learning_agent, new_probability)
                    node_utility += curr_policy[action] * utility[action]

                node.update(
                    utility=utility,
                    node_utility=node_utility,
                    probability=np.prod(np.delete(probability, game.agent_name_mapping[agent]))
                )
            else:
                game.step(self.choose_action(game, agent))

        return node_utility
        
