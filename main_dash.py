# This is an old project of mine for a practicum in physical chemistry, we can use the skeleton of it
import matplotlib
matplotlib.use('tkagg')
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


Strategies = {'RANDOM': 1, 'DEFECT': 2, 'COOPERATE': 3,
              'GT': 4, 'TFT': 5, 'TFTD': 6, 'TF2T': 7}

fig = go.Figure()
poo_plot = go.Figure()

colorscales = px.colors.named_colorscales()

task_queue = None
res_queue = None

app.layout = html.Div(
    className="main_app",
    children=[
        # This feels really dirty but how can I have dash callback without an output?
        dcc.Store(id='local_start', storage_type='local'),
        # Local Store to keep the Simulator
        dcc.Store(id='local_stop', storage_type='local'),
        # Local Store to keep the Simulator
        dcc.Store(id='local_toggle', storage_type='local'),
        html.H1(
            children='Controversies in Game Theory 2021 - Repeated Prisoners Dilemma'),

        html.P(children='''
        Made by Fabrice Egger, Robin Staab, Jan Urech, Kim Nik Baumgartner'''),
        html.P(children='''short explanation of app usage'''),
        html.P(children=''' If you have any troubles don't hesitate to write us a mail to my kimbau@student.ethz.ch mail :)
    '''),
        html.Div(
            className="content",
            children=[
                html.Div(className="header", children=[
                    html.Div(className="sliders", children=[
                        html.Div(className="strategies", children=[
                            html.H3(children='Strategies'),
                            html.Div([
                                html.Div(children=[
                                    html.P(children=f"{_}"),
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
                                            0: '0',
                                            50: '50',
                                            100: '100',
                                            150: '150',
                                            200: '200',
                                        },
                                        value=50,
                                        persistence=True,
                                    )
                                ]) for _, n in Strategies.items()
                            ],),
                        ]),
                        html.Div(className="rewards", children=[
                            html.H3(
                                children='Regulating Rewards'),
                            html.Table(children=[
                                html.Thead(children=[
                                    html.Tr(children=[html.Td(""), html.Td(
                                        "Cooperate"), html.Td("Defection")])
                                ]),
                                html.Tbody(children=[
                                    html.Tr(children=[html.Td("Cooperate"), html.Td(
                                        "R, R"), html.Td("S, T")]),
                                    html.Tr(children=[html.Td("Defection"), html.Td(
                                        "T, S"), html.Td("P, P")])
                                ])
                            ]),
                            html.Div(className="rewardSlider", children=[
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
                                    value=30,
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
                                    value=20,
                                    persistence=True,
                                ),

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
                                    value=10,
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
                                    value=5,
                                    persistence=True,
                                )]),
                        ])
                    ]),
                    html.Div(className="simulationSliders", children=[
                        html.Div(children=[
                            html.Label("Width of Field"),
                            dcc.Input(
                                id="grid_x",
                                type="number",
                                value=20
                            )]),
                        html.Div(children=[
                            html.Label("Height of Field"),
                            dcc.Input(
                                id="grid_y",
                                type="number",
                                value=20,
                            )]),
                        html.Div(children=[
                            html.Label("Window play size"),
                            dcc.Input(
                                id="play_window",
                                type="number",
                                value=1,
                            ), ]),

                        html.Div(children=[
                            html.Label("Migration range"),
                            dcc.Input(
                                id="travel_window",
                                type="number",
                                value=3,
                            ), ]),

                        html.Div(children=[
                            html.Label("Random Seed"),
                            dcc.Input(
                                id="rand_seed",
                                type="number",
                                value=12345,
                                placeholder="Random Seed"
                            ), ]),

                        html.Div(children=[
                            html.Label("Imitation probability"),
                            dcc.Input(
                                id="imit_prob",
                                type="number",
                                value=0.2,
                                min=0, max=1, step=0.1
                            )]),

                        html.Div(children=[
                            html.Label("Migration probability"),
                            dcc.Input(
                                id="migrate_prob",
                                type="number",
                                value=0.1,
                                min=0, max=1, step=0.1
                            )]),
                        html.Div(children=[
                            html.Label("Step Size"),
                            dcc.Input(
                                id="step_size",
                                type="number",
                                value=10,
                                min=1, max=100, step=1
                            ), ]),

                        html.Div(children=[
                            html.Label("Omega probability"),
                            dcc.Input(
                                id="omega",
                                type="number",
                                value=0.9,
                                min=0, max=1, step=0.1
                            )]),
                    ])
                ]),
                
                html.Div(className="simulation", children=[
                    dcc.Dropdown(
                        id='colorscale',
                        options=[{"value": x, "label": x}
                                 for x in colorscales],
                        value='viridis',
                        style={"display": "none"}
                    ),
                    html.H2("Simulation"),
                    html.Div(className="game", children=[
                        html.Div(children=[
                            html.Div(className="controlbuttons", children=[
                                html.Button('Start', id='start', n_clicks=0),
                                html.Button('Pause', id='toggle', n_clicks=0),
                                html.Button('Reset', id='stop', n_clicks=0),
                                html.Button('Refresh', id='refresh', n_clicks=0)
                            ]),
                            dcc.Graph(id='play-graph', figure=fig),
                            dcc.Interval(id='interval-component', interval=200,  # in milliseconds
                                         n_intervals=0)]),
                        html.Div(children=[
                            html.Div(className="timeline",
                                     children="Timeline"),

                            html.Div(className="plots", children=[
                                dcc.Graph(id='poo-plot', figure=poo_plot),
                            ])
                        ])
                    ]),
                    html.Div(id='results-1',
                             children='Summary will be displayed here'),
                ]),
            ]),
    ])


