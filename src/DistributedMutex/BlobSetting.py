from azure.storage.blob.aio import BlobServiceClient #type: ignore
import asyncio 

class BlobSetting:
    def __init__(self, connection_string, container_name, blob_name):
        self.connection_string = connection_string
        self.container_name = container_name
        self.blob_name = blob_name

        self.connect_blob_storage()

    def connect_blob_storage(self):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(self.container_name)
        self.blob_client = container_client.get_blob_client(self.blob_name)

    def get_blob_client(self):
        return self.blob_client

