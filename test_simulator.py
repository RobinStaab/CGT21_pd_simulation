from typing import Dict, List, Tuple
from Simulator import Simulator
from Player import Player
from Strategies import *
import time


def generate_players(strategies: List[str], amount: List[int], play_window: int, migrate_window: int, imit_prob: float, migrate_prob: float, omega: float):
    player_cfgs = []

    assert len(strategies) == len(amount)

    for amount, strategy in zip(amount, strategies):
        for i in range(amount):
            strategy_obj = None
            if strategy == "RANDOM":
                strategy_obj = RANDOM(0.5)
            elif strategy == "DEFECT":
                strategy_obj = DEFECT()
            elif strategy == "COOPERATE":
                strategy_obj = COOPERATE()
            elif strategy == "GT":
                strategy_obj = GT()
            elif strategy == "TFT":
                strategy_obj = TFT()
            elif strategy == "TFTD":
                strategy_obj = TFTD()
            elif strategy == "TF2T":
                strategy_obj = TF2T()
            else:
                assert False, "Unkown strategy type"
            
            player_cfgs.append({
                "play_window": play_window,
                "migrate_window": migrate_window,
                "imit_prob": imit_prob,
                "migrate_prob": migrate_prob,
                "strategy": strategy_obj,
                "omega": omega
            })

    return player_cfgs

if __name__ == "__main__":
    
    # T > R > P > S
    T = 1.5
    R = 1
    S = 0.5
    P = 0.8
    grid_x          = 10
    grid_y          = 10
    num_players     = 100
    play_window     = 1
    migrate_window  = 3
    imit_prob       = 0.8
    migrate_prob    = 0.8
    epochs          = 100
    omega          = 0.5
    
    player_cfgs = generate_players(["RANDOM","DEFECT","COOPERATE","GT","TFT","TFTD","TF2T"], 
                                    [40, 10, 10, 10, 10, 10, 10], play_window, migrate_window, imit_prob, migrate_prob, omega)

    sim = Simulator(grid_x, grid_y, num_players, play_window, migrate_window, player_cfgs, T, R, S, P)

   
    for i in range(10):
        start_time = time.time()
        sim.simulate(epochs, visualize=False)
        print(f"Time: {(time.time() - start_time)}")

    print(f"Total Time for {epochs} epochs, {num_players} players and grid-size {grid_x} x {grid_y}: {(time.time() - start_time)}")