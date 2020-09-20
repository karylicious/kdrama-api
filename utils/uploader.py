from google.cloud import storage
import os
from config import GOOGLE_CREDENTIALS_PATH, BUCKET_NAME

class Uploader:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CREDENTIALS_PATH
        self.storage_client = storage.Client()

    def upload_file_to_cloud(self, source_file_name, destination_blob_name):
          
        bucket = self.storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        return blob.public_url

    def delete_file_from_cloud(self, file_name):
        bucket = self.storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.delete()
    
    def delete_file_from_project(self, source_file_name):
        if os.path.isfile(source_file_name):
            os.remove(source_file_name)