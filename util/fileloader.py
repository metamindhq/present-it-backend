import logging
import requests
import random
import string
from mutagen.mp3 import MP3
import io
import math


LOGGER = logging.getLogger(__name__)


class FileLoader(object):
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

    def upload_image_uri_to_gcp_object_store(self, image_uri) -> str:
        file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
        try:
            image = requests.get(image_uri)
            blob = self.bucket.blob(f"images/{file_name}.webp")
            blob.upload_from_string(image.content, content_type="image/webp")
            blob.make_public()
        except FileNotFoundError:
            LOGGER.error(f"File not found: {image_uri}")
            raise FileNotFoundError(f"File not found: {image_uri}")

        return f"https://storage.googleapis.com/{self.bucket.name}/images/{file_name}.webp"

    def upload_audio_to_gcp_object_store(self, audio_bytes) -> (int, str):
        file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
        try:
            mp3_file_len = math.ceil(MP3(io.BytesIO(audio_bytes)).info.length)
            # get the audio duration
            blob = self.bucket.blob(f"audio/{file_name}.mp3")
            blob.upload_from_string(audio_bytes, content_type="audio/mpeg")
            blob.make_public()
        except FileNotFoundError:
            LOGGER.error(f"File not found: {audio_bytes}")
            raise FileNotFoundError(f"File not found: {audio_bytes}")

        return mp3_file_len, f"https://storage.googleapis.com/{self.bucket.name}/audio/{file_name}.mp3"
