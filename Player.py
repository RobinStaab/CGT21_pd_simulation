from typing import List
from Strategies import *
from Simulator import Simulator
from random import random

class Player:

    def __init__(self, id: int, loc, init_util: float, 
                    play_window: int, migrate_window: int, 
                    imit_prob: float, migrate_prob: float,
                    sim_state: Simulator, strategy: Strategy) -> None:
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
        """
        self.id = id
        self.loc = loc
        self.init_util = init_util
        self.play_window = play_window
        self.migrate_window = migrate_window
        self.imit_prob = imit_prob
        self.migrate_prob = migrate_prob
        self.sim_state = sim_state
        self.strategy = strategy
        self.alive = True
        
        # How much utility we gained last round 
        self.latest_util = 0

        # List of players ID's in our neighbourhood
        self.play_neighbourhood: List[int]

        # List of tuples containing the potential locations that we can travel to
        self.migrate_neighbourhood: List

    def imitate(self) -> None:
        """Imitates the most successfully strategy in the window.
        """
        r = random()
        if r < self.imit_prob:
            # We imitate the most succesfull player in the neighbourhood
            new_strategy = self.strategy
            best_util = self.latest_util
            for n_id in self.play_neighbourhood:
                if self.sim_state.players[id].latest_util > best_util:
                    best_util = self.sim_state.players[id].latest_util
                    new_strategy = self.sim_state.players[id].strategy

            self.strategy = new_strategy

    def migrate(self) -> None:
        """Migrates to the free square with the best expected payoff 
        """
        # TODO Do we really always want to do this? Could implement custom 
        r = random()
        if r < self.migrate_prob:
            # We migrate if we find a better spot
            best_loc    = self.loc
            best_util   = self.latest_util
            for f_loc in self.migrate_neighbourhood:
                # How high would our payoff be here
                new_util = self.sim_state.sub_grid_play(self, f_loc)
                if new_util > best_util:
                    best_util = new_util
                    best_loc  = f_loc

            # Actual migration
            if self.loc != best_loc:
                # NOTE Important to keep this order as otherwise matchups will be lost
                self.sim_state._update_location(False, self.loc)
                self.sim_state._update_location(True, f_loc, self.id)
                self.loc = f_loc

    def _reset(self):
        """In case we want to reset something for a single player, we can do it here
        """