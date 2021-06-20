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
    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        """ Makes a move for player one based on it's strategy.
        Args:
            player_one (Player) one object
            player_two (Player) two object
            game_config (Dict): Dictionary containing the base setting values for the game - to be used by iterated policies
        Returns:
            int: decision, 0 if we cooperate 1 if we defect 
            int: value, For iterated policies we return the payoff directly
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        return self.name

class RANDOM(Strategy):

    def __init__(self, coop_prob) -> None:
        """Random-Strategy 

        Args:
            coop_prob ([type]): Probability of cooperation
        """
        super().__init__()
        self.name = "RANDOM"
        self.p = coop_prob
        
    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        p = self.p
        r = random()
        decision = int(r < p)

        w = player_one.omega
        R = game_config["R"]
        S = game_config["S"]
        T = game_config["T"]
        P = game_config["P"]

        if player_two.strategy.name == "RANDOM":
            p1 = p
            p2 = player_two.strategy.p
            utility = (p1*p2*R + p1*(1-p2)*S + (1-p1)*p2*T + (1-p1)*(1-p2)*P)/(1-w)
        elif player_two.strategy.name == "DEFECT":
            utility = (p*S + (1-p)*P)/(1-w)
        elif player_two.strategy.name == "COOPERATE":
            utility = (p*R + (1-p)*T)/(1-w)
        elif player_two.strategy.name == "GT":
            utility = (p*R + (1-p)*(T+w*(p*S + (1-p)*P)/(1-w)))/(1-p*w)
        elif player_two.strategy.name == "TFT":
            utility = (p**2*w*(T+S-R-P) + p*(2*w*P + R*(w-1) - 2*w*T + T - w*S) - w*P + T*(w-1))/(w-1)
        elif player_two.strategy.name == "TFTD":
            utility = (w*p**3 + w*p**2*(R-S-T-1) + w*p*T + p*(S+1-p))/(w-1)
        elif player_two.strategy.name == "TF2T":
            utility = (-1*w**2*p**4 + w**2*p**3*(3+T-R+S) + w**2*p**2*(-3-3*T+2*R-2*S) + w**2*p*(1+3*T) + p*(R-T) + w**2*p*(S-R) + T - w**2*T)/(1-w)
        else:
            raise NotImplementedError

        return decision, utility

    def __str__(self) -> str:
        return f"{self.name} p: {self.p}"

class DEFECT(Strategy):

    def __init__(self) -> None:
        """Always Defect
        """
        super().__init__()
        self.name = "DEFECT"

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        decision = 1

        w = player_one.omega
        R = game_config["R"]
        S = game_config["S"]
        T = game_config["T"]
        P = game_config["P"]

        if player_two.strategy.name == "RANDOM":
            p = player_two.strategy.p
            utility = (p*T + (1-p)*P)/(1-w)
        elif player_two.strategy.name == "DEFECT":
            utility = P/(1-w)
        elif player_two.strategy.name == "COOPERATE":
            utility = T/(1-w)
        elif player_two.strategy.name == "GT":
            utility = T + w*P/(1-w)
        elif player_two.strategy.name == "TFT":
            utility = T + w*P/(1-w)
        elif player_two.strategy.name == "TFTD":
            utility = P/(1-w)
        elif player_two.strategy.name == "TF2T":
            utility = T + w*T + w**2*P/(1-w)
        else:
            raise NotImplementedError

        return decision, utility

class COOPERATE(Strategy):

    def __init__(self) -> None:
        """Always Cooperate
        """
        super().__init__()
        self.name = "COOPERATE"

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        decision = 0

        w = player_one.omega
        R = game_config["R"]
        S = game_config["S"]
        T = game_config["T"]
        P = game_config["P"]

        if player_two.strategy.name == "RANDOM":
            p = player_two.strategy.p
            utility = (p*R + (1-p)*S)/(1-w)
        elif player_two.strategy.name == "DEFECT":
            utility = S/(1-w)
        elif player_two.strategy.name == "COOPERATE":
            utility = R/(1-w)
        elif player_two.strategy.name == "GT":
            utility = R/(1-w)
        elif player_two.strategy.name == "TFT":
            utility = R/(1-w)
        elif player_two.strategy.name == "TFTD":
            utility = S + w*R/(1-w)
        elif player_two.strategy.name == "TF2T":
            utility = R/(1-w)
        else:
            raise NotImplementedError

        return decision, utility

class GT(Strategy):

    def __init__(self) -> None:
        """ Grim Trigger
        """
        self.name = "GT"
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        # Defect if the opponent defected once
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) == 0:
            decision = 0
        elif 1 in [game.opponent_decision for game in previous_games] :
            decision = 1
        else:
            decision = 0 

        w = player_one.omega
        R = game_config["R"]
        S = game_config["S"]
        T = game_config["T"]
        P = game_config["P"]

        if player_two.strategy.name == "RANDOM":
            p = player_two.strategy.p
            utility = (p*R + (1-p)*(S+w*(p*T + (1-p)*P)/(1-w)))/(1-p*w)
        elif player_two.strategy.name == "DEFECT":
            utility = S + w*P/(1-w)
        elif player_two.strategy.name == "COOPERATE":
            utility = R/(1-w)
        elif player_two.strategy.name == "GT":
            utility = R/(1-w)
        elif player_two.strategy.name == "TFT":
            utility = R/(1-w)
        elif player_two.strategy.name == "TFTD":
            utility = S + w*T + w**2*P/(1-w)
        elif player_two.strategy.name == "TF2T":
            utility = R/(1-w)
        else:
            raise NotImplementedError

        return decision, utility


class TFT(Strategy):

    def __init__(self) -> None:
        """ Tit for Tat
        """
        self.name = "TFT"
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        # Check if a last move against this player existed and if yes, copy it, otherwise cooperate
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) == 0:
            decision = 0
        else:
            decision =  previous_games[-1].opponent_decision

        w = player_one.omega
        R = game_config["R"]
        S = game_config["S"]
        T = game_config["T"]
        P = game_config["P"]

        if player_two.strategy.name == "RANDOM":
            p = player_two.strategy.p
            utility = (w*p**3 + w*p**2*(R-T-S-2) + w*p*(1+T-R+2*S) + p*(R-S) + S - w*S)/(1-w)
        elif player_two.strategy.name == "DEFECT":
            utility = S + w*P/(1-w)
        elif player_two.strategy.name == "COOPERATE":
            utility = R/(1-w)
        elif player_two.strategy.name == "GT":
            utility = R/(1-w)
        elif player_two.strategy.name == "TFT":
            utility = R/(1-w)
        elif player_two.strategy.name == "TFTD":
            utility = (S + w*T)/(1-w**2)
        elif player_two.strategy.name == "TF2T":
            utility = R/(1-w)
        else:
            raise NotImplementedError

        return decision, utility
    
class TFTD(Strategy):

    def __init__(self) -> None:
        """ Tit for Tat Defect
        """
        self.name = "TFTD"
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        # Check if a last move against this player existed and if yes, copy it, otherwise defect
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) == 0:
            decision =  1
        else:
            decision =  previous_games[-1].opponent_decision

        w = player_one.omega
        R = game_config["R"]
        S = game_config["S"]
        T = game_config["T"]
        P = game_config["P"]

        if player_two.strategy.name == "RANDOM":
            p = player_two.strategy.p
            utility = (w*p**3 + w*p**2*(R-T-S-1) + w*p*S + p*(T+1-p))/(w-1)
        elif player_two.strategy.name == "DEFECT":
            utility = P*(1-w)
        elif player_two.strategy.name == "COOPERATE":
            utility = T + w*R*(1-w)
        elif player_two.strategy.name == "GT":
            utility = T + w*S + w**2*R/(1-w)
        elif player_two.strategy.name == "TFT":
            utility = (T+w*S)/(1-w**2)
        elif player_two.strategy.name == "TFTD":
            utility = P*(1-w)
        elif player_two.strategy.name == "TF2T":
            utility = T + w*R/(1-w)
        else:
            raise NotImplementedError

        return decision, utility


class TF2T(Strategy):

    def __init__(self) -> None:
        """ Tit for 2 Tats
        """
        self.name = "TF2T"
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        # Only defect if the last two moves of the opponent were to defect
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) < 2:
            decision =  0
        elif previous_games[-1].opponent_decision == 1 and previous_games[-2].opponent_decision == 1:
            decision =  1
        else:
            decision =  0

        w = player_one.omega
        R = game_config["R"]
        S = game_config["S"]
        T = game_config["T"]
        P = game_config["P"]
        
        if player_two.strategy.name == "RANDOM":
            p = player_two.strategy.p
            utility = (-1*w**2*p**4 + w**2*p**3*(3+S-R+T) + w**2*p**2*(-3-3*S+2*R-2*T) + w**2*p*(1+3*S) + p*(R-S) + w**2*p*(T-R) + S - w**2*S)/(1-w)
        elif player_two.strategy.name == "DEFECT":
            utility = S + w*S + w**2*P/(1-w)
        elif player_two.strategy.name == "COOPERATE":
            utility = S + w*S + w**2*P/(1-w)
        elif player_two.strategy.name == "GT":
            utility = R/(1-w)
        elif player_two.strategy.name == "TFT":
            utility = R/(1-w)
        elif player_two.strategy.name == "TFTD":
            utility = w*R/(1-w)
        elif player_two.strategy.name == "TF2T":
            utility = R/(1-w)
        else:
            raise NotImplementedError

        return decision, utility


# Additional strategies (no utility functions implemented for infinity game repetitions)

class GTFT(Strategy):

    def __init__(self) -> None:
        """ Generous Tit for Tat: Following a defection, it cooperates with 
            probability min{1-(T-R)/(R-S), (R-P)/(T-P)}.
        """
        self.name = "GTFT"
        self.p = 0
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        
        R = game_config["R"]
        S = game_config["S"]
        T = game_config["T"]
        P = game_config["P"]
        
        self.p = min([1-(T-R)/(R-S), (R-P)/(T-P)])
        
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) == 0:
            decision = 0
        else:
            if previous_games[-1].opponent_decision == 1:
                r = random()
                decision = int(r > self.p)
            else:
                decision = 0

        # utility not implemented
        utility = None

        return decision, utility


class ImpTFT(Strategy):

    def __init__(self, prob=0.95) -> None:
        """ Imperfect Tit for Tat: Imitates opponent's last move with high 
            (but less than one) probability.
        """
        self.name = "ImpTFT"
        self.p = prob
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) == 0:
            decision = 0
        else:
            r = random()
            if previous_games[-1].opponent_decision == 1:
                decision = int(r < self.p)
            else:
                decision = int(r > self.p)

        # utility not implemented
        utility = None

        return decision, utility


class TTFT(Strategy):

    def __init__(self) -> None:
        """ Two Tits for Tat: Defects twice after being defected against, otherwise cooperates.
        """
        self.name = "TTFT"
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        # Defect if one of the last two moves of the opponent were to defect
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) < 2:
            decision =  0
        elif previous_games[-1].opponent_decision == 1 or previous_games[-2].opponent_decision == 1:
            decision =  1
        else:
            decision =  0

        # utility not implemented
        utility = None

        return decision, utility
    

'''
class EARTHERLY(Strategy):

    def __init__(self) -> None:
        """ Eartherly: Keeps track of its partner's
            defection rate (the fraction of total turns its 
            partner has defected) so that after its partner defects,
            EATHERLY can defect with probability equal to its
            partner's defection rate.
        """
        self.name = "EARTHERLY"
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        # Defect if one of the last two moves of the opponent were to defect
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) < 1:
            decision =  0
        else:
            print(previous_games.opponent_decision)
            defection_prob = sum(previous_games[:].opponent_decision) / len(previous_games[:].opponent_decision)
            r = random()
            decision =  int(r < defection_prob)

        # utility not implemented
        utility = None

        return decision, utility
    
    
class CHAMPION(Strategy):

    def __init__(self, n_cooperation=10, n_TFT=10) -> None:
        """ Champion: Begins with a short period
            of unconditional cooperation, mirrors its partner's
            moves for another short period, and thereafter does
            the same as EATHERLY, except if its partner has
            cooperated more than 60% of the time then CHAMPION 
            cooperates even after its partner defects.
            
            n_cooperation: length of unconditional cooperation 
                period at the start
            n_TFT: lenght of the TFT period after the cooperation
                period
        """
        self.name = "CHAMPION"
        self.n_cooperation = n_cooperation
        self.n_TFT = n_TFT
        super().__init__()

    def make_move(self, player_one, player_two, game_config: Dict) -> Tuple[int, float]:
        # Defect if one of the last two moves of the opponent were to defect
        previous_games = player_one.history.game_list(player_two.id)
        if len(previous_games) <= self.n_cooperation:
            decision =  0
        elif self.n_cooperation < len(previous_games) <= self.n_cooperation + self.n_TFT:
            decision = previous_games[-1].opponent_decision
        else:
            defection_prob = sum(previous_games[:].opponent_decision) / len(previous_games[:].opponent_decision)
            if defection_prob < 0.4:
                decision = 0
            else:
                r = random()
                decision =  int(r < defection_prob)

        # utility not implemented
        utility = None

        return decision, utility
    
''' 

