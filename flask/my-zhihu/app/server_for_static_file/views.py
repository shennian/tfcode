from flask import send_from_directory
from . import static_file


@static_file.route('/static/<path:path>')
def send_static_file(path):
    print path
    return send_from_directory('static', path)

