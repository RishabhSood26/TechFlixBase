import os

from flask import (
    Flask, render_template, redirect, url_for, session
)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load correct config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Blueprints:
    # Authentication
    from . import auth
    app.register_blueprint(auth.bp)

    # Story/game  # Commented out pending functional implementation of story.py
    from . import story
    app.register_blueprint(story.bp)

    # The administration logic
    from . import handlers
    app.register_blueprint(handlers.bp)

    # Code to run only if deployed to production
    if app.config['DEPLOY']:
        from . import deployed
        app.register_blueprint(deployed.bp)

    # Easier debugging
    if app.config['DEBUG']:
        @app.route('/debug')
        def debug():
            # Run in debug console to get app_context.
            # from . import create_app
            # debug_app = create_app()
            # Useful for accessing, e.g, debug_app.config
            debug_session = dict(session)
            raise ValueError

    # Root route
    @app.route('/')
    def index():
        if 'user' in session:
            return redirect(url_for('story.story'))

        return render_template('home.html')

    # Rulebook
    @app.route('/rules')
    def rules():
        return render_template('rulebook.html')

    @app.errorhandler(404)
    def page_not_found(e):
        """ 404 Handler"""
        print("Sending to index")
        return redirect(url_for('index'))

    return app
