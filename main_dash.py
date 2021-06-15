# This is an old project of mine for a practicum in physical chemistry, we can use the skeleton of it

from matplotlib.pyplot import title
from Simulator import Simulator
from Player import Player
from Strategies import *
from Taskrunner import SimulatorProcess, ProcessMsg
import time
from test_simulator import *
from dash.dependencies import Input, Output, State, MATCH, ALL
from statistics import median
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
import typing
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import multiprocessing as mp
import numpy as np
from queue import Empty


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


Strategies = {'TFT': 1, 'TF2T': 2, 'TFTD': 3, 'AC': 4, 'AD': 5, 'GT': 6, 'R': 7}
fig = go.Figure()
colorscales = px.colors.named_colorscales()

task_queue  = None
res_queue   = None

app.layout = html.Div(children=[
    dcc.Store(id='local', storage_type='local'),    # Local Store to keep the Simulator
    html.H1(children='INSERT TITLE Controversies in Game Theory 2021 - Prisoners Dilemma'),

    html.Div(children='''
        Made by Fabrice Egger, Robin Staab, Jan Urech, Kim Nik Baumgartner'''),
    html.Div(children=
        '''short explanation of app usage'''),
    html.Div(children=''' If you have any troubles don't hesitate to write us a mail to my kimbau@student.ethz.ch mail :)
    '''),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H3(children='Strategies'),
                html.Div([
                html.Div(children=[
                        html.P(children=f"Strategy: {n}"),
                        dcc.Input(
                            id={'role': 'strategy_input', 'index': _},
                            type="number",
                            placeholder=f"Number of players playing {n}",
                        ),
                        dcc.Slider(
                            id={'role': 'strategy_slider', 'index': _},
                           min=0,
                           max=200,
                           step=1,
                           marks={
                                1: '1',
                               50: '50',
                                100: '100',
                                150: '150',
                               200: '200',
                           },
                           value=50,
                           persistence=True,
                        )
                ], style={'width': '49%', 'display': 'inline-block'}) for _,n in Strategies.items()
                ],),
            ]),
                html.H4(children='Sliders for regulating rewards following'),
                html.Div(children=[
                    html.P(children="T"),
                    dcc.Slider(
                        id="slider-T",
                        min=1,
                        max=40,
                        step=1,
                        marks={
                            1: '1',
                            10: '10',
                            20: '20',
                            30: '30',
                            40: '40',
                        },
                        value=1,
                        persistence=True,
                    ),
                    html.P(children="R"),
                    dcc.Slider(
                        id="slider-R",
                        min=1,
                        max=40,
                        step=1,
                        marks={
                            1: '1',
                            10: '10',
                            20: '20',
                            30: '30',
                            40: '40',
                        },
                        value=1,
                        persistence=True,
                    ),
                ], style={'width': '49%', 'display': 'inline-block'}),
                html.Div(id = "test",children=[
                html.P(children="P"),
                dcc.Slider(
                    id="slider-P",
                    min=1,
                    max=40,
                    step=1,
                    marks={
                        1: '1',
                        10: '10',
                        20: '20',
                        30: '30',
                        40: '40',
                    },
                    value=1,
                    persistence=True,
                ),
                html.P(children="S"),
                dcc.Slider(
                    id="slider-S",
                    min=1,
                    max=40,
                    step=1,
                    marks={
                        1: '1',
                        10: '10',
                        20: '20',
                        30: '30',
                        40: '40'
                    },
                    value=1,
                    persistence=True,
                )], style={'width': '49%', 'display': 'inline-block'}),

                html.Button('Start', id='start', n_clicks=0),
                dcc.Dropdown(
                    id='colorscale',
                    options=[{"value": x, "label": x}
                    for x in colorscales],
                    value='viridis'
                ),
                dcc.Graph(id='play-graph', figure=fig),
                dcc.Interval( id='interval-component', interval=200, # in milliseconds 
                                n_intervals=0),
                html.Div(id='results-1', children='Summary will be displayed here', style={'width': '49%', 'display': 'inline-block'}),
            ]),
        ]),
        ])


@app.callback(
    Output('play-graph', 'figure'),
    [Input('interval-component', 'n_intervals')],
    [State("slider-T", 'value'),
     State("slider-R", 'value'),
     State("slider-P", 'value'),
     State("slider-S", 'value'),
     State({'role': 'strategy_slider', 'index': ALL}, 'value'),
     ], prevent_initial_call=True)
