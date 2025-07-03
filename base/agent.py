from base.game import AlternatingGame, AgentID

class Agent():

    def __init__(self, game:AlternatingGame, agent: AgentID, name: str = None) -> None:
        self.game = game
        self.agent = agent
        self.name = name if name is not None else agent

    def action(self):
        pass

    def policy(self):
        pass
    
    def train(self, *kwargs) -> None:
        pass
