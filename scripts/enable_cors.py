from google.cloud import storage


def cors_configuration(bucket_name):
    """Set a bucket's CORS policies configuration."""

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.cors = [
        {
            "origin": ["*"],
            "responseHeader": [
                "Content-Type",
                "x-goog-resumable"],
            "method": ['GET', 'HEAD'],
            "maxAgeSeconds": 3600
        }
    ]
    bucket.patch()

    print(f"Set CORS policies for bucket {bucket.name} is {bucket.cors}")
    return bucket


def main():
    bucket_name = "canva-hackathon"
    cors_configuration(bucket_name)

if __name__ == "__main__":
    main()
