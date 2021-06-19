from random import seed, random, sample
from typing import Dict, List, Tuple
from tqdm import tqdm, trange

import numpy as np
from Player import Player
from sortedcontainers import SortedDict

class Simulator:

    def __init__(self, grid_x: int, grid_y: int, 
                    num_players: int, play_window: int, travel_window: int, players, 
                    T:float , R: float, S: float, P: float,  rand_seed=42) -> None:
        """ Initializes the Simulator

        Args:
            grid_x (int): x dimension of the grid
            grid_y (int): y dimension of the grid
            num_players (int): Total number of players
            play_window (int): Size of the window in which players play against each other
            travel_window (int): Size of the window in which players travel
            players (List[PlayerCFG]): List of player configurations 
            T (float): T value
            R (float): R value
            S (float): S value
            P (float): P value
            rand_seed (int, optional): Random Seed. Defaults to 42.
        """

        
        # Fix seeds
        seed(rand_seed)
        np.random.seed(rand_seed)

        # Set basic variables
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.num_players = num_players
        self.play_window = play_window
        self.travel_window = travel_window
        self.values = {'T': T, 'R': R, 'S': S, 'P': P}
        self.wrap = True
        self.use_iterated_policy = False
        self.total_epoch = 0
        
        # We save the match-ups in a dict per player - This allows access in O(log(n)), and more importantly migration in O(log(n))
        # Match-ups are saved both ways and updated via the _update_location function
        self.match_ups = SortedDict({})

        # Setup the grid
        self.grid = np.zeros((grid_x, grid_y))
        assert self.grid_x * self.grid_y >= num_players, "Too many players for the grid-size"

        # Setup the payoff matrices
        # Format
        #       p2
        #       D    C
        # p1 D  P,P  T,S
        #    C  S,T  R,R
        #
        #
        self.p1_matrix = np.matrix([[P,T],[S,R]])
        self.p2_matrix = np.matrix([[P,S],[T,R]])

        # Get & Select the locations
        loc_idcs = [ (i,j) for i in range(grid_x) for j in range(grid_y)]   # Equally performant as Cartesian product
        select_locs = sample(loc_idcs, num_players)
        
        self.players = []      
        
        for idx, p_cfg in enumerate(players):
            p_id = idx + 1  # We use this one-time offset to get player ids starting at 1. This allows to use 0 as an empty cell
            player = Player(p_id, p_cfg["class"], select_locs[idx], 0, p_cfg["play_window"], p_cfg["migrate_window"], 
                             p_cfg["imit_prob"], p_cfg["migrate_prob"], 
                             self, p_cfg["strategy"], p_cfg["omega"])

            self.match_ups[p_id] = []
            self.players.append(player)
            self._update_location(True, select_locs[idx], p_id)

        # Setup policies
        self.migration_order_policy = lambda x: x   # Identity migration

        print("Created Simulator")

    def _update_location(self, take: int, loc, id: int = None):
        """ Updates a location on the grid based on whether it is taken or not.
            It automatically registers the location with the players in the region 
            Runtime: O(log(n))
        Args:
            take (int): 0 if the location is now free, 1 in case the location is now taken
            loc ([type]): 
        """

        if self.wrap:
            x_l, x_h = loc[0]-self.play_window, loc[0]+self.play_window
            y_l, y_h = loc[1]-self.play_window, loc[1]+self.play_window
        else:
            x_l, x_h = max(0, loc[0]-self.play_window), min(self.grid_x, loc[0]+self.play_window)
            y_l, y_h = max(0, loc[1]-self.play_window), min(self.grid_y, loc[1]+self.play_window)

        if take:
            assert self.grid[loc] == 0  
            # We're new at this location, we have to 
            # 1. Register ourselves with everyone around this location
            for x in range(x_l, x_h+1):
                for y in range(y_l, y_h+1):
                    x_mod, y_mod = x % self.grid_x, y % self.grid_y

                    if (x_mod,y_mod) != loc and self.grid[x_mod,y_mod] != 0:
                        # Found a match-up
                        self.match_ups[int(self.grid[x_mod,y_mod])].append(id)
                        self.match_ups[id].append(int(self.grid[x_mod,y_mod]))

                        # TODO append to play_neighbourhood
                        self.players[id-1].play_neighbourhood.append(int(self.grid[x_mod,y_mod]))
                        self.players[int(self.grid[x_mod,y_mod])-1].play_neighbourhood.append(id)

            # 2. Update the grid state
            self.grid[loc] = id
        else:
            assert self.grid[loc] == id
            # We're leaving this location, we have to 
            # 1. We remove ourselves from this location
            for x in range(x_l, x_h+1):
                for y in range(y_l, y_h+1):
                    x_mod, y_mod = x % self.grid_x, y % self.grid_y
                    if (x_mod,y_mod) != loc and self.grid[x_mod,y_mod] != 0:
                        # Found a match-up
                        self.match_ups[int(self.grid[x_mod,y_mod])] = list(filter(lambda x: x != id, self.match_ups[int(self.grid[x_mod,y_mod])]))

                        # TODO Remove ourselves from other players
                        self.players[int(self.grid[x_mod,y_mod])-1].play_neighbourhood = list(filter(lambda x: x != id, self.players[int(self.grid[x_mod,y_mod])-1].play_neighbourhood))

            # TODO Reset neighbour list
            self.players[id-1].play_neighbourhood = []

            self.match_ups[id] = [] # Can reset ourselves

            # 2. Update the grid state
            self.grid[self.players[id-1].loc] = 0

    def simulate(self, epochs: int, visualize: bool = False):
        past_states = None  # For book-keeping
        #t = tqdm(range(epochs), position=0, leave=True)
        t = range(epochs)
        for i in t:
            self.step(self.total_epoch)
            self.total_epoch += 1
            # TODO Update bookkeeping here

            if visualize:
                tqdm.write(str(self.grid)+"\n")
                #t.set_description(str(self.grid)+"\n", refresh=True)


    def step(self, epoch: int):
        """ Simulates a single epoch step by 
            0. Reset players (wrt. to single step metrics)
            1. Playing
            2. Letting players communicate
            3. Letting players imitate
            4. Letting players migrate
        """
        # TODO Nothing to reset atm
        self.reset(epoch)
        self.play(epoch)
        self.player_comm()
        self.imitate(epoch)
        self.migrate(epoch)
    
    def global_update(self):
        """ This function applies global behaviour to all players. It could i.e. be used to simulate the "harshness" of an environment
        """
        pass

    def player_comm(self):
        """ This function would allow players to communicate after a round.
        """
        pass

    def migrate(self, epoch: int):
        """ This function triggers the migration behaviour of the players 
        """
        ordered_players = self.migration_order_policy(self.players)

        for p in ordered_players:
            p.migrate()

    def imitate(self, epoch: int):
        """ This function triggers the imitation behaviour of the players 
        """
        # ordered_players = self.migration_order_policy(self.players)

        for p in self.players:
            p.imitate()

    def play(self, epoch):
        """ Play all matchups and update the state accordingly
        """
        games_played = 0
        for k, v in self.match_ups.items():
            for p2 in v:
                if k < p2:  # We only need match-ups once and we're symmetric
                    player_one = self.players[k-1]
                    player_two = self.players[p2-1]

                    if self.use_iterated_policy:  # We used an iterated policy which directly returns the values
                        p1_dec, p1_util  = player_one.make_move(player_two, self.values)
                        p2_dec, p2_util  = player_two.make_move(player_one, self.values)
                    else: # We used a step policy and can look_up the values from the matrix
                        p1_dec, _  = player_one.make_move(player_two, self.values)
                        p2_dec, _  = player_two.make_move(player_one, self.values)
                        p1_util = self.p1_matrix[p1_dec, p2_dec]
                        p2_util = self.p2_matrix[p1_dec, p2_dec]

                    #print(p1_util)
                    # Update players
                    player_one.latest_util += p1_util
                    player_two.latest_util += p2_util

                    player_one.total_util += p1_util
                    player_two.total_util += p2_util

                    games_played += 1

                    #add to histories
                    player_one.add_to_history(epoch, player_two.id, player_two.player_class, p1_dec, p2_dec, player_one.strategy.name, player_two.strategy.name, p1_util, p2_util, {})
                    player_two.add_to_history(epoch, player_one.id, player_one.player_class, p2_dec, p1_dec, player_two.strategy.name, player_one.strategy.name, p2_util, p1_util, {})

        
        #print(f"Total games: {games_played}")

    def sub_grid_play(self, p:Player, loc: Tuple[int,int]) -> float:
        """ Returns the outcome if the player p would play at position location now

        Args:
            new_loc (Tuple[int, int]): Location to play from 

        Returns:
            float: utility at this location
        """
        player_one = p

        # New Grid
        if self.wrap:
            x_l, x_h = loc[0]-self.play_window, loc[0]+self.play_window
            y_l, y_h = loc[1]-self.play_window, loc[1]+self.play_window
        else:
            x_l, x_h = max(0, loc[0]-self.play_window), min(self.grid_x, loc[0]+self.play_window)
            y_l, y_h = max(0, loc[1]-self.play_window), min(self.grid_y, loc[1]+self.play_window)
        # New neighbours
        neighs: List[Player] = []
        for x in range(x_l, x_h+1):
                for y in range(y_l, y_h+1):
                    x_mod, y_mod = x % self.grid_x, y % self.grid_y

                    if (x_mod, y_mod) != loc and self.grid[x_mod, y_mod] != 0:
                        neighs.append(self.players[int(self.grid[x_mod, y_mod])-1])

        util = 0.0
        for neigh in neighs:
            if self.use_iterated_policy:  # We used an iterated policy which directly returns the values
                p1_dec, p1_util  = player_one.make_move(neigh, self.values)
            else: # We used a step policy and can look_up the values from the matrix
                p1_dec, _  = player_one.make_move(neigh, self.values)
                p2_dec, _  = neigh.make_move(player_one, self.values)
                p1_util = self.p1_matrix[p1_dec, p2_dec]
            # Don't append to history
            util += p1_util

        return util

    def reset(self, epoch: int):
        for p in self.players:
            p._reset()

    def get_state(self) -> Dict:
        """ Returns the entire history of a played matches

        Returns:
            Dict: (player_id, player_history)
        """

        hist_dict = { }
        for i, player in enumerate(self.players):
            hist_dict[i+1] = player.history
        
        return hist_dict

    def get_flat_mapped_grid(self):
        # Prepare the ouput 
        def grid_map(x):
            if x == 0:
                return x
            else:
                return self.players[int(x)-1].strategy.name
        
        list_2d = self.grid.flatten().tolist()
        return map(grid_map, list_2d)