@ app.callback(
    Output('play-graph', 'figure'),
    Output('poo-plot', 'figure'),
    [Input('interval-component', 'n_intervals')],
    [State("slider-T", 'value'),
     State("slider-R", 'value'),
     State("slider-P", 'value'),
     State("slider-S", 'value'),
     State({'role': 'strategy_slider', 'index': ALL}, 'value'),
     ], prevent_initial_call=True)
def update_figure(n_intervals, val_T: int = 1, val_R: int = 1, val_P: int = 1, val_S: int = 1, *args: tuple):

    # NOTE I just removed this for testing purposes
    # inputs = [val_T, val_R, val_P, val_S] + list(args[0])       # This excludes any inputs not regulated through sliders but we can change this later if needed

    try:
        pot_res = res_queue.get(False)   # Non-Blocking get

        print(f"Update: {pot_res['epoch']}")
        fig = go.Figure(data=go.Heatmap(
            name=f"Epoch: {pot_res['epoch']}",
            z=pot_res["grid"],
            xgap=1.5,
            ygap=1.5,
            hoverongaps=False))
        fig.update_layout(width=800, height=800, title=f"Epoch: {pot_res['epoch']}")

        fig_poo = px.line(pot_res['df_poo'], y="res", title='Percentage of Optimum over time')
        print("Done")
        return fig, fig_poo
    except Empty:
        return dash.no_update


# @ app.callback(
#     Output('play-graph', 'figure'),
#     Input('refresh', 'n_clicks'),
#     prevent_initial_call=True)
# def refresh_sim(*args):

#     print("You clicked me!")
#     try:
#         pot_res = res_queue.get(False)   # Non-Blocking get
#         print(f"Update1: {pot_res['epoch']} - Q-size: {res_queue.qsize()}")
#         while not res_queue.empty() > 0:
#             pot_res = res_queue.get(False)
#             print(f"Found epoch: {pot_res['epoch']} - Q-size: {res_queue.qsize()}")

#         print(f"Update: {pot_res['epoch']}")
#         fig = go.Figure(data=go.Heatmap(
#             name=f"Epoch: {pot_res['epoch']}",
#             z=pot_res["grid"],
#             xgap=1.5,
#             ygap=1.5,
#             hoverongaps=False))
#         fig.update_layout(width=800, height=800, title=f"Epoch: {pot_res['epoch']}")

#         return fig
#     except Empty:
#         return dash.no_update


@ app.callback(
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
def start_sim(clicks, val_T: int = 1, val_R: int = 1, val_P: int = 1, val_S: int = 1, grid_x: int = 40, grid_y: int = 40, play_window: int = 1, travel_window: int = 3, imit_prob: float = 0.8, migrate_prob: float = 0.8, omega: float = 0.9, step_size: int = 42, rand_seed: int = 42,  *args: tuple):

    print("Started Simulation")

    strategy_counts = args[0]
    strategy_names = list(Strategies.keys())


    msg_dict = {
        'T': val_T,
        'R': val_R,
        'S': val_S,
        'P': val_P,
        'strategies': strategy_names,
        'counts': strategy_counts,
        'grid_x': grid_x,
        'grid_y': grid_y,
        'num_players': sum(strategy_counts),
        'play_window': play_window,
        'migrate_window': travel_window,
        'imit_prob': imit_prob,
        'migrate_prob': migrate_prob,
        'omega': omega,
        'epochs': 10,
        'step-size': step_size,
        'rand_seed': rand_seed
    }

    task_queue.put(ProcessMsg("RESTART", msg_content=msg_dict))

    return 1


@ app.callback(
    Output('local_stop', 'data'),
    [Input('stop', 'n_clicks')],
    prevent_initial_call=True)
def stop_sim(*args):
    print("Reset Simulation")
    task_queue.put(ProcessMsg("RESET", msg_content=None))
    return 1


@ app.callback(
    Output('local_toggle', 'data'),
    [Input('toggle', 'n_clicks')],
    prevent_initial_call=True)
def toggle_sim(*args):
    print("Toggled Simulation")
    task_queue.put(ProcessMsg("TOGGLE", msg_content=None))
    return 1


@ app.callback(
    Output({'role': 'strategy_slider', 'index': MATCH}, 'value'),
    [Input({'role': 'strategy_input', 'index': MATCH}, 'value')], prevent_initial_call=True)
def update_output(value: int):
    if not value:
        raise PreventUpdate
    return int(value)


# This is stupid but I cant have the same output/input pair....
@ app.callback(
    Output({'role': 'strategy_input', 'index': MATCH}, 'placeholder'),
    [Input({'role': 'strategy_slider', 'index': MATCH}, 'value')])
def update_output(value: int):
    if not value:
        raise PreventUpdate
    return int(value)


if __name__ == '__main__':

    # Establish communication queues
    task_queue = mp.Queue()
    res_queue = mp.Queue()

    num_servers = 1  # mp.cpu_count() * 2
    print('Creating {} consumers'.format(num_servers))
    consumers = [SimulatorProcess(task_queue, res_queue)
                 for i in range(num_servers)]
    for w in consumers:
        w.start()

    app.run_server(debug=True)
