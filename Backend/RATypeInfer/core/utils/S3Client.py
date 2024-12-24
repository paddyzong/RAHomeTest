import threading
from django.conf import settings
import boto3
from botocore.config import Config

class S3Client:
    """
    A thread-safe singleton for a Boto3 S3 client.
    """
    _instance = None       # Will hold the single client instance
    _lock = threading.Lock()  # For thread safety

    @classmethod
    def get_client(cls):
        """
        Returns the single S3 client instance. If it does not exist yet,
        it will be created in a thread-safe manner.
        """
        # Double-checked locking pattern
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # Optional: configure S3 client parameters here
                    s3_config = Config(
                        retries = {
                            'max_attempts': 10,
                            'mode': 'standard'
                        },
                        max_pool_connections = 50
                    )
                    cls._instance = boto3.client(
                        's3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        region_name=settings.AWS_REGION, config=s3_config
                        )
        return cls._instance

