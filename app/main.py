from typing import Tuple
from io import BytesIO

from app.settings import settings
from azure.storage.blob import BlobServiceClient, ContainerClient


class AzureBlobCopier:
    def __init__(self):
        self.storage_account_name = settings.storage_account_name
        self.storage_account_auth = settings.storage_account_auth
        self.source_container_name = settings.source_storage_container
        self.destination_container_name = settings.destination_storage_container
        self.account_url = f"https://{self.storage_account_name}.blob.core.windows.net/"

    def client_init(self, type, container_name) -> Tuple[BlobServiceClient, ContainerClient]:
        if type == "blob":
            client = BlobServiceClient(
                account_url=self.account_url,
                credential=self.storage_account_auth,
                container_name=container_name,
            )
        if type == "container":
            client = ContainerClient(
                account_url=self.account_url,
                credential=self.storage_account_auth,
                container_name=container_name,
            )
        return client

    def list_blobs_(self, prefix=None) -> list:
        if prefix:
            prefix == settings.destination_prefix
            container = self.client_init(type="container", container_name=self.destination_container_name)
            return [blob for blob in container.list_blob_names(name_starts_with=prefix)]
        else:
            container = self.client_init(type="container", container_name=self.source_container_name)
            return [blob for blob in container.list_blob_names()]

    def upload_blob_(self) -> None:
        data = BytesIO()
        container_client = self.client_init(type="container", container_name=self.source_container_name)
        for blob in self.diff_containers():
            db = container_client.get_blob_client(blob).download_blob()
            db.readinto(data)
            blob_client = self.client_init(type="blob", container_name=self.destination_container_name)
            bc = blob_client.get_blob_client(container=self.destination_container_name, blob=f"media/{blob}")
            bc.upload_blob(data)

    def diff_containers(self) -> list:
        source_blobs = self.list_blobs_()
        destination_blobs = self.list_blobs_(
            prefix=settings.destination_prefix,
        )
        destination_list_prefix = {str(i).removeprefix(settings.destination_prefix) for i in destination_blobs}
        diff = set(source_blobs) ^ set(destination_list_prefix)
        return diff


def run():
    azure_blob_copier = AzureBlobCopier()
    azure_blob_copier.upload_blob_()


run()
