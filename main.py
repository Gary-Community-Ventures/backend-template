from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://dev:dev@localhost/csp_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Flask backend is running'}), 200

# Basic route
@app.route('/')
def index():
    return jsonify({'message': 'Flask backend API', 'version': '1.0.0'})