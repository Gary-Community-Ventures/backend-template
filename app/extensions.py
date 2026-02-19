# app/extensions.py
from flask_cors import CORS

cors = CORS()  # Initialized here without app, then init_app(app) in __init__
