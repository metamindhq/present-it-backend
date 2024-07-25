import logging
from google.cloud import storage, client


LOGGER = logging.getLogger(__name__)


class ImageLoader(object):
    def __init__(self, bucket_name, storage_client):
        self.bucket = storage_client.bucket(bucket_name)

    def upload_to_gcp_object_store(self, image_path, file_name: str) -> str:
        try:
            blob = self.bucket.blob(file_name)
            blob.upload_from_filename(image_path)
            blob.make_public()
        except FileNotFoundError:
            LOGGER.error(f"File not found: {image_path}")
            raise FileNotFoundError(f"File not found: {image_path}")

        return f"https://storage.googleapis.com/{self.bucket.name}/{file_name}"
