import os
import dash
from dash import dcc, html, CeleryManager
from dash_html_template import Template
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

from quantutils.api.datasource import MIDataStoreRemote
from marketinsights.api.dash import Dashboard

#import diskcache
#cache = diskcache.Cache("./cache")
#background_callback_manager = DiskcacheManager(cache)

REDIS_URL = "redis://192.168.1.205:6379"
# Use Redis & Celery if REDIS_URL set as an env variable
from celery import Celery
celery_app = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)
background_callback_manager = CeleryManager(celery_app)

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP])
load_figure_template(["bootstrap", "materia", "darkly"])

with open('html/index.html', 'r') as file:
    html_layout = file.read()

# Create MDS for charts
mds = MIDataStoreRemote(location="http://pricestore.192.168.1.203.nip.io")

# Build Content
dashboard = Dashboard(app, background_callback_manager, mds, theme="darkly")
#dashboard.addComponent("Chart3", "ImpliedVolatility", {"market": "WTICrudeOil_Options", "optionType": "p"})
#dashboard.addComponent("Chart4", "ImpliedVolatility", {"market": "WTICrudeOil_Options", "optionType": "c"})
dashboard.addComponent("Chart1", "HistoricalPrice", {"market": "WTICrudeOil", "source": "CL=F"})
# dashboard.addComponent("Chart2", "HistoricalVolatility", {"mds": mds, "market": "WTICrudeOil", "source": "CL=F", "window": 20})


content_dict = {'content': html.Div([dcc.Location(id='url', refresh=False), html.Div(dashboard.getContent())])}
app.layout = Template.from_string(html_layout, content_dict)

# run
if __name__ == '__main__':
    # When running this app on the local machine, default to 8080
    port = int(os.getenv('PORT', 8080))
    app.run_server(host='0.0.0.0', port=port, debug=True)
