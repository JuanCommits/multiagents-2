from base.game import AlternatingGame, AgentID
from base.agent import Agent
import numpy as np

class InputAgent(Agent):

    def __init__(self, game: AlternatingGame, agent: AgentID, seed=None) -> None:
        super().__init__(game=game, agent=agent)

    def action(self):
        return int(input('Action: '))
    
    def policy(self):
        raise ValueError('InputAgent: Not implemented')
    