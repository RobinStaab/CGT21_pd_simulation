import numpy as np
import math
import pandas as pd


def r_up(val, base):
    return base * math.ceil(val/base)

def defection_per_class_over_time(history, classes, min_epoch=-1, max_epoch=-1, agg_step=1):
    """ Returns a dict with the defection rate per class over time and overall


    Args:
        history ([type]): [description]
        aggregation_step ([type]): [description]

    Returns:
        [type]: dict with total values and per-epoch values
    """

    def defection_map(d, player_entry):
        for encounter in player_entry.history.values():
            for game in encounter:
                act_epoch = r_up(game.epoch, agg_step)
                if d.get(act_epoch) == None:
                    d[act_epoch] = { 0: dict([(name, 0) for name in classes]),
                                     1: dict([(name, 0) for name in classes]) }

                    
                d[act_epoch][game.player_decision][game.player_strategy] += 1
                d['total'][game.player_decision][game.player_strategy] += 1


    summary_dict = {}
    summary_dict["total"] = {
        0: dict([(name, 0) for name in classes]),
        1: dict([(name, 0) for name in classes])
    }
    
    
    for player in history.values():
        defection_map(summary_dict, player)

    # Here the dict is complete

    return summary_dict, pd.DataFrame.from_dict({(i,j): summary_dict[i][j] for i in summary_dict.keys() for j in summary_dict[i].keys()}, orient='index')

def class_distribution_over_time(graph_history, classes, min_epoch=-1, max_epoch=-1, agg_step=1):

    def cd_map(d, player_entry):
        for state in graph_history.grid:
            act_epoch = r_up(state.epoch, agg_step)
            if d.get(act_epoch) == None:
                d[act_epoch] = dict([(name, 0) for name in classes])
            for entry in state:
                d[act_epoch][entry] += 1


    summary_dict = {}
    summary_dict["total"] = dict([(name, 0) for name in classes])
    
    for entry in graph_history:
        cd_map(summary_dict, entry)

    return summary_dict

def class_vs_class_over_time(history, classes, agg_step=1):
    """ Returns a dict containing the behaviour of each class vs each class at every-point in time

    Args:
        history ([type]): [description]

    Returns:
        [dict]: Order: Time-step, Strat-1, Strat-2, 0: Coop, 1: Defect 
    """
    def c_vs_c_map(d, player_entry):
        for encounter in player_entry.history.values():
            for game in encounter:
                act_epoch = r_up(game.epoch, agg_step)
                if d.get(act_epoch) == None:
                    d[act_epoch] = { }
                if d[act_epoch].get(game.player_strategy) == None:
                    d[act_epoch][game.player_strategy] = { }
                if d[act_epoch][game.player_strategy].get(game.other_strategy) == None:
                    d[act_epoch][game.player_strategy][game.other_strategy] = { 0: 0,
                                                                                1: 0,}

                d[act_epoch][game.player_strategy][game.other_strategy][game.player_decision] += 1
                d['total'][game.player_strategy][game.other_strategy][game.player_decision] += 1

    summary_dict = {}
    summary_dict["total"] = dict([(name, dict([(name, { 0: 0, 1: 0,}) for name in classes])) for name in classes])
    
    for player in history.values():
        c_vs_c_map(summary_dict, player)

    #df = pd.DataFrame.from_dict({((i,j),k): summary_dict[i][j][k] for i in summary_dict.keys() for j in summary_dict[i].keys() for k in summary_dict[i][j].keys()}, orient='index')

    return summary_dict

def payoff_per_class_over_time(history, classes, agg_step=1):
    """ Returns a dict containing the average payoff for each class at every-point in time

    Args:
        history ([type]): [description]
        aggregation_step (int, optional): [description]. Defaults to 1.

    Returns:
        [type]: [description]
    """

    def poc_map(d, player_entry):
        for encounter in player_entry.history.values():
            for game in encounter:
                act_epoch = r_up(game.epoch, agg_step)
                if d.get(act_epoch) == None:
                    d[act_epoch] = { 'pay_off': dict([(name, 0) for name in classes]),
                                     'num_of_players': dict([(name, 0) for name in classes]) }

                    
                d[act_epoch]['pay_off'][game.player_strategy] += game.player_util
                d[act_epoch]['num_of_players'][game.player_strategy] += 1

                d['total']['pay_off'][game.player_strategy] += game.player_util
                d['total']['num_of_players'][game.player_strategy] += 1


    summary_dict = {}
    summary_dict["total"] = { 'pay_off': dict([(name, 0) for name in classes]),
                              'num_of_players': dict([(name, 0) for name in classes]) }
    
    
    for player in history.values():
        poc_map(summary_dict, player)

    df = pd.DataFrame.from_dict({(i,j): summary_dict[i][j] for i in summary_dict.keys() for j in summary_dict[i].keys()}, orient='index')

    return summary_dict, df

def percentage_of_optimum(history, classes, agg_step=1):
    """ Returns the percentage of the peak overall utility that we could have achieved

    Args:
        history ([type]): [description]
        aggregation_step (int, optional): [description]. Defaults to 1.

    Returns:
        [type]: Note that the number of matches has not been divided by 2
    """

    def poo_map(d, player_entry):
            for encounter in player_entry.history.values():
                for game in encounter:
                    act_epoch = r_up(game.epoch, agg_step)
                    if d.get(act_epoch) == None:
                        d[act_epoch] = { 'pay_off': 0,
                                        'num_of_matches': 0 }

                    # TODO FIX for the correct util
                    d[act_epoch]['pay_off'] += game.player_util
                    d[act_epoch]['num_of_matches'] += 1

                    d['total']['pay_off'] += game.player_util
                    d['total']['num_of_matches'] += 1


    summary_dict = {}
    summary_dict["total"] = { 'pay_off': 0,
                              'num_of_matches': 0 }


    for player in history.values():
        poo_map(summary_dict, player)

    df = pd.DataFrame.from_dict(summary_dict, orient='index')

    return summary_dict, df

def class_change_over_time(history, classes, agg_step=1):
    raise NotImplementedError