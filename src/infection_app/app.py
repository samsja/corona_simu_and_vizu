# Dash app initialization
import dash
# User management initialization
import os
from flask_login import LoginManager, UserMixin

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
