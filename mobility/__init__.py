import os
from flask import Flask, render_template
from .models import parse_csv_file


def create_app(test_config=None):
    # Create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    # Configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite')
    )

    # Import blueprints
    from . import stats, city, requests

    app.register_blueprint(stats.bp)
    app.register_blueprint(city.bp)
    app.register_blueprint(requests.bp)

    if test_config is None:

        app.config.from_pyfile('config.py', silent=True)
    else:

        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Define routes and views
    @app.route('/team')
    def team():
        return render_template('team.html')

    @app.route('/stats')
    def stats():
        return render_template('stats.html')

    @app.route('/requests')
    def req():
        return render_template('requests.html')

    from . import db
    db.init_app(app)

    with app.app_context():
        db.init_db()
        # parse_csv_file("assets/ugly_csv.csv")

    return app
