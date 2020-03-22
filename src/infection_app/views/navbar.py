import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app, server
from views import basic_model


dashboard_pages = {'/basic_model': basic_model}

navBar = dbc.NavbarSimple(id='navBar',
                          children=[],
                          sticky='top',
                          dark=False,
                          fluid=True,  # for simple
                          )

@app.callback(
    Output('navBar', 'children'),
    [Input('pageContent', 'children')])
def navBar_children(input1):
    DashboardNavItems = [
        dbc.NavItem(dbc.NavLink(href.replace('/', '').title().replace('-', ' '),
                                href=href))
        for href in dashboard_pages.keys()
    ]

    navBarContents = DashboardNavItems
    return navBarContents
