import dash

from src.layout import layout
from src.callbacks import register_callbacks

app = dash.Dash(__name__, title='Mortalidad Colombia 2019', suppress_callback_exceptions=True)
server = app.server

app.layout = layout
register_callbacks(app)
