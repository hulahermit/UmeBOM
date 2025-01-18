from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_cors import CORS

# db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)
# db.init_app(app)
print(app.config)
CORS(app, resources={r"/*": {"origins": "*"}})  # Update this line to handle CORS

with app.app_context():
    from .bluprints import main_bp
    # db.create_all()

app.register_blueprint(main_bp)