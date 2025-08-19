"""Factory for creating the CinemaFlow Flask application.

This module exposes a :func:`create_app` factory which builds and configures
the Flask application instance. Configuration values are loaded from
environment variables using the classes defined in ``cinemaflow.config``.
The application registers a number of blueprints to encapsulate distinct
areas of functionality:

* ``auth`` – user registration, login and logout
* ``movies`` – listing and management of movies and showtimes
* ``bookings`` – customer facing booking flows
* ``admin`` – administrative interfaces for managers and cashiers

Extensions such as the database and migrations are initialised here to
avoid circular imports. Calling ``create_app()`` without arguments will
construct the application using the ``DevelopmentConfig`` class. In a
production setting you should pass the configuration class name through
the ``CINEMAFLOW_CONFIG`` environment variable or manually specify it
when invoking ``create_app``.
"""

import os
from flask import Flask
from .config import load_config
from .extensions import db, migrate, login_manager


def create_app(config_class: str | None = None) -> Flask:
    """Application factory.

    Args:
        config_class: Optional name of a configuration class defined in
            :mod:`cinemaflow.config`. When omitted the value of the
            ``CINEMAFLOW_CONFIG`` environment variable is used. If that
            variable is undefined, :class:`cinemaflow.config.DevelopmentConfig`
            is assumed.

    Returns:
        A configured :class:`~flask.Flask` instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    cfg_name = (
        config_class
        or os.environ.get("CINEMAFLOW_CONFIG")
        or "DevelopmentConfig"
    )
    config_obj = load_config(cfg_name)
    app.config.from_object(config_obj)

    # Initialise extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from .auth import bp as auth_bp
    from .movies import bp as movies_bp
    from .bookings import bp as bookings_bp
    from .admin import bp as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)

    # Default route redirects to home page
    @app.route("/")
    def index() -> str:
        return "Welcome to CinemaFlow!"

    return app
