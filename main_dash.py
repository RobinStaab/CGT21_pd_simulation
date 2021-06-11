# This is an old project of mine for a practicum in physical chemistry, we can use the skeleton of it


from dash.dependencies import Input, Output, State, MATCH, ALL
from statistics import median
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
import dash_dangerously_set_inner_html
import typing
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='INSERT TITLE Controversies in Game Theory 2021 - Prisoners Dilemma'),

    html.Div(children='''
        Made by Fabrice Egger, Robin Staab, ??, Kim Nik Baumgartner'''),
    html.Div(children=
        '''short explanation of app usage'''),
    html.Div(children=''' If you have any troubles don't hesitate to write us a mail to my kimbau@student.ethz.ch mail :)
    '''),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H3(children='TITLE'),
                html.H4(children='SUBTITLE/TEXT'),
                dcc.Slider(
                    id="slider-P",
                    min=0,
                    max=100,    # find decent max? maybe more around 10/-10?
                    style={'width': '26%'},
                    step=1,
                    marks={
                        0: '0',
                        10: '10',
                        20: '20',
                        30: '30',
                        40: '40 etc....'
                    },
                    persistence=True,
                ),
                dcc.Slider(
                    id="slider-P",
                    min=0,
                    max=100,    # find decent max? maybe more around 10/-10?
                    style={'width': '26%'},
                    step=1,
                    marks={
                        0: '0',
                        10: '10',
                        20: '20',
                        30: '30',
                        40: '40 etc....'
                    },
                    persistence=True,
                ),
                dcc.Slider(
                    id="slider-P",
                    min=0,
                    max=100,  # find decent max? maybe more around 10/-10?
                    style={'width': '26%'},
                    step=1,
                    marks={
                        0: '0',
                        10: '10',
                        20: '20',
                        30: '30',
                        40: '40 etc....'
                    },
                    persistence=True,
                ),
                html.Button('Submit', id='submit-C', n_clicks=0), # technically not necessary so will be cut
                dcc.Graph(id='regression-C'), # do we even want a graph? what should it show?
                html.Div(id='results-1', children='Summary will be displayed here', style={'width': '49%', 'display': 'inline-block'}),
            ]),
        ]),
        ])
    ])


@app.callback(
    Output('mean-Ae', 'figure'),
    Input('submit-Ae', 'n_clicks'),
    [State("DataAa-K", 'value'),
     State("DataAb-K", 'value'),
     State("DataAc-K", 'value'),
     State("DataAd-K", 'value'),
     State("DataAe-K", 'value'),
     State("DataAa-T", 'value'),
     State("DataAb-T", 'value'),
     State("DataAc-T", 'value'),
     State("DataAd-T", 'value'),
     State("DataAa-T", 'value')], prevent_initial_call=True)
def update_figure(clicks, AaK: str, AbK: str, AcK: str, AdK: str, AeK: str, AaT: str, AbT: str, AcT: str, AdT: str, AeT: str):
    med = []
    inputs = [AaK, AbK, AcK, AdK, AeK, AaT, AbT, AcT, AdT, AeT]
    for i in inputs:
        if not i:
            raise PreventUpdate
        ui = [float(s) for s in i.split(',')]
        med.append(median(ui))

    medK = [med[s] for s in range(0,5)]
    medT = [med[s] for s in range(5,len(med))]
    source = ['High-purity Water', 'deionized water', 'tap water from the lab', 'your water from home', 'mineral water of your choice']

    df = pd.DataFrame(dict(a=medK, b=medT, source=source))        #[dict(a=[float(s) for s in AaK.split(',')], Temp=[float(s) for s in AaT.split(',')], source='High-purity Water'), dict(a=[float(s) for s in AbK.split(',')], Temp=[float(s) for s in AbT.split(',')], source='deionized water')])

    fig = px.scatter(df, y="a", x="source", hover_data="b", labels={
                     "a": "Conductivity κ (μS/cm)",
                     "b": "Temperature Θ (°C)"})  #"μS/cm", y="Temp in °C")

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    [Output('regression-B', 'figure'), Output('results-B', 'children')],
    Input('submit-B', 'n_clicks'),
    [State("DataB-K", 'value')], prevent_initial_call=True,)
