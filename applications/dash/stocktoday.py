import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import sqlite3
from config import dash_assets
import os

print("============", dash_assets)
base_asset = os.path.join(dash_assets, "base.css")
style_asset = os.path.join(dash_assets, "style.css")

ext_assets = [base_asset, style_asset]


def read_data():
    db_path = "instances/sample.db"
    df_ = pd.read_sql(
        "select * from daily_stock;",
        con=sqlite3.connect(db_path)
    )
    df_.index = pd.to_datetime(df_["stock_date"])
    return df_


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({"label": i, "value": i})
    return dict_list


def filter_pan(filter_list, init_filter):
    layout = html.Div(
        className="four columns div-user-controls",
        children=[
            html.H2("DASH - STOCK PRICES"),
            html.P("Stock Analytics Over Time"),
            html.P("Pick one or more stocks..."),
            html.Div(
                className="div-for-dropdown",
                children=[
                    dcc.Dropdown(
                        id="stock-selector",
                        options=get_options(filter_list),
                        multi=True,
                        value=[init_filter],
                        style={"backgroundColor": "#1E1E1E"},
                        className="stockselector",

                    )
                ],
                style={"color": "#1E1E1E"},
            )
        ]
    )
    return layout


def analytics_pan():
    layout = html.Div(
        className="eight columns div-for-charts bg-grey",
        children=[
            dcc.Graph(
                id="timeseries",
                config={"displayModeBar": False},
                animate=True,
            ),
            dcc.Graph(
                id="change",
                config={"displayModeBar": False}
            )
        ]
    )
    return layout


def full_layout(left_pan, right_pan):
    main_layout = html.Div(
        children=[
            html.Div(
                className="row",
                children=[left_pan, right_pan]
            )
        ]
    )
    return main_layout


def init_callback(app, df_):
    @app.callback(
        Output("timeseries", "figure"),
        [Input("stock-selector", "value")]
    )
    def update_graph(selected_value):
        trace1 = []
        df_sub = df_.copy()
        for stock in selected_value:
            trace1.append(
                go.Scatter(
                    x=df_sub[df_sub["stock"] == stock].index,
                    y=df_sub[df_sub["stock"] == stock]["value"],
                    mode="lines",
                    opacity=0.7,
                    name=stock,
                    textposition="bottom center"
                )
            )
        traces = [trace1]
        data = [val for sublist in traces for val in sublist]
        figure = {
            "data": data,
            "layout": go.Layout(
                colorway=[
                    "#5E0DAC", "#FF4F00", "#375CB1",
                    "#FF7400", "#FFF400", "#FF0056"
                ],
                template="plotly_dark",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                plot_bgcolor="rgba(0, 0, 0, 0)",
                margin={"b": 15},
                hovermode="x",
                autosize=True,
                title={
                    "text": "Stock Prices",
                    "font": {"color": "white"},
                    "x": 0.5
                },
                xaxis={"range": [df_sub.index.min(), df_sub.index.max()]},
            ),
        }
        return figure

    @app.callback(
        Output("change", "figure"),
        [Input("stock-selector", "value")]
    )
    def update_change(selected_value):
        """Draw traces of the feature "change"
        based one the currently selected stocks
        """
        trace = []
        df_sub = df_.copy()
        # Draw and append traces for each stock
        for stock in selected_value:
            trace.append(
                go.Scatter(
                    x=df_sub[df_sub["stock"] == stock].index,
                    y=df_sub[df_sub["stock"] == stock]["change"],
                    mode="lines",
                    opacity=0.7,
                    name=stock,
                    textposition="bottom center"
                )
            )
        traces = [trace]
        data = [val for sublist in traces for val in sublist]
        # Define Figure
        figure = {
            "data": data,
            "layout": go.Layout(
                colorway=[
                    "#5E0DAC", "#FF4F00", "#375CB1",
                    "#FF7400", "#FFF400", "#FF0056"
                ],
                template="plotly_dark",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                plot_bgcolor="rgba(0, 0, 0, 0)",
                margin={"t": 50},
                height=250,
                hovermode="x",
                autosize=True,
                title={
                    "text": "Daily Change",
                    "font": {"color": "white"},
                    "x": 0.5
                },
                xaxis={
                    "showticklabels": False,
                    "range": [df_sub.index.min(), df_sub.index.max()]
                },
            ),
        }

        return figure


def create_stock_app(server=None):
    stock_df = read_data()
    filters = stock_df["stock"].unique()
    first_filter = sorted(filters)[0]
    left_layout = filter_pan(filters, first_filter)
    right_layout = analytics_pan()
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/stock-today/',
        assets_folder=dash_assets
    )
    dash_app.title = 'My Stock App'
    dash_app.layout = full_layout(left_layout, right_layout)
    init_callback(dash_app, stock_df)
    return dash_app

