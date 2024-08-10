import logging
import requests
import random
import string


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

    def upload_uri_to_gcp_object_store(self, image_uri) -> str:
        file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
        try:
            # download image from uri and load it to gcp object store
            image = requests.get(image_uri)
            blob = self.bucket.blob(f"images/{file_name}.webp")
            blob.upload_from_string(image.content)
            blob.make_public()
        except FileNotFoundError:
            LOGGER.error(f"File not found: {image_uri}")
            raise FileNotFoundError(f"File not found: {image_uri}")

        return f"https://storage.googleapis.com/{self.bucket.name}/images/{file_name}.webp"
