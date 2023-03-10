from marketinsights.dashboard.components import DashboardComponent
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate


class ImpliedVolatility(DashboardComponent):

    def __init__(self, app, bcm, mds, id, theme, market, optionType):
        DashboardComponent.__init__(self, app, bcm, mds, id, theme)
        self.market = market
        self.type = optionType

    def getContent(self):

        @self.app.callback(Output(self.id, 'children'),
                           [Input('url', 'href')],
                           background=True,
                           manager=self.bcm)
        def load_graph(href):

            if href is None:
                raise PreventUpdate

            print("Callback")
            optionData = self.getData(self.market).reset_index()
            print("Got data")
            od = optionData.dropna().set_index(["underlyingSymbol", "Date_Time"])
            od = od[od["type"] == self.type]

            a = []
            for symbol, df in od.groupby(level=0):
                x = pd.DataFrame()
                for date, df2 in df.groupby(level=1):
                    strike = (min(df2["strike"], key=lambda x: abs(x - df2["underlying"][0])))
                    x = pd.concat([x, df2[df2["strike"] == strike]])
                a.append(x)

            IV = pd.DataFrame()
            for x in a:
                opts = x.reset_index()  # opt_utils.get_IV(x.reset_index())
                IV = pd.concat([IV, opts[["Date_Time", "IV"]].set_index("Date_Time").rename(columns={"IV": str(opts["expiry"][0])})], axis=1)
            print("here")

            fig = px.line(IV, x=IV.index, y=IV.columns,
                          template=self.theme,
                          title="{}: Implied Volatility".format(self.market),
                          labels={"y": "Volatility %", "x": "Date"}
                          )

            fig.update_layout(title={'xanchor': 'center', 'yanchor': 'top', 'x': 0.5, 'y': 0.9})

            print("returning graph")
            return [dcc.Graph(id=self.id + "_graph", figure=fig)]

        return html.Div(id=self.id, children=[html.Div([html.P("Loading..."), dbc.Spinner(color="primary")], style={"height": "300px"})])
