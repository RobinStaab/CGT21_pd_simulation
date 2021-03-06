import numpy as np
import math
import pandas as pd
import plotly.express as px
import plotly.colors as co
import plotly.figure_factory as ff
from collections import Counter

Strategies = {'RANDOM': 1, 'DEFECT': 2, 'COOPERATE': 3,
              'GT': 4, 'TFT': 5, 'TFTD': 6, 'TF2T': 7}

rStrategies = {0: 'EMPTY', 1: 'RANDOM', 2: 'DEFECT',
               3: 'COOPERATE', 4: 'GT', 5: 'TFT', 6: 'TFTD', 7: 'TF2T'}

fix_colorscale = {'EMPTY': '#BEBEBE', 'RANDOM': '#19D3F3', 'DEFECT': '#EF553B', 'COOPERATE': '#00CC96',
                  'GT': '#FFA15A', 'TFT': '#AB63FA', 'TFTD': '#FF6692', 'TF2T': '#B6E880'}


def r_up(val, base):
    return base * math.ceil(val/base)


def vis_dpc(dff):
    df_red = dff.drop('total', axis=1).sort_index(axis=1).transpose()
    ff = list(filter(lambda x: x in list(Strategies.keys()), df_red.keys().to_list()))
    #print(f"ff: {ff} , strat:{Strategies}", flush=True)
    ff.sort(key=Strategies.get)
    return px.line(df_red, y=ff, title='Defection rate per class over time', labels={"index": "epoch", "value": "Defection rate"}, color_discrete_map=fix_colorscale)


def defection_per_class_over_time(history, classes, min_epoch=-1, max_epoch=-1, agg_step=1, visualize=False):
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
                    d[act_epoch] = {0: dict([(name, 0) for name in classes]),
                                    1: dict([(name, 0) for name in classes])}

                d[act_epoch][game.player_decision][game.player_strategy] += 1
                d['total'][game.player_decision][game.player_strategy] += 1

    summary_dict = {}
    summary_dict["total"] = {
        0: dict([(name, 0) for name in classes]),
        1: dict([(name, 0) for name in classes])
    }

    for player in history.values():
        defection_map(summary_dict, player)

    final_dict = {}
    for epoch, e_state in summary_dict.items():
        final_dict[epoch] = {}
        for beh, cls in e_state.items():
            if beh == 0:
                for name, val in cls.items():
                    if val + e_state[1][name] > 0:
                        final_dict[epoch][name] = e_state[1][name] / \
                            (val + e_state[1][name])
                    else:
                        final_dict[epoch][name] = None

    # Here the dict is complete
    #df = pd.DataFrame.from_dict({(i,j): summary_dict[i][j] for i in summary_dict.keys() for j in summary_dict[i].keys()}, orient='index')
    dff = pd.DataFrame.from_dict(final_dict)

    fig = None
    if visualize:
        fig = vis_dpc(dff)
        # fig.show()
    return summary_dict, dff, fig


def vis_cd(df):
    df = df.transpose()
    mid = df['EMPTY']
    df.drop(labels=['EMPTY'], axis=1, inplace=True)
    # df.insert(0, 'EMPTY', mid)
    ff = df.keys().to_list()
    ff.sort(key=Strategies.get)
    # colorscale = [[strat, fix_colorscale[strat]] for strat in ff]
    # if colors is not None:
    return px.bar(df, y=ff, title='Class Distribution over time', labels={"index": "epoch", "value": "Class Distribution"}, color_discrete_map=fix_colorscale)
    # else:
    #return px.bar(df, y=ff, title='Class Distribution over time for ?? = 0.4', labels={"index": "epoch", "value": "Class Distribution"}, color_discrete_map=fix_colorscale)


def class_distribution_over_time(graph_history, classes, step_size=1, visualize=False):

    def cd_map(d, player_entry):
        for state in graph_history.grid:
            act_epoch = r_up(state.epoch, agg_step)
            if d.get(act_epoch) == None:
                d[act_epoch] = dict([(name, 0) for name in classes])
            for entry in state:
                d[act_epoch][entry] += 1

    summary_dict = {}

    for i, entry in enumerate(graph_history):
        index = step_size * i
        summary_dict[index] = dict(Counter(entry))

    df = pd.DataFrame.from_dict(summary_dict).fillna(0.0)

    fig = None
    if visualize:
        fig = vis_cd(df)
        # fig.show()
    return summary_dict, df, fig


def vis_cvc(df):
    df2 = (df[1] / (df[0]+df[1])).round(2)

    plotly_dict = {'z': df2.values.tolist(),
                   'x': df2.index.get_level_values(0).unique(),
                   'y': df2.index.get_level_values(0).unique()}

    # Reshape
    use_z = np.array(plotly_dict['z']).reshape(
        (len(plotly_dict['x']), len(plotly_dict['y'])))
    return ff.create_annotated_heatmap(use_z, x=list(plotly_dict['x']), y=list(plotly_dict['y']), colorscale="tealrose")


