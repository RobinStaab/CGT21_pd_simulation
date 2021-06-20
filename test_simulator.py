from typing import Dict, List, Tuple
from Simulator import Simulator
from Player import Player
from Strategies import *
import time
from analysis import *
import pandas as pd


def generate_player(strategy: Strategy, player_class: str, play_window: int, migrate_window: int, imit_prob: float, migrate_prob: float, omega: float):
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
    elif strategy == "GTFT":
        strategy_obj = GTFT()
    elif strategy == "ImpTFT":
        strategy_obj = ImpTFT()
    elif strategy == "TTFT":
        strategy_obj = TTFT()
    elif strategy == "EARTHERLY":
        strategy_obj = EARTHERLY()
    elif strategy == "CHAMPION":
        strategy_obj = CHAMPION()
    else:
        assert False, "Unkown strategy type"

    return {
        "class": player_class,
        "play_window": play_window,
        "migrate_window": migrate_window,
        "imit_prob": imit_prob,
        "migrate_prob": migrate_prob,
        "strategy": strategy_obj,
        "omega": omega
    }


def generate_simple_players(strategies: List[str], amount: List[int], play_window: int, migrate_window: int, imit_prob: float, migrate_prob: float, omega: float):
    player_cfgs = []
    assert len(strategies) == len(amount)
    for amount, strategy in zip(amount, strategies):
        for i in range(amount):
            player_cfgs.append(generate_player(
                strategy, strategy, play_window, migrate_window, imit_prob, migrate_prob, omega))

    return player_cfgs


if __name__ == "__main__":

    # T > R > P > S
    T = 1.7
    R = 1.5
    S = 0.5
    P = 0.5
    grid_x = 10
    grid_y = 10
    num_players = 100
    play_window = 1
    migrate_window = 3
    imit_prob = 0.8
    migrate_prob = 0.8
    epochs = 100
    omega = 0.5

    # player_cfgs = generate_players(["GTFT","ImpTFT","TTFT","EARTHERLY","CHAMPION"],
    #                                 [40, 10, 10, 20, 20], play_window, migrate_window, imit_prob, migrate_prob, omega)

    player_cfgs = generate_simple_players(["RANDOM", "DEFECT", "COOPERATE", "GT", "TFT", "TFTD", "TF2T"],
                                          [30, 10, 10, 10, 10, 10, 10], play_window, migrate_window, imit_prob, migrate_prob, omega)

    sim = Simulator(grid_x, grid_y, num_players, play_window,
                    migrate_window, player_cfgs, T, R, S, P)

    for i in range(10):
        start_time = time.time()
        sim.simulate(epochs, visualize=False)
        t, df_dpcot = defection_per_class_over_time(sim.get_state(), ["RANDOM", "DEFECT", "COOPERATE", "GT", "TFT", "TFTD", "TF2T"])

        # TODO requires grid history in the simulator
        #t2 = class_distribution_over_time(sim.get_flat_mapped_grid(), ["RANDOM","DEFECT","COOPERATE","GT","TFT","TFTD","TF2T"] )

        t3 = class_vs_class_over_time(sim.get_state(), ["RANDOM", "DEFECT", "COOPERATE", "GT", "TFT", "TFTD", "TF2T"])
        t4, df_ppcot = payoff_per_class_over_time(sim.get_state(), ["RANDOM", "DEFECT", "COOPERATE", "GT", "TFT", "TFTD", "TF2T"])
        t5 = percentage_of_optimum(sim.get_state(), ["RANDOM", "DEFECT", "COOPERATE", "GT", "TFT", "TFTD", "TF2T"])
        
        #t6 = class_change_over_time
        print(f"Time: {(time.time() - start_time)}")
        pd 
    print(
        f"Total Time for {epochs} epochs, {num_players} players and grid-size {grid_x} x {grid_y}: {(time.time() - start_time)}")
