import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from app import app
from dash import callback_context
import numpy as np
import pandas as pd
import os
import sys
import json

import scipy.integrate as integrate
root_folder = os.path.abspath(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(root_folder)))
sys.path.append(root_folder)
from src.packages.models.SIR_models import base_sri_model


class first_epi_model(base_sri_model):
    labels = ["healthy", "infected", "recovered"]
    epsilon = 1e-2
    a = 0.7  # infection
    b = 3  # recovering capatibility
    t_max = 20
    y0 = np.array([1, epsilon, 0])

    def edp_model(self, t, y):
        inf_p = self.b*y[0]*y[1]  # infected_people
        r_p = 1/self.a * y[1]

        dydt = np.array([-inf_p, inf_p-r_p, r_p])
        return dydt


e = first_epi_model()
e._compute_simu()


@app.callback(Output('graph_basic_evolution', 'figure'),
              [Input('infection_factor', 'value'),
              Input('recovering_factor', 'value'),
              Input('max_time', 'value'),])
def graph_basic_evolution_figure(a, b, t_max):
    e.a = a
    e.b = b
    e.t_max = t_max

    e._compute_simu()

    figure = {
        'data': [
            {'x': e.sol.t, 'y': soly, 'name': label} for soly, label in zip(e.sol.y, e.labels)
        ]
    }
    return figure

figure = graph_basic_evolution_figure(a=0.7, b=3, t_max=20)

layout = dbc.Container([
    html.H5('infection factor'),
    dcc.Slider(id='infection_factor', min=0, max=1, step=0.1, value=0.7,
        marks={val: "{0:.2f}".format(val) for val in np.arange(0.0, 1.0, 0.1)}
    ),
    html.H5('recovering factor'),
    dcc.Slider(id='recovering_factor', min=0, max=10, step=1, value=2,
        marks={val: "{0:.2f}".format(val) for val in np.arange(0.0, 10.0, 1.0001)}
),
    html.H5('max time'),
    dcc.Slider(id='max_time', min=0, max=50, step=1, value=20,
        marks={val: "{0:.2f}".format(val) for val in np.arange(0.0, 50.0, 5.00001)}
),

    dcc.Graph(
        id='graph_basic_evolution',
        figure=json.loads(figure)['response']['props']['figure']
    )
])
