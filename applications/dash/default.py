import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# = APP INIT # =
# - - - - - - - - - - - - - - - - - - - - - - - -
ext_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_dashboard(server=None):
    """Create a Dash app."""

    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dafault-app/',
                         external_stylesheets=ext_stylesheets
                         )
    dash_app.title = 'Top Gun Tool'
    if server:
        # Create Layout
        dash_app.layout = html.Div(children=[
            html.H1(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }
            )
        ])

        init_callbacks(dash_app)
        return dash_app.server
    else:
        return dash_app


def init_callbacks(app):
    @app.callback(
        Output(component_id='my-div', component_property='children'),
        [Input(component_id='my-id', component_property='value')]
    )
    # just to avoind the error using app_x as init call back as app
    def update_graph(app_x):
        pass


