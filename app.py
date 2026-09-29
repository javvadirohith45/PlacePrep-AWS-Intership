from flask import Flask, render_template
import logging
import os
import sqlite3

from flask_login import LoginManager
from flask_wtf import CSRFProtect

from config import Config
from extensions import db
from models.user import User

from routes.auth import auth_bp
from routes.main import main_bp
from routes.practice import practice_bp
from routes.mock_tests import mock_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp
from routes.companies import companies_bp
from routes.coding import coding_bp
from routes.interviews import interviews_bp
from routes.resume import resume_bp
from routes.dsa import dsa_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------
    if app.config.get('AWS_CLOUDWATCH_ENABLED'):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )

    # ---------------------------------------------------------
    # Extensions
    # ---------------------------------------------------------
    db.init_app(app)
    CSRFProtect(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please sign in to continue.'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    # ---------------------------------------------------------
    # Blueprints
    # ---------------------------------------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(practice_bp)
    app.register_blueprint(mock_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(coding_bp)
    app.register_blueprint(interviews_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(dsa_bp)

    # ---------------------------------------------------------
    # Global template variables
    # ---------------------------------------------------------
    @app.context_processor
    def inject_globals():
        return {
            'app_name': 'PlacePrep'
        }

    # ---------------------------------------------------------
    # Error handlers
    # ---------------------------------------------------------
    @app.errorhandler(403)
    def forbidden(error):
        return (
            render_template(
                'error.html',
                code=403,
                message='You do not have permission to access this page.'
            ),
            403
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            render_template(
                'error.html',
                code=404,
                message='The page you requested could not be found.'
            ),
            404
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            render_template(
                'error.html',
                code=500,
                message='Something went wrong. Please try again.'
            ),
            500
        )

    # ---------------------------------------------------------
    # Database initialization
    # ---------------------------------------------------------
    with app.app_context():

        # Create database tables.
        #
        # IMPORTANT:
        # On Vercel, Config points to PostgreSQL/Neon through
        # DATABASE_URL. No filesystem directory is created here.
        db.create_all()

        # -----------------------------------------------------
        # SQLite-only migrations
        # -----------------------------------------------------
        database_url = app.config.get(
            'SQLALCHEMY_DATABASE_URI',
            ''
        )

        if database_url.startswith('sqlite:///'):

            # Get the SQLite database path from SQLAlchemy URL.
            path = database_url.replace(
                'sqlite:///',
                '',
                1
            )

            if not os.path.isabs(path):
                path = os.path.abspath(path)

            # Ensure the parent directory exists.
            parent_dir = os.path.dirname(path)

            if parent_dir:
                os.makedirs(
                    parent_dir,
                    exist_ok=True
                )

            conn = sqlite3.connect(path)

            try:
                migrations = {
                    'test': [
                        'topic_id INTEGER'
                    ],

                    'coding_problem': [
                        'language_id INTEGER',
                        'input_format TEXT',
                        'output_format TEXT',
                        'constraints TEXT',
                        'examples TEXT',
                        'solution_reference TEXT',
                        'time_limit_ms INTEGER',
                        'memory_limit_mb INTEGER',
                        'placement_level VARCHAR(30)',
                        'category VARCHAR(40)'
                    ],

                    'interview_question': [
                        'topic VARCHAR(120)',
                        'interviewer_checking TEXT',
                        'how_to_answer TEXT',
                        'sample_answer TEXT',
                        'follow_up TEXT'
                    ],

                    'resume': [
                        'storage_key VARCHAR(500)'
                    ],
                }

                for table, columns in migrations.items():

                    table_exists = conn.execute(
                        """
                        SELECT name
                        FROM sqlite_master
                        WHERE type='table'
                        AND name=?
                        """,
                        (table,)
                    ).fetchone()

                    if not table_exists:
                        continue

                    existing_columns = {
                        row[1]
                        for row in conn.execute(
                            f'PRAGMA table_info({table})'
                        ).fetchall()
                    }

                    for column_definition in columns:

                        column_name = column_definition.split()[0]

                        if column_name not in existing_columns:
                            conn.execute(
                                f'ALTER TABLE {table} '
                                f'ADD COLUMN {column_definition}'
                            )

                conn.commit()

            finally:
                conn.close()

        # -----------------------------------------------------
        # Seed database
        # -----------------------------------------------------
        from seed.seed_data import seed_database

        seed_database()

    return app


# -------------------------------------------------------------
# Vercel / WSGI entry point
# -------------------------------------------------------------
app = create_app()


# -------------------------------------------------------------
# Local development
# -------------------------------------------------------------
if __name__ == '__main__':
    app.run(
        debug=True
    )