def update_figure(n_intervals, val_T: int = 1, val_R: int = 1, val_P: int = 1, val_S: int = 1, *args: tuple):

    # NOTE I just removed this for testing purposes
    #inputs = [val_T, val_R, val_P, val_S] + list(args[0])       # This excludes any inputs not regulated through sliders but we can change this later if needed

    # for i in inputs:
    #     if not i:
    #         raise PreventUpdate

    # grid_x = 50
    # grid_y = 50
    # num_players = 200
    # play_window = 1
    # migrate_window = 3
    # imit_prob = 0.8
    # migrate_prob = 0.8
    # epochs = 100
    # omega = 0.5

    # if data is None:
    #     player_cfgs = generate_players("random", num_players, play_window, migrate_window, imit_prob, migrate_prob, omega)
    #     # player_cfgs = generate_players("random", num_players, play_window, migrate_window, imit_prob, migrate_prob, omega)
    #     sim = Simulator(grid_x, grid_y, num_players, play_window, migrate_window, player_cfgs, val_T, val_R, val_S, val_P)
    #     data['sim'] = 
    #     sim.simulate(1000000000)

    # strat = []
    # strategies = []
    # for i in range(0, grid_x):
    #     for j in range(0, grid_y):
    #         if sim.grid[i][j] != 0:
    #             strat.append(Strategies[sim.players[int(sim.grid[i][j])-1].strategy.name])
    #         else:
    #             strat.append(0)
    #     strategies.append(strat)
    #     strat = []
    try:
        pot_res = res_queue.get(False)   # Blocking get
        print("Update")
        fig = go.Figure(data=go.Heatmap(
                    name= "Hello",
                    z=pot_res["grid"],
                    xgap=1.5,
                    ygap=1.5,
                    hoverongaps = False))
        fig.update_layout(width=600, height=600, title=str(time.time()))
        return fig
    except Empty:
        """fig = go.Figure(data=go.Heatmap(
                    name= "Hello2",
                    z=[[1, 20, 30],
                      [20, 1, 60],
                      [30, 60, 1]],
                    xgap=1.5,
                    ygap=1.5,
                    hoverongaps = False))
        fig.update_layout(width=600, height=600, title=str(time.time()))"""
        return dash.no_update
    



@app.callback(
    Output('local', 'data'),
    [Input('start', 'n_clicks')],
    [State("slider-T", 'value'),
     State("slider-R", 'value'),
     State("slider-P", 'value'),
     State("slider-S", 'value'),
     State({'role': 'strategy_slider', 'index': ALL}, 'value'),
     State('local', 'data')], prevent_initial_call=True)
def start_sim(clicks, val_T: int = 1, val_R: int = 1, val_P: int = 1, val_S: int = 1, *args: tuple):

    print("Hell - we clicked")
    msg_dict = {
            'T' : val_T,
            'R' : val_R,
            'S' : val_S,
            'P' : val_P,
            'strategy'        : "RANDOM",
            'grid_x'          : 22,
            'grid_y'          : 22,
            'num_players'     : int(22*22*0.4),
            'play_window'     : 1,
            'migrate_window'  : 3,
            'imit_prob'       : 0.8,
            'migrate_prob'    : 0.8,
            'epochs'          : 1000
    }

    task_queue.put(ProcessMsg("RESTART", msg_content=msg_dict))

    return 1

@app.callback(
    Output({'role': 'strategy_slider', 'index': MATCH}, 'value'),
    [Input({'role': 'strategy_input', 'index': MATCH}, 'value')], prevent_initial_call=True)
def update_output(value: int):
    if not value:
        raise PreventUpdate
    return int(value)


# This is stupid but I cant have the same output/input pair....
@app.callback(
    Output({'role': 'strategy_input', 'index': MATCH}, 'placeholder'),
    [Input({'role': 'strategy_slider', 'index': MATCH}, 'value')])
def update_output(value: int):
    if not value:
        raise PreventUpdate
    return int(value)


if __name__ == '__main__':

    # Establish communication queues
    task_queue  = mp.Queue()
    res_queue   = mp.Queue()

    num_servers = 1 #mp.cpu_count() * 2
    print('Creating {} consumers'.format(num_servers))
    consumers = [SimulatorProcess(task_queue, res_queue) for i in range(num_servers) ]
    for w in consumers:
        w.start()


    app.run_server(debug=True)
