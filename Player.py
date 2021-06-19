from typing import List
from Strategies import *
from random import random
from History import History
from Game_data import Game_data

class Player:

    def __init__(self, id: int, loc, init_util: float, 
                    play_window: int, migrate_window: int, 
                    imit_prob: float, migrate_prob: float,
                    sim_state, strategy: Strategy, omega:float) -> None:
        """Base player model

        Args:
            id (int): Unique identifier of the player
            loc ([type]): Current location of the player on the game grid
            init_util (float): Initial utility that the player has
            play_window (int): Size of the 2-D window in which the player plays against other players - For performance we should keep this equal in all cases
            migrate_window (int): Size of the 2-D window in which the player might migrate - For performance we should keep this equal in all cases
            imit_prob (float): Probability with which a player may imitate the most successful player in his area
            migrate_prob (float): Probability with which a player may migrate (if at all) - Can generalize this to a prob. dist over migrate_window
            sim_state: (Simulator): Reference to the Simulator to get access to other players
            strategy (Strategy): Strategy that this player follows
            omega (float): Shadow of the future
        """
        self.id     = id
        self.loc    = loc
        self.total_util     = init_util
        self.play_window    = play_window
        self.migrate_window = migrate_window
        self.imit_prob      = imit_prob
        self.migrate_prob   = migrate_prob
        self.sim_state      = sim_state
        self.strategy       = strategy
        self.alive          = True
        self.history        = History()
        self.omega          = omega
        
        # How much utility we gained last round 
        self.latest_util = 0

        # List of players ID's in our neighbourhood
        self.play_neighbourhood: List[int] = []

        # List of tuples containing the potential locations that we can travel to
        self.migrate_neighbourhood: List = []

    def imitate(self) -> None:
        """Imitates the most successfully strategy in the window.
        """
        r = random()
        if r < self.imit_prob:
            # We imitate the most succesfull player in the neighbourhood
            new_strategy = self.strategy
            best_util = self.latest_util
            for n_id in self.play_neighbourhood:    # TODO
                if self.sim_state.players[n_id-1].latest_util > best_util:
                    best_util = self.sim_state.players[n_id-1].latest_util
                    new_strategy = self.sim_state.players[n_id-1].strategy

            # TODO Could do some history changes here

            self.strategy = new_strategy

    def migrate(self) -> None:
        """Migrates to the free square with the best expected payoff 
        """
        # TODO Do we really always want to do this? Could implement custom migration policies here
        r = random()
        if r < self.migrate_prob:
            # We migrate if we find a better spot

            if self.sim_state.wrap:
                x_l, x_h = self.loc[0]-self.migrate_window, self.loc[0]+self.migrate_window
                y_l, y_h = self.loc[1]-self.migrate_window, self.loc[1]+self.migrate_window
            else:
                x_l, x_h = max(0, self.loc[0]-self.migrate_window), min(self.grid_x, self.loc[0]+self.migrate_window)
                y_l, y_h = max(0, self.loc[1]-self.migrate_window), min(self.grid_y, self.loc[1]+self.migrate_window)


            best_loc    = self.loc
            best_util   = self.latest_util
            # NOTE This could be updated on fly - but this is constant time overhead
            migrate_neighbourhood = [(x % self.sim_state.grid_x, y % self.sim_state.grid_y) for x in range(x_l, x_h+1) for y in range(y_l, y_h+1) if self.sim_state.grid[(x % self.sim_state.grid_x, y % self.sim_state.grid_y)] == 0]
            for f_loc in migrate_neighbourhood:
                # How high would our payoff be here
                new_util = self.sim_state.sub_grid_play(self, f_loc)
                if new_util > best_util:
                    best_util = new_util
                    best_loc  = f_loc

            # Actual migration
            if self.loc != best_loc:
                # NOTE Important to keep this order as otherwise matchups will be lost
                self.sim_state._update_location(False, self.loc, self.id)
                self.sim_state._update_location(True, best_loc, self.id)
                self.loc = best_loc

    def make_move(self, player_two, game_config: Dict) -> Tuple[int, float]:
        return self.strategy.make_move(self, player_two, game_config)

    def _reset(self):
        """In case we want to reset something for a single player, we can do it here
        """
        self.latest_util = 0

    def add_to_history(self, epoch, opponent_id, player_decision, opponent_decision, player_strategy, other_strategy, opponent_util, data_dict):
        """Player adds game to history
        
            Args:
            epoch (int)             : epoch of the game
            other_id (int)          : id of the opponent
            player_decision (0/1)   : decision of the player
            other_decision (0/1)    : decision of the opponent
            player_strategy         : strategy the player is currently following
            other_strategy          : strategy the other player is currently following
            other_util (float)      : utility of the opponent
            data_dict               : additional data dictionary
        """
        self.history.add_game(Game_data(epoch, self.id, opponent_id, player_decision, opponent_decision, player_strategy, other_strategy, self.latest_util, opponent_util, data_dict))