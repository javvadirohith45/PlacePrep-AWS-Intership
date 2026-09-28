"""Small AWS S3 adapter with a safe local-development fallback.

The Flask application can run without AWS credentials. When AWS_S3_BUCKET is
configured, boto3 uses the normal AWS credential chain (instance role,
Elastic Beanstalk role, environment variables, or local AWS profile).
"""
import logging
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import current_app

logger = logging.getLogger(__name__)


def _client():
    return boto3.client('s3', region_name=current_app.config['AWS_REGION'])


def enabled() -> bool:
    return bool(current_app.config.get('AWS_S3_BUCKET'))


def upload_bytes(data: bytes, key: str, content_type: str = 'application/octet-stream') -> Optional[str]:
    if not enabled():
        return None
    bucket = current_app.config['AWS_S3_BUCKET']
    try:
        _client().put_object(
            Bucket=bucket,
            Key=key,
            Body=data,
            ContentType=content_type,
            ServerSideEncryption='AES256',
        )
        return key
    except (BotoCoreError, ClientError) as exc:
        logger.exception('S3 upload failed for %s: %s', key, exc)
        raise RuntimeError('AWS S3 storage is configured but the upload failed.') from exc


def presigned_get_url(key: str, expires: Optional[int] = None) -> Optional[str]:
    if not enabled() or not key:
        return None
    try:
        return _client().generate_presigned_url(
            'get_object',
            Params={'Bucket': current_app.config['AWS_S3_BUCKET'], 'Key': key},
            ExpiresIn=expires or current_app.config['AWS_S3_PRESIGNED_SECONDS'],
        )
    except (BotoCoreError, ClientError) as exc:
        logger.exception('Could not create S3 download URL: %s', exc)
        return None
