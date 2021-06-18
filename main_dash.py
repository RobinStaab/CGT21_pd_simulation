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


Strategies = {'RANDOM': 1, 'DEFECT': 2, 'COOPERATE': 3, 'GT': 4, 'TFT': 5, 'TFTD': 6, 'TF2T': 7}
fig = go.Figure()
colorscales = px.colors.named_colorscales()

task_queue  = None
res_queue   = None

app.layout = html.Div(children=[
    dcc.Store(id='local_start', storage_type='local'),    # This feels really dirty but how can I have dash callback without an output?
    dcc.Store(id='local_stop', storage_type='local'),    # Local Store to keep the Simulator
    dcc.Store(id='local_toggle', storage_type='local'),    # Local Store to keep the Simulator
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
                        html.P(children=f"Strategy: {_}"),
                        dcc.Input(
                            id={'role': 'strategy_input', 'index': _},
                            type="number",
                            placeholder=f"Number of players playing {_}",
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
                        min=0,
                        max=40,
                        step=1,
                        marks={
                            0: '0',
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
                        min=0,
                        max=40,
                        step=1,
                        marks={
                            0: '0',
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
                    min=0,
                    max=40,
                    step=1,
                    marks={
                        0: '0',
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
                    min=0,
                    max=40,
                    step=1,
                    marks={
                        0: '0',
                        10: '10',
                        20: '20',
                        30: '30',
                        40: '40'
                    },
                    value=1,
                    persistence=True,
                )], style={'width': '49%', 'display': 'inline-block'}),

                html.Button('Start', id='start', n_clicks=0),
                html.Button('Pause', id='toggle', n_clicks=0),
                html.Button('Reset', id='stop', n_clicks=0),

                # Basic settings - TODO Make me look nice, also probably default values would be reasonable
                dcc.Input(
                        id="grid_x",
                        type="number",
                        placeholder="Width of Field"
                    ),
                dcc.Input(
                        id="grid_y",
                        type="number",
                        placeholder="Height of Field"
                    ),
                dcc.Input(
                        id="play_window",
                        type="number",
                        placeholder="Window play size"
                    ),
                dcc.Input(
                        id="travel_window",
                        type="number",
                        placeholder="Window in which agents travel"
                    ),
                dcc.Input(
                        id="rand_seed",
                        type="number",
                        placeholder="Random Seed"
                    ),
                dcc.Input(
                        id="imit_prob",
                        type="number",
                        placeholder="Imitation probability",
                        min=0, max=1, step=0.1
                    ),
                dcc.Input(
                        id="migrate_prob",
                        type="number",
                        placeholder="Migration probability",
                        min=0, max=1, step=0.1
                    ),
                dcc.Input(
                        id="step_size",
                        type="number",
                        placeholder="Step Size",
                        min=1, max=100, step=1
                    ),
                dcc.Input(
                        id="omega",
                        type="number",
                        placeholder="Omega probability",
                        min=0, max=1, step=0.1
                    ),

                dcc.Dropdown(
                    id='colorscale',
                    options=[{"value": x, "label": x}
                    for x in colorscales],
                    value='viridis'
                ),
                dcc.Graph(id='play-graph', figure=fig),
                dcc.Interval( id='interval-component', interval=100, # in milliseconds 
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

    try:
        pot_res = res_queue.get(False)   # Blocking get
        print("Update")
        fig = go.Figure(data=go.Heatmap(
                    name=f"Epoch: {pot_res['epoch']}",
                    z=pot_res["grid"],
                    xgap=1.5,
                    ygap=1.5,
                    hoverongaps = False))
        fig.update_layout(width=600, height=600, title=f"Epoch: {pot_res['epoch']}")
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
    Output('local_start', 'data'),
    [Input('start', 'n_clicks')],
    [State("slider-T", 'value'),
     State("slider-R", 'value'),
     State("slider-P", 'value'),
     State("slider-S", 'value'),
     State("grid_x", "value"),
     State("grid_y", "value"),
     State("play_window", "value"),
     State("travel_window", "value"),
     State("imit_prob", "value"),
     State("migrate_prob", "value"),
     State("omega", "value"),
     State("step_size", "value"),
     State("rand_seed", "value"),
     # NOTE Please append all fixed features before here so that we can use *args for the strategies
     State({'role': 'strategy_slider', 'index': ALL}, 'value')], 
     prevent_initial_call=True)
def start_sim(clicks, val_T: int = 1, val_R: int = 1, val_P: int = 1, val_S: int = 1, grid_x: int = 40, grid_y: int = 40 , play_window: int = 1, travel_window: int = 3, imit_prob: float = 0.8, migrate_prob: float = 0.8, omega:float = 0.9, rand_seed: int = 42, step_size:int = 42,  *args: tuple):

    print("Started Simulation")

    strategy_counts = args[0]
    strategy_names  = list(Strategies.keys())
    # Build the CFG-Message
    # TODO Input the grid-size x and y, etc.

    msg_dict = {
            'T' : val_T,
            'R' : val_R,
            'S' : val_S,
            'P' : val_P,
            'strategies'      : strategy_names,
            'counts'          : strategy_counts,
            'grid_x'          : grid_x,
            'grid_y'          : grid_y,
            'num_players'     : sum(strategy_counts),
            'play_window'     : play_window,
            'migrate_window'  : travel_window,
            'imit_prob'       : imit_prob,
            'migrate_prob'    : migrate_prob,
            'omega'           : omega,
            'epochs'          : 10,
            'step-size'       : step_size
    }

    task_queue.put(ProcessMsg("RESTART", msg_content=msg_dict))

    return 1


@app.callback(
    Output('local_stop', 'data'),
    [Input('stop', 'n_clicks')],
     prevent_initial_call=True)
def stop_sim(*args):
    print("Reset Simulation")
    task_queue.put(ProcessMsg("RESET", msg_content=None))
    return 1

@app.callback(
    Output('local_toggle', 'data'),
    [Input('toggle', 'n_clicks')],
     prevent_initial_call=True)
def stop_sim(*args):
    print("Toggled Simulation")
    task_queue.put(ProcessMsg("TOGGLE", msg_content=None))
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
