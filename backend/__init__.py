from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})  # Update this line to handle CORS

with app.app_context():
    from .bluprints import main_bp, item_bp, bom_bp
    db.create_all()

app.register_blueprint(main_bp)
app.register_blueprint(item_bp)
app.register_blueprint(bom_bp)

if os.getenv('DEBUG'):
    print('Debug mode!!')
