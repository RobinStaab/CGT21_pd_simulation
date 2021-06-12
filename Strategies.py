from abc import ABCMeta, abstractmethod
from typing import Dict, Tuple
from History import History
from random import random


class Strategy(object):

    def __init__(self) -> None:
        """ Strategy base class to be inherited from by specific strategies
        """
        pass

    @abstractmethod
    def make_move(self, player_one, player_two, game_config: Dict,  history) -> Tuple[int, float]:
        """ Makes a move for player one based on it's strategy. 
            It has access to a (potentially shared) history which contains prior encounters (of all players)
            Note that we return a tuple, only of which should a 
        Args:
            player_one (Player) one object
            player_two (Player) two object
            game_config (Dict): Dictionary containing the base setting values for the game - to be used by iterated policies
            history ([type]): (Potentially) Shared History of the players
        Returns:
            int: decision, 1 if we defect 0 if we cooperate
            int: value, For iterated policies we may have to return the payoff directly
        """
        pass

    @abstractmethod
    def iterated_move(self, player_one, player_two, game_config: Dict,  history) -> Tuple[int, float]:
        """ Makes an infinitely iterated for player one based on it's strategy. 
            It has access to a (potentially shared) history which contains prior encounters (of all players)
            Note that we return a tuple, only of which should a 
        Args:
            player_one (Player) one object
            player_two (Player) two object
            game_config (Dict): Dictionary containing the base setting values for the game - to be used by iterated policies
            history ([type]): (Potentially) Shared History of the players
        Returns:
            int: decision, 0 if we defect 1 if we cooperate
            int: value, For iterated policies we may have to return the payoff directly
        """

    @abstractmethod
    def __str__(self) -> str:
        return self.name

class Random(Strategy):

    def __init__(self, coop_prob) -> None:
        """Simple Random-Strategy 

        Args:
            coop_prob ([type]): Probability of cooperation
        """
        super().__init__()
        self.name = "R"
        self.p = coop_prob
        

    def make_move(self, player_one, player_two, game_config: Dict, history) -> int:

        r = random()
        
        return int(r < self.p), 0


    def iterated_move(self, player_one, player_two, game_config: Dict, history) -> Tuple[int, float]:
        raise NotImplementedError
        return super().iterated_move(player_one, player_two, game_config, history)


    def __str__(self) -> str:
        return f"{self.name} p: {self.p}"


class Cooperate(Strategy):

    def __init__(self, coop_prob) -> None:
        """Simple Random-Strategy 

        Args:
            coop_prob ([type]): Probability of cooperation
        """
        super().__init__()
        self.name = "COOPERATE"

        

    def make_move(self, player_one, player_two, game_config: Dict, history) -> int:
        return 0, 0


    def iterated_move(self, player_one, player_two, game_config: Dict, history) -> Tuple[int, float]:
        raise NotImplementedError
        return super().iterated_move(player_one, player_two, game_config, history)


    def __str__(self) -> str:
        return f"{self.name} p: {self.p}"

class TFT(Strategy):

    def __init__(self) -> None:
        """ Tit for Tat implementation
        """
        self.name = "TFT"
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict, history) -> Tuple[int, float]:
        raise NotImplementedError
        # Check if a last move against this player existed and if yes, copy it
        return super().make_move(player_one, player_two, game_config, history)

    def iterated_move(self, player_one, player_two, game_config: Dict, history) -> Tuple[int, float]:
        raise NotImplementedError
        # Directly return the payoff - what does happen if we meet a player again? (e.g., can the case happen where we start with Defect?)
        return super().iterated_move(player_one, player_two, game_config, history)
    
    def __str__(self) -> str:
        return super().__str__()
