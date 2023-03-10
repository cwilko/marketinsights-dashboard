from marketinsights.dashboard.components import DashboardComponent
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px


class HistoricalPrice(DashboardComponent):

    def __init__(self, app, bcm, mds, id, theme, market, source):
        DashboardComponent.__init__(self, app, bcm, mds, id, theme)
        self.market = market
        self.source = source

    def getContent(self):

        @self.app.callback(Output(self.id, 'children'),
                           [Input('url', 'href')],
                           background=True,
                           manager=self.bcm)
        def load_graph(href):

            if href is None:
                raise PreventUpdate

            data = self.getData(self.market, self.source)
            data = data.reset_index().set_index("Date_Time")

            fig = px.line(x=data.index, y=data.Close,
                          template=self.theme,
                          title="{}: Historical Prices for {}".format(self.market, self.source),
                          labels={"y": "Price", "x": "Date"}
                          )

            fig.update_layout(title={'xanchor': 'center', 'yanchor': 'top', 'x': 0.5, 'y': 0.9})

            return dcc.Graph(id=self.id, figure=fig)

        return html.Div(id=self.id, children=[html.Div([html.P("Loading..."), dbc.Spinner(color="primary")], style={"height": "300px"})])