def update_regB(clicks, K: str):

    if not K:
        raise PreventUpdate
    df = pd.DataFrame(dict(a=[float(s) for s in K.rsplit(',')], b=[float(s) for s in range(50, 30, -1)]))

    fig = px.scatter(df, y="a", x="b", opacity=0.65, trendline='ols', trendline_color_override='darkblue',  labels={
                     "a": "Conductivity κ (mS/cm)",
                     "b": "Temperature Θ (°C)"})  # "μS/cm", y="Temp in °C")

    fig.update_layout(transition_duration=500)
    results = px.get_trendline_results(fig)

    return fig, dash_dangerously_set_inner_html.DangerouslySetInnerHTML(f''' %s ''' % results.px_fit_results.iloc[0].summary().as_html())


@app.callback(
    [Output('regression-C', 'figure'), Output('results-C', 'children'), Output('results-C2', 'children')],
    Input('submit-C', 'n_clicks'),
    [State("DataC-K", 'value'),
     State("DataC-T", 'value'),
     State("DataC-CMC", 'value')], prevent_initial_call=True,)
def update_regC(clicks, K: str, T: str, CMC: str):

    if not K or not T or not CMC:
        raise PreventUpdate

    listC = [0, 2, 4, 6, 8, 10, 12, 15, 20, 24, 30]
    CMCP = listC.index(float(CMC))
    cinout = ["preCMC" for x in range(0, CMCP)]
    cinout.extend("postCMC" for x in range(CMCP, len(listC)))

    listK = [float(s) for s in K.rsplit(',')]
    listK.insert(CMCP, listK[CMCP])

    listT = [float(s) for s in T.rsplit(',')]
    listT.insert(CMCP, listT[CMCP])

    listC.insert(CMCP, listC[CMCP])

    cinout.insert(CMCP, "preCMC")

    df = pd.DataFrame(dict(a=listK, b=listC, temp=listT, cmc=cinout))

    fig = px.scatter(df, y="a", x="b", opacity=0.65, color="cmc", trendline='ols', labels={
                     "a": "Conductivity κ (μS/cm)",
                     "b": "Concentration of SDS (mM)",
                     "temp": "Temp in °C"})  # "μS/cm", y="Temp in °C")
    results = px.get_trendline_results(fig)
    fig.update_layout(transition_duration=500)

    return fig, dash_dangerously_set_inner_html.DangerouslySetInnerHTML(f''' %s ''' % results.px_fit_results.iloc[0].summary().as_html()), dash_dangerously_set_inner_html.DangerouslySetInnerHTML(f''' %s ''' % results.px_fit_results.iloc[1].summary().as_html())


@app.callback(
    Output('regression-D', 'figure'),
    Input('submit-D', 'n_clicks'),
    [State("DataD-K", 'value'),
     State("DataD-T", 'value'),
     State("DataD-Cl", 'value')], prevent_initial_call=True,)
def update_regD(clicks, K: str, T: str, Cl: str):

    if not K or not T or not Cl:
        raise PreventUpdate

    df = pd.DataFrame(dict(a=[float(s) for s in K.rsplit(',')], b=[float(s) for s in T.rsplit(',')], cl=[float(s) for s in Cl.rsplit(',')]))

    fig = px.scatter(df, y="a", x="cl", opacity=0.65, trendline='lowess',  labels={
                     "a": "Conductivity κ (μS/cm)",
                     "cl": "Amount of titrated CaCl₂ (ml)",
                     "b": "Temperature Θ (°C)"})  # "μS/cm", y="Temp in °C")

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)