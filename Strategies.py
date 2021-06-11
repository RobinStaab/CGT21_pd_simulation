from abc import ABCMeta, abstractmethod
from Player import Player
from random import random

class Strategy(object):

    def __init__(self) -> None:
        """ Strategy base class to be inherited from by specific strategies
        """
        pass

    @abstractmethod
    def make_move(self, player_one: Player, player_two: Player, history) -> int:
        """ Makes a move for player one based on it's strategy. 
            It has access to a (potentially shared) history which contains prior encounters (of all players)

        Args:
            player_one (Player): Player one object
            player_two (Player): Player two object
            history ([type]): (Potentially) Shared History of the players
        Returns:
            int: 1 If we defect 0 if we cooperate
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class Random(Strategy):

    def __init__(self, coop_prob) -> None:
        """Simple Random-Strategy 

        Args:
            coop_prob ([type]): Probability of cooperation
        """
        super().__init__()
        self.name = "RANDOM"
        self.p = coop_prob
        

    def make_move(self, player_one: Player, player_two: Player, history) -> int:

        r = random()
        
        return int(r < self.p)

    def __str__(self) -> str:
        return f"{self.name} p: {self.p}"