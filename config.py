import os
from urllib.parse import urlsplit, urlunsplit

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Vercel's deployed filesystem is read-only.
# /tmp is the writable directory available to Vercel functions.
if os.environ.get('VERCEL') == '1':
    INSTANCE_DIR = '/tmp/instance'
else:
    INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

os.makedirs(INSTANCE_DIR, exist_ok=True)


def normalize_database_url(value: str) -> str:
    """Normalize common AWS/RDS/PostgreSQL URLs for SQLAlchemy."""
    if not value:
        return 'sqlite:///' + os.path.join(INSTANCE_DIR, 'placeprep.db')

    # Some providers still expose postgres://.
    # SQLAlchemy 2 expects postgresql://.
    if value.startswith('postgres://'):
        value = 'postgresql://' + value[len('postgres://'):]

    # psycopg 3 is the driver used by this project.
    if value.startswith('postgresql://') and '+psycopg' not in value:
        value = value.replace(
            'postgresql://',
            'postgresql+psycopg://',
            1
        )

    return value


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        'placeprep-dev-change-this-key'
    )

    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.environ.get('DATABASE_URL')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Production-friendly connection settings.
    # These are harmless for SQLite.
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.environ.get(
        'COOKIE_SAMESITE',
        'Lax'
    )

    SESSION_COOKIE_SECURE = (
        os.environ.get('COOKIE_SECURE', '0') == '1'
    )

    # AWS / production settings.
    # Local development works without these values.
    AWS_REGION = os.environ.get(
        'AWS_REGION',
        'ap-south-1'
    )

    AWS_S3_BUCKET = os.environ.get(
        'AWS_S3_BUCKET',
        ''
    ).strip()

    AWS_S3_PREFIX = os.environ.get(
        'AWS_S3_PREFIX',
        'placeprep'
    ).strip('/')

    AWS_S3_PRESIGNED_SECONDS = int(
        os.environ.get(
            'AWS_S3_PRESIGNED_SECONDS',
            '900'
        )
    )

    AWS_STORAGE_ENABLED = bool(AWS_S3_BUCKET)

    AWS_CLOUDWATCH_ENABLED = (
        os.environ.get(
            'AWS_CLOUDWATCH_ENABLED',
            '1'
        ) == '1'
    )

    APP_ENV = os.environ.get(
        'APP_ENV',
        'local'
    )