from Simulator import Simulator
from Player import Player
from Strategies import *
import time


def generate_players(strategy: str, amount: int, play_window: int, migrate_window: int, imit_prob: float, migrate_prob: float):
    
    strategy_obj = None
    if strategy == "random":
        strategy_obj = Random(0.5)
    elif strategy == "TFT":
        strategy_obj = TFT()
    else:
        assert False, "Unkown strategy type"

    player_cfgs = []

    for i in range(amount):
        player_cfgs.append({
            "play_window": play_window,
            "migrate_window": migrate_window,
            "imit_prob": imit_prob,
            "migrate_prob": migrate_prob,
            "strategy": strategy_obj
        })

    return player_cfgs

if __name__ == "__main__":
    
    # T > R > P > S
    T = 1.5
    R = 1
    S = 0.5
    P = 0.8
    grid_x          = 20
    grid_y          = 20
    num_players     = 300
    play_window     = 1
    migrate_window  = 3
    imit_prob       = 0.8
    migrate_prob    = 0.8
    epochs          = 100
    
    player_cfgs = generate_players("random", num_players, play_window, migrate_window, imit_prob, migrate_prob)

    sim = Simulator(grid_x, grid_y, num_players, play_window, migrate_window, player_cfgs, T, R, S, P)

   
    for i in range(10):
        start_time = time.time()
        sim.simulate(epochs, visualize=False)
        print(f"Time: {(time.time() - start_time)}")

    print(f"Total Time for {epochs} epochs, {num_players} players and grid-size {grid_x} x {grid_y}: {(time.time() - start_time)}")