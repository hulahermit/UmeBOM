from flask import Blueprint

main_bp = Blueprint('main', __name__)
item_bp = Blueprint('item', __name__)
bom_bp = Blueprint('bom', __name__)
user_bp = Blueprint('user', __name__)

from . import main, item, bom, user
