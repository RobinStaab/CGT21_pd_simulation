from Simulator import Simulator
from Player import Player
from Strategies import *

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
    grid_x          = 10
    grid_y          = 10
    num_players     = 100
    play_window     = 1
    migrate_window  = 3
    imit_prob       = 0.8
    migrate_prob    = 0.8
    
    player_cfgs = generate_players("random", 100, 1, 3, 0.8, 0.8)

    sim = Simulator(grid_x, grid_y, num_players, play_window, migrate_window, player_cfgs, T, R, S, P)

    sim.simulate(50, visualize=True)