def class_vs_class_over_time(history, classes, agg_step=1, visualize=True):
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
                    d[act_epoch] = {}
                if d[act_epoch].get(game.player_strategy) == None:
                    d[act_epoch][game.player_strategy] = {}
                if d[act_epoch][game.player_strategy].get(game.other_strategy) == None:
                    d[act_epoch][game.player_strategy][game.other_strategy] = {0: 0,
                                                                               1: 0, }

                d[act_epoch][game.player_strategy][game.other_strategy][game.player_decision] += 1
                d['total'][game.player_strategy][game.other_strategy][game.player_decision] += 1

    summary_dict = {}
    summary_dict["total"] = dict(
        [(name, dict([(name, {0: 0, 1: 0, }) for name in classes])) for name in classes])

    for player in history.values():
        c_vs_c_map(summary_dict, player)

    df = pd.DataFrame.from_dict({(i, j): summary_dict['total'][i][j] for i in summary_dict['total'].keys(
    ) for j in summary_dict['total'][i].keys()}, orient='index')
    # Dict is done here
    fig = None
    if visualize:
        fig = vis_cvc(df)
        # fig.show()
    return summary_dict, df, fig


def vis_ppc(dff):
    df_red = dff.drop('total', axis=1).sort_index(axis=1).transpose()
    ff = list(filter(lambda x: x in list(Strategies.keys()), df_red.keys().to_list()))
    #print(f"ff: {ff} , strat:{Strategies}", flush=True)
    ff.sort(key=Strategies.get)
    return px.line(df_red, y=ff, title='Average payoff per class over time', labels={"index": "epoch", "value": "Avg. payoff"}, color_discrete_map=fix_colorscale)


def payoff_per_class_over_time(history, classes, agg_step=1, visualize=True):
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
                    d[act_epoch] = {'pay_off': dict([(name, 0) for name in classes]),
                                    'num_of_players': dict([(name, 0) for name in classes])}

                d[act_epoch]['pay_off'][game.player_strategy] += game.player_util
                d[act_epoch]['num_of_players'][game.player_strategy] += 1

                d['total']['pay_off'][game.player_strategy] += game.player_util
                d['total']['num_of_players'][game.player_strategy] += 1

    summary_dict = {}
    summary_dict["total"] = {'pay_off': dict([(name, 0) for name in classes]),
                             'num_of_players': dict([(name, 0) for name in classes])}

    for player in history.values():
        poc_map(summary_dict, player)

    final_dict = {}
    for key, itm in summary_dict.items():
        final_dict[key] = {}
        for ty, rel in itm.items():
            if ty == "pay_off":
                for cl, val in rel.items():
                    if itm['num_of_players'][cl] > 0:
                        final_dict[key][cl] = val / itm['num_of_players'][cl]
                    else:
                        final_dict[key][cl] = None

    # Dict is done here
    #df = pd.DataFrame.from_dict({(i,j): summary_dict[i][j] for i in summary_dict.keys() for j in summary_dict[i].keys()}, orient='index')
    dff = pd.DataFrame.from_dict(final_dict)
    # Dataframe is done here
    fig = None
    if visualize:
        fig = vis_ppc(dff)
        # fig.show()
    return summary_dict, dff, fig


def vis_poo(df_red):
    return px.line(df_red, y="res", title='Percentage of Optimum', labels={"index": "epoch", "res": "Percentage of social optimum"})


def percentage_of_optimum(history, cop_val, classes, agg_step=1, visualize=True):
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
                    d[act_epoch] = {'pay_off': 0,
                                    'num_of_matches': 0}

                # TODO FIX for the correct util
                d[act_epoch]['pay_off'] += game.player_util
                d[act_epoch]['num_of_matches'] += 1

                d['total']['pay_off'] += game.player_util
                d['total']['num_of_matches'] += 1

    summary_dict = {}
    summary_dict["total"] = {'pay_off': 0,
                             'num_of_matches': 0}

    for player in history.values():
        poo_map(summary_dict, player)
    # Here the dict is done

    df = pd.DataFrame.from_dict(summary_dict, orient='index')

    # Here the df is done
    df['res'] = df['pay_off']/(cop_val * df['num_of_matches'])
    df_red = df.drop(['total']).sort_index()

    fig = None
    if visualize:
        vis_poo(df_red)
        # fig.show()
    return summary_dict, df_red, fig


def class_change_over_time(history, classes, agg_step=1):
    raise NotImplementedError


def vis_grid(df_grid, epoch):
    z_colors = []
    for row in df_grid:
        curr = []
        for value in row:
            curr.append(
                list(co.hex_to_rgb(fix_colorscale[rStrategies[value]])))
        z_colors.append(curr)
    img_rgb = np.array(z_colors, dtype=np.uint8)
    fig = px.imshow(img_rgb)
    fig.update_layout(width=700, height=700, title=f"Epoch: {epoch}")
    return fig
