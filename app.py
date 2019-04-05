from flask import Flask, g, render_template
from werkzeug.routing import BaseConverter
import datetime

class SlugConverter(BaseConverter):
    def __init__(self, url_rule, *items):
        BaseConverter.__init__(self, url_rule)
        self.regex = r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)'

def create_app():
    app = Flask(__name__)

    app.secret_key = b'\xd2\xf7\xa6XtML&\xf6$t\xae&\xbc\xb3\xb2'

    app.url_map.converters['slug'] = SlugConverter

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.before_request
    def inject_variables():
        g.today = datetime.datetime.today()

    import s
    app.register_blueprint(s.bp)

    import accounts
    app.register_blueprint(accounts.bp)
    
    return app
