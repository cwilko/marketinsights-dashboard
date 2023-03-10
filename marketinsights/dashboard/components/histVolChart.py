from marketinsights.dashboard.components import DashboardComponent
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import numpy as np


class HistoricalVolatility(DashboardComponent):

    def __init__(self, app, bcm, mds, id, theme, market, source, window):
        DashboardComponent.__init__(self, app, bcm, mds, id, theme)
        self.market = market
        self.source = source
        self.window = window

    def getContent(self):

        @self.app.callback(Output(self.id, 'children'),
                           [Input('url', 'href')],
                           background=True,
                           manager=self.bcm)
        def load_graph(href):

            if href is None:
                raise PreventUpdate

            data = self.getData(self.market, self.source).reset_index().set_index("Date_Time")

            data = (np.log(data.Close) - np.log(data.Close.shift(1))).rolling(self.window).std() * 252 ** .5 * 100.0

            fig = px.line(x=data.index, y=data,
                          template=self.theme,
                          title="{}: Historical Volatility for {}".format(self.market, self.source),
                          labels={"y": "Volatility %", "x": "Date"}
                          )

            fig.update_layout(title={'xanchor': 'center', 'yanchor': 'top', 'x': 0.5, 'y': 0.9})

            return dcc.Graph(id=self.id, figure=fig)

        return html.Div(id=self.id, children=[html.Div([html.P("Loading..."), dbc.Spinner(color="primary")], style={"height": "300px"})])
