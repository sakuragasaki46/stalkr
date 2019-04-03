from flask import Flask, render_template
from werkzeug.routing import BaseConverter

class SlugConverter(BaseConverter):
    def __init__(self, url_rule, *items):
        BaseConverter.__init__(self, url_rule)
        self.regex = r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)'

def create_app():
    app = Flask(__name__)

    app.url_map.converters['slug'] = SlugConverter

    @app.route('/')
    def index():
        return render_template('home.html')

    from . import s
    app.register_blueprint(s.bp)
    
    return app
