import boto3
import logging

LOGGER = logging.getLogger(__name__)


class ImageLoader(object):
    def __init__(self, bucket, access_key, secret_key):
        self.bucket = bucket
        self.s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    def upload_to_s3(self, image_path, s3_file_name: str) -> str:
        try:
            self.s3.upload_file(image_path, self.bucket, s3_file_name)
        except FileNotFoundError:
            LOGGER.error(f"File not found: {image_path}")
            raise FileNotFoundError(f"File not found: {image_path}")

        return f"https://{self.bucket}.s3.amazonaws.com/{s3_file_name}"
