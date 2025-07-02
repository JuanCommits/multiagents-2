import numpy as np
from numpy import ndarray
from numpy import random
from gymnasium.spaces import Discrete, Text, Dict, Tuple
from base.game import AlternatingGame, AgentID, ActionType

class KuhnPoker(AlternatingGame):

    def __init__(self, initial_player=None, seed=None, render_mode='human', num_agents=2):
        self.render_mode = render_mode

        self.seed = seed
        random.seed(seed)

        self.agents = []
        self.players = []
        for agent in range(num_agents):
            self.agents.append(f"agent_{agent+1}")
            self.players.append(agent)


        self.initial_player = 0#initial_player

        self.possible_agents = self.agents[:]
        self.agent_name_mapping = dict(zip(self.agents, list(range(self.num_agents))))
        self.agent_selection = None

        # actions
        self._moves = ['p', 'b']
        self._num_actions = 2
        self.action_spaces = {
            agent: Discrete(self._num_actions) for agent in self.agents
        }

        # states
        self._max_moves = 3
        self._start = ''
        self._terminalset = set(['pp', 'pbp', 'pbb', 'bp', 'bb'])
        self._hist_space = Text(min_length=0, max_length=self._max_moves, charset=frozenset(self._moves))
        self._hist = None
        self._card_names = ['J', 'Q', 'K']
        if self.num_agents == 3:
            self._card_names.append('L')
            self._terminalset = set([
                'ppp', 
                'ppbpp', 'ppbpb', 'ppbbp', 'ppbbb',
                'pbpp', 'pbpb', 'pbbp', 'pbbb',
                'bpp', 'bpb', 'bbp', 'bbb'
            ])
            self._max_moves = 5

        self._num_cards = len(self._card_names)
        self._cards = list(range(self._num_cards))
        self._card_space = Discrete(self._num_cards)
        self._hand = None

        # observations
        self.observation_spaces = {
            agent: Dict({ 'card': self._card_space, 'hist': self._hist_space}) for agent in self.agents
        }
        self.terminations = {agent: False for agent in self.agents}
    
    def step(self, action: ActionType) -> None:
        agent = self.agent_selection
        # check for termination
        if (self.terminations[agent] or self.truncations[agent]):
            try:
                self._was_dead_step(action)
            except ValueError:
                print('Game has already finished - Call reset if you want to play again')
                return

        # perform step
        self._hist += self._moves[action]
        self._player = (self._player + 1) % self.num_agents
        self.agent_selection = self.agents[self._player]

        self._compute_rewards()

    def _compute_rewards(self):
        if self.num_agents == 2:
            self._compute_rewards_2()
        elif self.num_agents == 3:
            self._compute_rewards_3()

    def _set_initial(self):
        # set initial history
        self._hist = self._start

        # deal a card to each player
        random.seed(self.seed)
        self._hand = random.choice(self._cards, size=self.num_agents, replace=False)      

        # reset agent selection
        if self.initial_player is None:
            # select random player
            self.initial_player = 0 #random.choice(self.players)
 
        self._player = self.initial_player
        self.agent_selection = self.agents[self._player]

        
    def reset(self, seed: int | None = None, options: dict | None = None) -> None:
        self._set_initial()

        self.rewards = dict(map(lambda agent: (agent, None), self.agents))
        self.terminations = dict(map(lambda agent: (agent, False), self.agents))
        self.truncations = dict(map(lambda agent: (agent, False), self.agents))
        self.infos = dict(map(lambda agent: (agent, {}), self.agents))

    def render(self) -> ndarray | str | list | None:
        for agent in self.agents:
            print(agent, self._card_names[self._hand[self.agent_name_mapping[agent]]], self._hist)

    def observe(self, agent: AgentID) -> str:
        observation = str(self._hand[self.agent_name_mapping[agent]]) + self._hist
        return observation
    
    def available_actions(self):
        return list(range(self._num_actions))
    
    def random_change(self, agent: AgentID):
        agent_idx = self.agent_name_mapping[agent]
        agent_card = self._hand[agent_idx]
        other_idx = 1 - agent_idx 
        other_cards = self._cards.copy()
        other_cards.pop(agent_card)
        new_game = self.clone()
        new_game._hand[other_idx] = np.random.choice(other_cards)
        return new_game

    def action_move(self, action: ActionType) -> str:
        if action not in range(self._num_actions):
            raise ValueError(f"{action} is not a legal action.")
        
        return self._moves[action]

    def eval(self, agent: AgentID):
        """Evaluation function for minimax."""
        if self.game_over():
            return self.reward(agent)
        # Simple heuristic: higher card is better
        return self._hand[self.agent_name_mapping[agent]] / self._num_cards

    def _compute_rewards_2(self):
        if self._hist in self._terminalset:
            # game over - compute rewards
            if self._hist == 'pp':
                # pass pass
                _rewards = list(map(lambda p: 1 if p == np.argmax(self._hand) else -1, range(self.num_agents))) 
            elif self._hist == 'pbp':
                # pass bet pass
                _rewards = list(map(lambda p: 1 if p == 1 else -1, range(self.num_agents)))
            elif self._hist == 'bp':
                # bet pass
                _rewards = list(map(lambda p: 1 if p == 0 else -1, range(self.num_agents))) 
            else:
                # pass bet bet OR bet bet
                _rewards = list(map(lambda p: 2 if p == np.argmax(self._hand) else -2, range(self.num_agents)))              
        
            self.rewards = dict(map(lambda p: (p, _rewards[self.agent_name_mapping[p]]), self.agents))
            self.terminations = dict(map(lambda p: (p, True), self.agents))
    
    def _compute_rewards_3(self):
        if self._hist not in self._terminalset:
            return

        # Default payoff values
        pot = 3  # 1 ante from each
        contributions = [1] * self.num_agents  # Starting from ante
        active = [True] * self.num_agents

        # Determine contributions and active players based on actions
        turn = self.initial_player

        for move in self._hist:
            if move == 'b':
                contributions[turn] += 1
                pot += 1
            elif move == 'p':
                active[turn] = False
            turn = (turn + 1) % self.num_agents

        # Determine rewards
        num_active = sum(active)
        rewards = [0] * self.num_agents

        if num_active == 1:
            # Only one player didn't fold — they win the pot
            winner = active.index(True)
            for i in range(self.num_agents):
                rewards[i] = pot - contributions[i] if i == winner else -contributions[i]

        elif num_active == 3:
            # All called to showdown
            winner = np.argmax([card for i, card in enumerate(self._hand)])
            for i in range(self.num_agents):
                rewards[i] = pot - contributions[i] if i == winner else -contributions[i]

        elif num_active == 2:
            # One player folded, showdown between two
            indices = [i for i, a in enumerate(active) if a]
            hands = [self._hand[i] for i in indices]
            winner = indices[np.argmax(hands)]
            for i in range(self.num_agents):
                rewards[i] = pot - contributions[i] if i == winner else -contributions[i]

        # Apply to game
        self.rewards = dict((f"agent_{i+1}", rewards[i]) for i in range(self.num_agents))
        self.terminations = dict((f"agent_{i+1}", True) for i in range(self.num_agents))