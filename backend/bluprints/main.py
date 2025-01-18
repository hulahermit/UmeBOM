from . import main_bp

@main_bp.route('/', methods=['GET'])
def get_all():
    return 'Hello World'
