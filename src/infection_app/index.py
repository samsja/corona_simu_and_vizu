# import for requirements

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app

from views import error, navbar
from views.navbar import navBar, dashboard_pages
from datetime import datetime as dt
import sys


app.layout = html.Div([
    dcc.Location(id='url'),

    html.Div([
        navBar,
        html.Div(id='pageContent'),
        dcc.Link('redirect', id='success_login_link'),
        
    ] + [dcc.Link(pathname_dashboard.replace('_',' ').replace('/',' '), href=pathname_dashboard) for pathname_dashboard in dashboard_pages.keys()]
    )
], id='table-wrapper')




@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def displayPage(pathname):
    layout = None
    print(f'path_name {pathname}')
    for pathname_dashboard, file in dashboard_pages.items():
        if pathname == pathname_dashboard and file:
            layout = file.layout

    if not layout:
        layout = error.layout
        print(f'path error {pathname}')
    return layout


if __name__ == '__main__':
    app.run_server(debug=True)
