from google.cloud import storage


def get_gcp_storage_client(project_id):
    storage_client = storage.Client(project=project_id)
    return storage_client
