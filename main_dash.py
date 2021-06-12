# This is an old project of mine for a practicum in physical chemistry, we can use the skeleton of it

from Simulator import Simulator
from Player import Player
from Strategies import *
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


Strategies = {'TFT': 1, 'TF2T': 2, 'TFTD': 3, 'AC': 4, 'AD': 5, 'GT': 6, 'R': 7}

fig = go.Figure()

app.layout = html.Div(children=[
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
                dcc.Graph(id='play-graph', figure=fig),
                html.Div(id='results-1', children='Summary will be displayed here', style={'width': '49%', 'display': 'inline-block'}),
            ]),
        ]),
        ])


@app.callback(
    Output('play-graph', 'figure'),
    Input('start', 'n_clicks'),
    [State("slider-T", 'value'),
     State("slider-R", 'value'),
     State("slider-P", 'value'),
     State("slider-S", 'value'),
     State({'role': 'strategy_slider', 'index': ALL}, 'value')], prevent_initial_call=True)
def update_figure(clicks, val_T: int = 1, val_R: int = 1, val_P: int = 1, val_S: int = 1, *args: tuple):

    inputs = [val_T, val_R, val_P, val_S] + list(args[0])       # This excludes any inputs not regulated through sliders but we can change this later if needed

    for i in inputs:
        if not i:
            raise PreventUpdate

    grid_x = 50
    grid_y = 50
    num_players = 2400
    play_window = 1
    migrate_window = 3
    imit_prob = 0.8
    migrate_prob = 0.8
    epochs = 1000

    # hahaha this will never be this simple
    player_cfgs = generate_players("random", num_players, play_window, migrate_window, imit_prob, migrate_prob)
    # player_cfgs = generate_players("random", num_players, play_window, migrate_window, imit_prob, migrate_prob)
    sim = Simulator(grid_x, grid_y, num_players, play_window, migrate_window, player_cfgs, val_T, val_R, val_S, val_P   )


    # sim.grid id id-1 is player.strategy

    x = []
    y = []
    strat = []
    strategies = []
    for i in range(0, grid_x):
        for j in range(0, int(sim.grid[i].size)):
            if sim.grid[i][j] != 0:
                strat.append(Strategies[sim.players[int(sim.grid[i][j])-1].strategy.name])
            else:
                strat.append(0)
        strategies.append(strat)
        strat = []
    # round()
    fig = px.imshow(strategies, x=list(range(0,50)), y=list(range(0,50)), color_continuous_scale='RdBu_r')
    fig.update_layout(transition_duration=500)
    return fig


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
    app.run_server(debug=True)
