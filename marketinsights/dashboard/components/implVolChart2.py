from marketinsights.dashboard.components import DashboardComponent
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px


class ImpliedVolatility2(DashboardComponent):

    def __init__(self, app, bcm, mds, id, theme, market, optionType):
        DashboardComponent.__init__(self, app, bcm, mds, id, theme)
        self.market = market
        self.type = optionType
        self.source = source

    def getContent(self):

        @self.app.callback(Output(self.id, 'children'),
                           [Input('url', 'href')],
                           background=True,
                           manager=self.bcm)
        def load_graph(href):

            if href is None:
                raise PreventUpdate

            optionData = self.getData(self.market).reset_index()
            contracts = optionsData[optionsData["type"] == self.type].dropna()

            contracts = contracts[contracts["underlyingSymbol"] == self.source].sort_values("timeToExpiry")
            # p=puts[puts["Date_Time"]=="2022-10-05"].sort_values("timeToExpiry")

            fig = px.scatter(contracts, x="strike", y="IV", animation_frame="timeToExpiry",
                             template=self.theme,
                             title="{}: Implied Volatility for ".format(self.market, self.source),
                             labels={"y": "Volatility %", "x": "Date"}
                             )

            fig.update_layout(title={'xanchor': 'center', 'yanchor': 'top', 'x': 0.5, 'y': 0.9})

            return dcc.Graph(id=self.id, figure=fig)

        return html.Div(id=self.id, children=[html.Div([html.P("Loading..."), dbc.Spinner(color="primary")], style={"height": "300px"})])
